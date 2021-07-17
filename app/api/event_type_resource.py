from flask.views import MethodView
from flask import request, abort, jsonify
from app.data.models import EventTypes
from uuid import uuid4
from datetime import datetime
from app.schemas.serializer import EventTypeSchema


class EventTypeResource(MethodView):
    def get(self):
        data = request.get_json()
        event_types = EventTypes.query.all()

        return jsonify(EventTypeSchema().dump(event_types, many=True))