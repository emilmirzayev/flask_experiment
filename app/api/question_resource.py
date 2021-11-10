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
        data = pd.read_csv("app/helpers/questions.csv")
        json = data.groupby("question_group").agg(lambda x: x.tolist()).to_dict("index")

        return jsonify(json)