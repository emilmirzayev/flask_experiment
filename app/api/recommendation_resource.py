from flask.views import MethodView
from app.core.extensions import db
from flask import request, abort, jsonify
from app.data.models import Recommendations, ChoiceSets
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import RecommendationSchema
import pandas as pd
import numpy as np
from app.helpers.helper import create_recommendation


class RecommendationResource(MethodView):
    def post(self):
        """
        Needed fields:
        {
            "task_id": "something",
            "columns_to_use": "string separated columns"
        }
        """
        data = request.get_json()
        print(data)
        df_records = (pd
                        .DataFrame(RecommendationSchema().dump(ChoiceSets.query.filter_by(task_id = data["task_id"]), many=True))
                        )
        df = df_records[df_records.columns.difference(["created", "updated"])]
        # rename column ID to avoid Uniqueness conflict with choice
        df = df.rename(columns = {"id": "choice_id"})
        cols = data["columns_to_use"]
        recommendations = create_recommendation(df, columns_to_use= cols)
        uuid = str(uuid4())
        recommendations["recommendation_id"] = uuid
        recommendations["columns_used"] = data["columns_to_use"]
        print(uuid)
        recommendations_json = recommendations.to_dict(orient = "records")
        db.engine.execute(Recommendations.__table__.insert(), recommendations_json)
        return {"message":recommendations_json}

    def get(self):
        # get recommendation set specific to a task and id string
        """
        Needed fields:
        {
            "task_id": "something",
            "recommendation_id": "some uuid"
        }
        """
        data  = request.get_json()
        sets = Recommendations.query.filter_by(task_id = data["task_id"], recommendation_id = data["recommendation_id"])

        return jsonify(RecommendationSchema(exclude=["created", "updated", "objective_score"]).dump(sets, many=True))

