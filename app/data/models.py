from app.core.db_setup import Model, db

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
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    event_type = db.Column(db.Integer, nullable=False)
    


class Performances(Model):
    __tablename__ = "performances"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    objective_score = db.Column(db.Float, nullable= False)
    performance_score = db.Column(db.Float, nullable= False)



class ChoiceSets(Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    X = db.Column(db.Integer, nullable=False)
    Y = db.Column(db.Integer, nullable=False)
    Z = db.Column(db.Integer, nullable=False)
    F = db.Column(db.Integer, nullable=False)
    V = db.Column(db.Integer, nullable=False)
    objective_score = db.Column(db.Float, nullable=False)


class Recommendations(Model):
    __tablename__ = "recommendations"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    recommendation_id = db.Column(db.String, nullable=False)
    X = db.Column(db.Integer, nullable=True)
    Y = db.Column(db.Integer, nullable=True)
    Z = db.Column(db.Integer, nullable=True)
    F = db.Column(db.Integer, nullable=True)
    V = db.Column(db.Integer, nullable=True)
    objective_score = db.Column(db.Float, nullable=False)


class Answers(Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)
    question_number = db.Column(db.Integer, nullable = False)
    # putting answer as string, will filter ex-post
    answer = db.Column(db.String, nullable = False)
