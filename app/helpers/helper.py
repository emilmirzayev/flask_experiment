# from app.data.models import EventTypes
# from app.core.extensions import db
# from sqlalchemy import inspect
import pandas as pd
from flask import jsonify


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



