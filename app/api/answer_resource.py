from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Answers, Questions
from app.core.extensions import db
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import AnswerSchema, QuestionSchema



class AnswerResource(MethodView):
    def post(self):
        data = request.get_json()
        # bulk inserting the answers. Must obey the structure
        db.engine.execute(Answers.__table__.insert(), data)
        
        return jsonify({"Message": "Answers_recorded"}
                        )

    def get(self):
        # get performance specific to a task
        data  = request.get_json()
        answers = Answers.query.filter_by(task_id = data["task_id"])

        return jsonify(AnswerSchema().dump(answers, many=True))