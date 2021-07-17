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
        df = pd.DataFrame(np.random.randint(0, 500, size = (100, 5)))
        df.columns = "X Y Z F V".split()
        df["objective_score"] = abs(df.X - df.Z)
        df["task_id"] = data["task_id"]
        records = df.to_dict(orient = "records")
        # for record in records:
        #     ChoiceSets.create(**record)
        db.engine.execute(ChoiceSets.__table__.insert(), records)
        return jsonify({"Choice_set": records})

    def get(self):
        # get choice set specific to a task
        data  = request.get_json()
        sets = ChoiceSets.query.filter_by(task_id = data["task_id"])
        

        return jsonify(ChoiceSchema().dump(sets, many=True))