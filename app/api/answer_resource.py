from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Answers
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import AnswerSchema



class AnswerResource(MethodView):
    def post(self):
        data = request.get_json()
        answer = Answers.create(**data)
        return jsonify({"Message": "Answer recorded", 
                        "task_id": data["task_id"],
                        "question_number": data["question_number"]})

    def get(self):
        # get performance specific to a task
        data  = request.get_json()
        answers = Answers.query.filter_by(task_id = data["task_id"])

        return jsonify(AnswerSchema().dump(answers, many=True))