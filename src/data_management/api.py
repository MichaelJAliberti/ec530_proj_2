from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


TODOS = {
    "todo1": {"task": "build an API"},
    "todo2": {"task": "?????"},
    "todo3": {"task": "profit!"},
}

parser = reqparse.RequestParser()
parser.add_argument("task")


class RESTService:
    def __init__(self, name):
        self.app = Flask(name)
        self.api = Api(self.app)
        self.api.add_resource(ElementList, "/todos")
        self.api.add_resource(Element, "/todos/<id>")


def abort_if_does_not_exist(id):
    if id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(id))


class Element(Resource):
    def get(self, id):
        abort_if_does_not_exist(id)
        return TODOS[id]

    def delete(self, id):
        abort_if_does_not_exist(id)
        del TODOS[id]
        return "", 204

    def put(self, id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        TODOS[id] = task
        return task, 201


class ElementList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        id = int(max(TODOS.keys()).lstrip("todo")) + 1
        id = "todo%i" % id
        TODOS[id] = {"task": args["task"]}
        return TODOS[id], 201


if __name__ == "__main__":
    passthrough = RESTService("placeholder")
    passthrough.app.run(debug=True)
