from flask.views import MethodView
from app.core.extensions import db
from flask import request, abort, jsonify
from app.data.models import ChoiceSets
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import ChoiceSchema
import pandas as pd
import numpy as np



class ChoiceSetResource(MethodView):
    def post(self):
        data = request.get_json()
        columns = "F1 F2 F3 F4 F5".split()
        # check if exists in the database
        exists = db.session.query(db.session.query(ChoiceSets).filter_by(task_id = data["task_id"]).exists()).scalar()
        if exists:
            return jsonify({'columns''': columns, 'choice_set': self.get_choice_sets(data["task_id"])})

        # we might need to change the minimum value for given feature to 1      
        df = pd.DataFrame(np.random.randint(0, 500, size = (100, 5)))
        
        df.columns = columns
        df["objective_score"] = df["F1"] + df["F3"] + df["F5"]
        df["task_id"] = data["task_id"]
        records = df.to_dict(orient = "records")
        # for record in records:
        #     ChoiceSets.create(**record)
        db.engine.execute(ChoiceSets.__table__.insert(), records)
        return jsonify({'columns''': columns, 'choice_set': self.get_choice_sets(data["task_id"])})

    def get(self):
        # get choice set specific to a task
        data  = request.get_json()
        return jsonify(self.get_choice_sets(data["task_id"]))

    def get_choice_sets(self, task_id):
        sets = ChoiceSets.query.filter_by(task_id=task_id)
        return ChoiceSchema(exclude=["created", "updated", "objective_score"]).dump(sets, many=True)