from app.data.models import Questions, EventTypes
# from app.core.extensions import db
from sqlalchemy import inspect
import pandas as pd
from app.core.extensions import db
from flask import jsonify
import json
import os
from random import choice
from collections import Counter

DEFAULT_REWARD = 1
REWARD_MULTIPLIER = 2


class Recommendation:
    
    def __init__(self, n):

        self.n = n
        self.numbers = []
        
    
    def gather(self, *args):
        

        for step, col in enumerate(zip(*args)):
            most_common = Counter(col).most_common(1)
            if most_common[0][1] > 1:
                most_common = most_common[0][0]
            else:
                most_common = None

            if most_common:
                indexes = []
                for index2, el2 in enumerate(col):
                    if el2 == most_common:
                        indexes.append(index2)
                choosen_index = choice(indexes)
                indexes.remove(choosen_index)
                for i in indexes:
                    args[i].pop(step)
                    args[i].append(0)
                self.gather(*map(lambda col2: col2[step:], args))
            elif set(col).intersection(self.numbers):
                intersection = set(col).intersection(self.numbers)
                indexes = []
                for index3, el3 in enumerate(col):
                    if intersection.issuperset((el3,)):
                        indexes.append(index3)
                choosen_index = choice(indexes)
                indexes.remove(choosen_index)
                for i in indexes:
                    args[i].pop(step)
                    args[i].append(0)
                self.gather(*map(lambda col2: col2[step+1:], args))
            else:
                if len(self.numbers) >= self.n:
                    self.numbers = self.numbers[:self.n]
                    break
                else:
                    self.numbers.extend(col)


def calculate_reward(users_performance, real_performance, default_reward = DEFAULT_REWARD, multiplier = REWARD_MULTIPLIER):
    reward = default_reward + ((users_performance / real_performance) * multiplier)
    return reward



def create_recommendation(df, cols:str = "X Y Z F V", length = 10):

    """
    This function outputs the indices corresponding to the top
    features per column 
    """
    # columns = cols.split()
    

    top_10_per_each = (df
                         .drop("task_id", axis = 1)
                         .melt(id_vars= "objective_score", 
                               var_name= "feature", 
                               ignore_index= False)
                         .sort_values(["feature", "value"], 
                                      ascending = False)
                         .groupby("feature")
                         .value
                         .nlargest(length)
                        ).reset_index()
    d = {
        
    }
    
    d["X"] = top_10_per_each.query("feature == 'X'").level_1.values.tolist()
    d["Y"] = top_10_per_each.query("feature == 'Y'").level_1.values.tolist()
    d["Z"] = top_10_per_each.query("feature == 'Z'").level_1.values.tolist()
    d["F"] = top_10_per_each.query("feature == 'F'").level_1.values.tolist()
    d["V"] = top_10_per_each.query("feature == 'V'").level_1.values.tolist()
    
    def argparse():

        # 'X Y Z F'
        #print(globals())
        args = map(lambda arg: d.get(arg), cols.split(' '))
        
        return args
    
    arguments = argparse()

    
    recommenderGenerator = Recommendation(length)

    recommenderGenerator.gather(*arguments)
    
    
    return recommenderGenerator.numbers


# {def create_recommendation(df:pd.DataFrame,columns_to_use:str = "X Y V Z F",  top = True):

#     """
#     This will be used to generate recommendations based on
#     columns user chooses (to hide)
#     """

#     ix = set()
#     columns = columns_to_use.split()
#     if len(columns) != 5:
#         per_group = round(10/len(columns)) + 1
#     else:
#         per_group = 2
#     if top:
#         for col in columns:
#             s = df[col].drop(ix).drop_duplicates().sort_values(ascending=False)
#             ix |= set(s.index[:per_group])
#     else:
#         for col in columns:
#             s = df[col].drop(ix).drop_duplicates().sort_values(ascending=True)
#             ix |= set(s.index[:per_group])
#     result = df.loc[ix]
    
#     return result.sort_values(by = ["objective_score"], ascending = False).head(10).sample(frac = 1)}


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
    # with open("app/helpers/questions.json") as f:
    #     file = json.load(f)
    # data = pd.json_normalize(file)
    # data.question_answers = data.question_answers.apply(str)
    data = pd.read_csv("app/helpers/questions.csv", sep = ",")
    data_json = data.to_dict(orient = "records")

    if inspect(db.engine).has_table("questions"):
        exist = Questions.query.first()
        if not exist:   
            db.engine.execute(Questions.__table__.insert(), data_json)


def init_event_types():

    data = pd.read_csv("app/helpers/event_types.csv", sep = ",")
    data_json = data.to_dict(orient = "records")

    if inspect(db.engine).has_table("event_types"):

        exist = EventTypes.query.first()

        if not exist:
           db.engine.execute(EventTypes.__table__.insert(), data_json)
         
         
