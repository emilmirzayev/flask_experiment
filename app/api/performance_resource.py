from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Performances, FinalSets, ChoiceSets, Recommendations
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import PerformanceSchema, FinalSetSchema, ChoiceSchema, RecommendationSchema


class PerformanceResource(MethodView):
    def post(self):
        # change this
        data = request.get_json()
        event = Performances.create(**data)
        return jsonify({"Message": "Performance_recorded", "task_id": data["task_id"], "treatment_group": data["treatment_group"]})

    def get(self):
        # get performance specific to a task
        """
        We need to get task id, recommendation_ids and final choice set here.
        Get the choice set, get the recommendation set, get the final set.
        Calculate the average performance for the record
        """
        data  = request.get_json()
        task_id = data["task_id"]
        # first we get choice set and calculate the real performance
        choice_set = ChoiceSets.query.filter_by(task_id = data["task_id"])
        json_choices = ChoiceSchema(exclude=["created", "updated"]).dump(sets, many=True)
        choice_df = pd.DataFrame.from_records(json_choices)
        real_performance = choice_df.objective_score.nlargest(5).mean()
        # then I need the recommendation performance, for that I need the recommendation id

        recommendation_set = Recommendations.query.filter_by(task_id = data["task_id"], recommendation_id = data["recommendation_id"])
        recommendation_json = RecommendationSchema(exclude=["created", "updated"]).dump(sets, many=True)
        recommendation_df =  pd.DataFrame.from_records(recommendation_json)
        recommendation_performance = recommendation_df.objective_score.mean()

        # now we get final choices for the task id
        final_choice_set = FinalSets.query.filter_by(task_id = data["task_id"])
        final_choice_json = FinalSetSchema(exclude=["created", "updated"]).dump(sets, many=True)
        final_chice_df = pd.DataFrame.from_records(final_choice_json)
        user_performance = final_chice_df.objective_score.mean()




        performances = Performances.query.filter_by(task_id = data["task_id"])

        return jsonify(PerformanceSchema().dump(performances, many=True))