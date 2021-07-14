from flask.views import MethodView
from flask import request

from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventSchema


# class TaskResource(MethodView):
#     def get(self):
#         tasks = Tasks.query.all()
#         task_schema = TaskSchema().dump(tasks, many=True)
#         return {
#             "status": "success",
#             "data": task_schema,
#         }, 200

#     def post(self):
#         data = request.get_json()
#         task = Tasks.create(**data)

#         return {"message": task.id}
