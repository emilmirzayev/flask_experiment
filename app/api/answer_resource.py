from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Answers, Questions
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import AnswerSchema, QuestionSchema



class AnswerResource(MethodView):
    def post(self):
        data = request.get_json()
        answer = Answers.create(**data)
        return jsonify({"Message": "Answer_recorded", 
                        "task_id": data["task_id"],
                        "question_id": data["question_id"],
                        "Answer": data["answer"]})

    def get(self):
        # get performance specific to a task
        data  = request.get_json()
        answers = Answers.query.filter_by(task_id = data["task_id"])

        return jsonify(AnswerSchema().dump(answers, many=True))