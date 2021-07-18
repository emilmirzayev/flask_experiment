from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Events
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventSchema
import random


class EventResource(MethodView):
    def post(self):
        data = request.get_json()
        data["task_id"] = str(uuid4())
        treatment_group = "Already_provided"
        if data["event_type"] == 1:
            treatment_group = random.randint(1, 4)
        event = Events.create(**data)
        return jsonify({"Message": "Event_created", "task_id": data["task_id"], "treatment_group": treatment_group})

    def get(self):
        # get events specific to a task
        data  = request.get_json()
        events = Events.query.filter_by(task_id = data["task_id"])

        return jsonify(EventSchema().dump(events, many=True))