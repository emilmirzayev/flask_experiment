from app.data.models import Questions, EventTypes
# from app.core.extensions import db
from sqlalchemy import inspect
import pandas as pd
from app.core.extensions import db
from flask import jsonify
import json
import os



def create_recommendation(df:pd.DataFrame,columns_to_use:str = "X Y V Z F",  top = True):

    """
    This will be used to generate recommendations based on
    columns user chooses (to hide)
    """

    ix = set()
    columns = columns_to_use.split()
    if len(columns) != 5:
        per_group = round(10/len(columns)) + 1
    else:
        per_group = 2
    if top:
        for col in columns:
            s = df[col].drop(ix).drop_duplicates().sort_values(ascending=False)
            ix |= set(s.index[:per_group])
    else:
        for col in columns:
            s = df[col].drop(ix).drop_duplicates().sort_values(ascending=True)
            ix |= set(s.index[:per_group])
    result = df.loc[ix]
    
    return result.sort_values(by = ["objective_score"], ascending = False).head(10).sample(frac = 1)


infer_dtypes = lambda x: pd.api.types.infer_dtype(x, skipna=True)


# def init_event_types():
#     data = [
#         {"id": 1, "description": "Task created"},
#         {"id": 2, "description": "Task finished"},
#     ]
#     if inspect(db.engine).has_table("event_types"):
#         exist = EventTypes.query.first()
#         if not exist:
#             for event in data:
#                 EventTypes.create(**event)


def init_questions():

    data = pd.read_csv("app/helpers/questions.csv", sep = ";")
    data_json = data.to_dict(orient = "records")

    if inspect(db.engine).has_table("questions"):
        exist = Questions.query.first()
        if not exist:   
            db.engine.execute(Questions.__table__.insert(), data_json)


def init_event_types():

    data = pd.read_csv("app/helpers/event_types.csv", sep = ";")
    data_json = data.to_dict(orient = "records")

    if inspect(db.engine).has_table("event_types"):

        exist = EventTypes.query.first()

        if not exist:
           db.engine.execute(EventTypes.__table__.insert(), data_json)
         
         
