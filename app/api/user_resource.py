from flask.views import MethodView
from app.core.extensions import db
from flask import request, abort, jsonify
from app.data.models import Users
from app.schemas.serializer import UserSchema
from datetime import datetime
from app.schemas.serializer import RecommendationSchema
import socket

class UserResource(MethodView):
    
    def post(self):
        data = request.get_json()
        null_or_default = lambda x: "NoIP" if x is None else x
        ip = null_or_default(request.headers.get("X-Real-IP"))
        if ip == "NoIP":
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        data["real_ip"] = ip
        # check if there is a user existing
        exists = db.session.query(
                        db.session.query(Users).filter_by(real_ip = ip).exists()
            ).scalar()
        if exists:
            return {"Message": "User already exists"}
        else:
            data["status"] = "new"
            Users.create(**data)
            return {"Message": "User created successfully"}
