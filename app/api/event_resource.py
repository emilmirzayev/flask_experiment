from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Events
from app.core.extensions import db
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventSchema
import numpy as np
from app.helpers.helper import TREATMENT_GROUPS



class EventResource(MethodView):
    def post(self):
        data = request.get_json()
        null_or_default = lambda x: "11" if x is None else x
        # get the real ip of the person
        ip = null_or_default(request.headers.get("X-Real-IP"))
        print(f"real_ip is {ip}")

        data["real_ip"] = ip

        # check if there exists already a user in the database with this IP address
        exists = db.session.query(
                    db.session.query(Events).filter_by(real_ip = ip).exists()
        ).scalar()

        if exists:
            return_data = self.get_existing_task_events(ip_to_query = ip)
            return jsonify({"Message": "This user already has an unfinished task", "task_id": return_data[0]["task_id"], 
                        "treatment_group": return_data[0]["treatment_group"]})

        if data["event_type"] == 1:
            """
            Only when event type is 1 -> task_creation then the new task id will be
            generated.
            """
            data["task_id"] = str(uuid4())
            data["treatment_group"] = next(TREATMENT_GROUPS)
            
        Events.create(**data)
        return jsonify({"Message": f"Event_created for the user with IP {ip}", "task_id": data["task_id"], 
                        "treatment_group": data["treatment_group"], "real_ip": data["real_ip"]})

    def get(self):
        # get events specific to a task
        data  = request.get_json()
        events = Events.query.filter_by(task_id = data["task_id"])
        return jsonify(EventSchema().dump(events, many=True))

    # this function is to be used only when there is already an unfinished task for a given user IP
    def get_existing_task_events(self, ip_to_query):
        task_data = Events.query.filter_by(real_ip=ip_to_query)
        returned_data = EventSchema(exclude=["created", "updated", "real_ip"]).dump(task_data, many =True)
        return returned_data