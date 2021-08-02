from flask.views import MethodView
from app.core.extensions import db
from flask import request, abort, jsonify
from app.data.models import FinalSets, ChoiceSets
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import FinalSetSchema, ChoiceSchema
import pandas as pd
import numpy as np



class FinalSetResource(MethodView):
    def post(self):
        data = request.get_json()
        task_id = data["task_id"]
        ids = data["ids"]
        recommendation_id = data["recommendation_id"]

        exists = db.session.query(
                    db.session.query(FinalSets).filter_by(task_id = data["task_id"]).exists()
        ).scalar()

        if exists:
            return jsonify({"Message": "Final set already recorded for this task_id", 'data': self.get_final_set(data["task_id"])})
        else:
            choice_set = ChoiceSets.query.filter_by(task_id = data["task_id"])
            json_choices = ChoiceSchema(exclude=["created", "updated"]).dump(choice_set, many=True)
            choice_df = pd.DataFrame.from_records(json_choices)
            final_set = choice_df[choice_df["id"].isin(ids)]
            final_set["recommendation_id"] = recommendation_id
            final_set["final_set_id"] = str(uuid4())
            final_set_json = final_set.to_dict(orient = "records")
            db.engine.execute(FinalSets.__table__.insert(), final_set_json)
            return {"message": "final_set_recorded", "data": final_set_json}

    def get(self):
        """
        Get the final set and see how it is structured
        """
        data = request.get_json()
        return {"message": "Final set", "data": self.get_final_set(task_id = data["task_id"])}

    def get_final_set(self, task_id):
        final_set = FinalSets.query.filter_by(task_id = task_id)
        return FinalSetSchema().dump(final_set, many=True)