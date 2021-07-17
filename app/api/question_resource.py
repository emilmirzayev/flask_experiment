from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Questions
from app.schemas.serializer import QuestionSchema
import pandas as pd


class QuestionResource(MethodView):
    def get(self):
        data  = request.get_json()
        questions = Questions.query.all()

        return jsonify(QuestionSchema(exclude = ['created', 'updated']).dump(questions, many=True))