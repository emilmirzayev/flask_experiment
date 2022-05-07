from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import Questions
from app.schemas.serializer import QuestionSchema
import pandas as pd
import json


class QuestionResource(MethodView):
    def get(self):
        # data  = request.get_json()
        # questions = Questions.query.all()
        # with open("app/helpers/questions.json") as f:
        #     file = json.load(f)
        data = pd.read_csv("app/helpers/questions.csv", sep = ";")
        json = ([data
                    .groupby("question_group")
                    .apply(lambda x:  x[["id", "question_header","question_type","question_body", "question_answers"]]
                            .to_dict("r"))
                        .to_dict()])

        return jsonify(json)