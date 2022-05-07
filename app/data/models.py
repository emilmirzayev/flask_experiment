from app.core.db_setup import Model, db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

# class Task(Model):
#     __tablename__ = "tasks"

#     id = db.Column(db.Integer(), primary_key=True, nullable=False)
#     creation_date = db.Column(
#         db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False
#     )
#     score = db.Column(db.Float, default=0, nullable=True)
#     events = db.relationship("Event", backref="task", lazy="dynamic")

#     def __repr__(self):
#         return f"Task {self.task_id} created"


# class Tasks(Model):
#     __tablename__ = "tasks"

#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String())
#     events = db.relationship("EventTypes", backref="task", lazy=True)


# class EventTypes(Model):
#     __tablename__ = "event_types"

#     id = db.Column(db.Integer(), primary_key=True)
#     description = db.Column(db.String())
#     task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True)


class Events(Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String, nullable=False)
    event_type = db.Column(db.Integer, nullable=False)
    treatment_group = db.Column(db.Integer, nullable = False)
    data = db.Column(db.JSON, nullable = True)



class Performances(Model):
    __tablename__ = "performances"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String, nullable=False)
    recommendation_id = db.Column(db.String, nullable=False)
    real_performance = db.Column(db.Float, nullable= False)
    recommendation_performance = db.Column(db.Float, nullable= False)
    user_performance = db.Column(db.Float, nullable= False)
    treatment_group = db.Column(db.Integer, nullable=False)
    reward = db.Column(db.Float, nullable= False)


class ChoiceSets(Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String, nullable=False)
    X = db.Column(db.Integer, nullable=False)
    Y = db.Column(db.Integer, nullable=False)
    Z = db.Column(db.Integer, nullable=False)
    F = db.Column(db.Integer, nullable=False)
    V = db.Column(db.Integer, nullable=False)
    objective_score = db.Column(db.Float, nullable=False)


class Recommendations(Model):
    __tablename__ = "recommendations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    choice_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.String, nullable=False)
    recommendation_id = db.Column(db.String, nullable=False)
    columns_used = db.Column(db.String, nullable=False)
    X = db.Column(db.Integer, nullable=True)
    Y = db.Column(db.Integer, nullable=True)
    Z = db.Column(db.Integer, nullable=True)
    F = db.Column(db.Integer, nullable=True)
    V = db.Column(db.Integer, nullable=True)
    objective_score = db.Column(db.Float, nullable=False)


class FinalSets(Model):
    __tablename__ = "finalsets"
    id = db.Column(db.Integer,primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    recommendation_id = db.Column(db.String, nullable=False)
    final_set_id = db.Column(db.String, nullable=False)
    X = db.Column(db.Integer, nullable=True)
    Y = db.Column(db.Integer, nullable=True)
    Z = db.Column(db.Integer, nullable=True)
    F = db.Column(db.Integer, nullable=True)
    V = db.Column(db.Integer, nullable=True)
    objective_score = db.Column(db.Float, nullable=False)

class Answers(Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, nullable = False)
    # putting answer as string, will filter ex-post
    answer = db.Column(db.Integer, nullable = False)


class Questions(Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key = True)
    question_group = db.Column(db.Integer, nullable = False)
    question_header = db.Column(db.String, nullable=True)
    question_type = db.Column(db.String, nullable = False)
    question_body = db.Column(db.String, nullable=False)
    question_answers = db.Column(db.String, nullable=False)
    


class EventTypes(Model):
    __tablename__ = "event_types"
    id = db.Column(db.Integer, primary_key=True)
    event_body = db.Column(db.String, nullable=False)


