from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Events, Users, ChoiceSets
from app.core.extensions import db
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventSchema, ChoiceSchema
import numpy as np
from app.helpers.helper import TREATMENT_GROUPS
import time



class EventResource(MethodView):
    def post(self):
        data = request.get_json()
        null_or_default = lambda x: "NoIPP" if x is None else x
        # get the real ip of the person
        ip = null_or_default(request.headers.get("X-Real-IP"))

        data["real_ip"] = ip

        
        # first we check for the User

        if data["event_type"] == 0:

            response = {
                "message": "This is the initial check for any new user"
            }


            # check if the user exists in the users database
            user_exists_in_users_db = db.session.query(db.session.query(Events).filter_by(real_ip = ip).exists()).scalar()

            # if user exists, find out in which stage user is
            # if there is event_type 13, user finished
            # if there is event_type 7, user finished task1
            # if there is only event_type 1, user has started the task1
            #   
            if user_exists_in_users_db:
                
                # get its task id
                sample_event_to_get_task_id = db.session.query(Events).filter_by(real_ip = ip).first()
                formatted_sample_event = EventSchema(exclude=["created", "updated", "real_ip"]).dump(sample_event_to_get_task_id)
                response["task_id"] = formatted_sample_event["task_id"]
                response["treatment_group"] = formatted_sample_event["treatment_group"]


                # find which stage user is
                # if we have event_type 13
                user_has_finished_task = db.session.query(db.session.query(Events).filter_by(real_ip = ip, event_type = 13).exists()).scalar()
                if user_has_finished_task:
                    
                    response["status"] = "task_finished"

                    return response
                else:
                    # it means user has not finished the task and in the middle of it

                    # we check whether the user has finished the first task. Event code 7 is for questionnaire starting
                    user_has_finished_task1 = db.session.query(db.session.query(Events).filter_by(real_ip = ip, event_type = 7).exists()).scalar()

                    if user_has_finished_task1:
                            
                        response["status"] = "questionnaire_started"

                        return response
                    
                    # if user has started but not finished the task1
                    users_task_1_details = db.session.query(Events).filter_by(real_ip = ip, event_type = 1)
                    task_1_binary = db.session.query(users_task_1_details.exists()).scalar()

                    users_task_1_details_json = EventSchema(exclude=["updated"]).dump(users_task_1_details, many=True)
                    start_time = users_task_1_details_json[0]["created"].split(".")[0]

                    start_time_as_timestamp  =  int(time.mktime(time.strptime(start_time, "%Y-%m-%dT%H:%M:%S")))

                    response["start_timestamp"] = start_time_as_timestamp
                    current_time = int(time.time())
                    remaining_time = current_time - start_time_as_timestamp
                    response["time_remaining"] = remaining_time
                    response["is_timeout"] = remaining_time >= 600


                    if task_1_binary:
                        response["status"] = "task_in_progress"

                        return response

                    # user can not be in the database and not start the task 1. Only add users when they started the task1
            else:
                response["status"] = "new_user"
                return response

                    


        # check if the user already has a task only when they are trying to create a new task
        if data["event_type"] == 1:
            """
            Only when event type is 1 -> task_creation then the new task id will be
            generated.
            """
            # check if there exists already a user in the database with this IP address
            # event type 0 is for checking the user, if it does not exist, create in the Users table
            
            data = request.get_json()
            null_or_default = lambda x: "NoIP" if x is None else x
            # get the real ip of the person
            ip = null_or_default(request.headers.get("X-Real-IP"))

            # add the user to the database Users. For the record only.
            user_data = {

            }


            # now prepare the upload to Events table
            user_exists_in_users_db = db.session.query(db.session.query(Events).filter_by(real_ip = ip).exists()).scalar()
            
            if user_exists_in_users_db:
                return_data = {

                }
                sample_event_to_get_task_id = db.session.query(Events).filter_by(real_ip = ip, event_type = 1).first()
                formatted_sample_event = EventSchema(exclude=["created", "updated", "real_ip"]).dump(sample_event_to_get_task_id)
                task_id = formatted_sample_event["task_id"]
                # sets = ChoiceSets.query.filter_by(task_id=task_id)
                treatment_group = formatted_sample_event["treatment_group"]
                data["task_id"] = task_id
                data["treatment_group"] = treatment_group
            else:
                # if this user is not in the database at all
                user_data["real_ip"] = ip
                user_data["task_status"] = "new_user"
                db.engine.execute(Users.__table__.insert(), user_data)
                data["task_id"] = str(uuid4())
                data["treatment_group"] = next(TREATMENT_GROUPS)


            # if exists:
            #     return_data = self.get_existing_task_events(ip_to_query = ip)
            #     # we need to add a new task id even the person is alreay in  the database bny IP address
            #     return_data[0]["task_id"] = str(uuid4())

            #     return jsonify({"Message": "This user already has an unfinished task", "task_id": return_data[0]["task_id"], 
            #             "treatment_group": return_data[0]["treatment_group"]})
            # else:
            #     data["task_id"] = str(uuid4())
            #     data["treatment_group"] = next(TREATMENT_GROUPS)
            
        Events.create(**data)
        return jsonify({"Message": "Event_created for the user", "task_id": data["task_id"], 
                        "treatment_group": data["treatment_group"]})

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