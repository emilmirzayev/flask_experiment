from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Performances
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import PerformanceSchema


class PerformanceResource(MethodView):
    def post(self):
        data = request.get_json()
        event = Performances.create(**data)
        return jsonify({"Message": "Performance recorded", "task_id": data["task_id"], "treatment_group": data["treatment_group"]})

    def get(self):
        # get performance specific to a task
        data  = request.get_json()
        performances = Performances.query.filter_by(task_id = data["task_id"])

        return jsonify(PerformanceSchema().dump(performances, many=True))