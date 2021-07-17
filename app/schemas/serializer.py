from app.data.models import ChoiceSets, Events, Performances, Recommendations, Answers, Questions, EventTypes
from app.core.extensions import ma
from marshmallow import fields



# class TaskSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Tasks

#     events = fields.Nested("EventSchema", many=True, exclude=("task_id",))


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Events
        include_fk = True


class PerformanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Performances
        include_fk = True


class ChoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChoiceSets
        include_fk = True


class RecommendationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recommendations
        include_fk = True
    

class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answers
        include_fk = True


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Questions
        include_fk = True


class EventTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventTypes
        include_fk = True
