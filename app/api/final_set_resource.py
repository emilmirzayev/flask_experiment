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
        choice_set = ChoiceSets.query.filter_by(task_id = data["task_id"])
        json_choices = ChoiceSchema(exclude=["created", "updated"]).dump(sets, many=True)
        choice_df = pd.DataFrame.from_records(json_choices)
        final_set = choice_df[choice_df["id"].isin(ids)]
        final_set["recommendation_id"] = recommendation_id
        final_set_json = final_set.to_dict(orient = "records")
        db.engine.execute(FinalSets.__table__.insert(), final_set_json)
        return {"message": "final_set_recorded"}