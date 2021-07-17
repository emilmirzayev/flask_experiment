from app.data.models import Questions
# from app.core.extensions import db
from sqlalchemy import inspect
import pandas as pd
from app.core.extensions import db
from flask import jsonify
import json
import os



def create_recommendation(df:pd.DataFrame,columns_to_use:str = "X Y V Z F",  top = True, n:int = 2):

    """
    This will be used to generate recommendations based on
    columns user chooses (to hide)
    """

    ix = set()
    columns = columns_to_use.split()
    if top:
        for col in columns:
            s = df[col].drop(ix).drop_duplicates().sort_values(ascending=False)
            ix |= set(s.index[:n])
    else:
        for col in columns:
            s = df[col].drop(ix).drop_duplicates().sort_values(ascending=True)
            ix |= set(s.index[:n])
    result = df.loc[ix]
    
    return result


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
    print(data_json)
    if inspect(db.engine).has_table("questions"):
        print("table exists")
        exist = Questions.query.first()
        print(exist)
        if not exist:
            
            for question in data_json:
                Questions.create(**question)
         
