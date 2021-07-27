from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Performances, FinalSets, ChoiceSets, Recommendations
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import PerformanceSchema, FinalSetSchema, ChoiceSchema, RecommendationSchema
import pandas as pd



class PerformanceResource(MethodView):

    def post(self):
        # get performance specific to a task
        """
        We need to get task id, recommendation_ids and final choice set here.
        Get the choice set, get the recommendation set, get the final set.
        Calculate the average performance for the record
        {
            "task_id":
            "recommendation_id":
            "final_set_id":
        }
        """
        data  = request.get_json()
        task_id = data["task_id"]
        # first we get choice set and calculate the real performance
        choice_set = ChoiceSets.query.filter_by(task_id = data["task_id"])
        json_choices = ChoiceSchema(exclude=["created", "updated"]).dump(choice_set, many=True)
        choice_df = pd.DataFrame.from_records(json_choices)
        real_performance = choice_df.objective_score.nlargest(5).mean()
        # then I need the recommendation performance, for that I need the recommendation id

        recommendation_set = Recommendations.query.filter_by(task_id = data["task_id"], recommendation_id = data["recommendation_id"])
        recommendation_json = RecommendationSchema(exclude=["created", "updated"]).dump(recommendation_set, many=True)
        recommendation_df =  pd.DataFrame.from_records(recommendation_json)
        recommendation_performance = recommendation_df.objective_score.mean()

        # now we get final choices for the task id
        final_choice_set = FinalSets.query.filter_by(task_id = data["task_id"])
        final_choice_json = FinalSetSchema(exclude=["created", "updated"]).dump(final_choice_set, many=True)
        final_chice_df = pd.DataFrame.from_records(final_choice_json)
        user_performance = final_chice_df.objective_score.mean()


        performance = dict(
            
            task_id = data["task_id"], 
            recommendation_id = data["recommendation_id"],
            real_performance = real_performance,
            recommendation_performance = recommendation_performance,
            user_performance = user_performance,
            treatment_group = data["treatment_group"]
        )

        Performances.create(**performance)

        return {"Message": "Performance recorded", "data": performance}

    def get(self):
    # change this

        data = request.get_json()

        performances = Performances.query.filter_by(task_id = data["task_id"])

        return {"Message": "Performance queried", "data": jsonify(PerformanceSchema().dump(performances, many=True))}


    def get_performance(self, task_id):

        performances = Performances.query.filter_by(task_id = task_id)

        return {"Message": "Performance recorded", "data": jsonify(PerformanceSchema().dump(performances, many=True))}
