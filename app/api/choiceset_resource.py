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
        columns = "X Y Z F V".split()
        # check first if such choice set for that task id exists. if yes, return it. if not, create it
        exists = db.session.query(
                    db.session.query(ChoiceSets).filter_by(task_id = data["task_id"]).exists()
        ).scalar()

        if exists:
            return jsonify({"Message": "Choice set already exists for this task_id, returning", 'columns''': columns, 'choice_set': self.get_choice_sets(data["task_id"])})
        else:
                
            df = pd.DataFrame(np.random.randint(0, 500, size = (100, 5)))
            
            df.columns = columns
            df["objective_score"] = df.X + df.Z + df.V
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