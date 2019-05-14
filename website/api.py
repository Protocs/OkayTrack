from flask import jsonify, request
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from .utils import generate_token, PRIORITIES, STAGES

from .db import User, db, Task
from .app import api

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("login", required=True)
auth_parser.add_argument("password", required=True)


class Auth(Resource):
    def post(self):
        args = auth_parser.parse_args()
        user = User.get_by_username(args["login"])
        if user is None:
            return jsonify({"error": "wrong user"})
        if check_password_hash(user.password_hash, args["password"]):
            token = str(generate_token())
            user.api_token = token
            db.session.commit()
            return jsonify({"token": token})
        else:
            return jsonify({"error": "wrong password"})


class TaskList(Resource):
    def get(self):
        token = request.args.get("token")
        if token is None:
            return jsonify({"error": "Invalid token"})
        user = User.get_by_token(token)
        if user is None:
            return jsonify({"error": "Invalid token"})

        response = []
        for task in Task.get_user_tasks(user.name):
            response.append({
                "id": task.id,
                "author": task.username,
                "name": task.name,
                "description": task.task,
                "performer": task.performer,
                "priority": PRIORITIES[task.priority] if task.priority is not None else None,
                "stage": STAGES[task.stage] if task.stage is not None else None,
                "completed": task.completed,
                "category": {
                    "id": task.category_id,
                    "name": task.category.name
                } if task.category is not None else None,
                "tags": [
                    {
                        "id": tag.id,
                        "name": tag.tag
                    } for tag in task.tags
                ] if task.tags is not None else None
            })
        return jsonify(response)


class TaskApi(Resource):
    def get(self, task_id):
        ...

api.add_resource(Auth, "/api/auth")
api.add_resource(TaskList, "/api/task")
