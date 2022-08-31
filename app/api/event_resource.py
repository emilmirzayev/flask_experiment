from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Events
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventSchema
import numpy as np
from app.helpers.helper import TREATMENT_GROUPS


class EventResource(MethodView):
    def post(self):
        data = request.get_json()


        if data["event_type"] == 1:
            """
            Only when event type is 1 -> task_creation then the new task id will be
            generated.
            """
            data["task_id"] = str(uuid4())
            data["treatment_group"] = next(TREATMENT_GROUPS)
            
        Events.create(**data)
        return jsonify({"Message": "Event_created", 
        "task_id": data["task_id"], "treatment_group": data["treatment_group"], 
        "real_ip": request.headers.get('HTTP_CF_CONNECTING_IP')})

    def get(self):

        # get events specific to a task
        data  = request.get_json()
        events = Events.query.filter_by(task_id = data["task_id"])

        return jsonify(EventSchema().dump(events, many=True))