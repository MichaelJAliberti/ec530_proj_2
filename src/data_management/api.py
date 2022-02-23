from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields


parser = reqparse.RequestParser()
parser.add_argument("task")


class RESTService:
    def __init__(self, name, data):
        self.name = name
        self.data = data

        self.app = Flask(self.name)
        self.api = Api(self.app)
        self._add_resources()

    def _add_resources(self):
        self.api.add_resource(
            ElementList, f"/{self.name}", resource_class_kwargs={"data": self.data}
        )
        self.api.add_resource(
            Element, f"/{self.name}/<id>", resource_class_kwargs={"data": self.data}
        )


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message="Element {} doesn't exist".format(id))


class Element(Resource):
    def __init__(self, **kwargs):
        self.data = kwargs["data"]

    def delete(self, id):
        abort_if_does_not_exist(id, self.data)
        del self.data[id]
        return "", 204

    def get(self, id):
        abort_if_does_not_exist(id, self.data)
        return self.data[id]

    def put(self, id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        self.data[id] = task
        return task, 201


class ElementList(Resource):
    def __init__(self, **kwargs):
        self.data = kwargs["data"]

    def get(self):
        return self.data

    def post(self):
        args = parser.parse_args()
        # id = int(max(self.data.keys()).lstrip("todo")) + 1
        # id = "todo%i" % id
        id = max(self.data.keys()) + 1
        self.data[id] = {"task": args["task"]}
        return self.data[id], 201


if __name__ == "__main__":
    sample_data = {
        1: {"task": "build an API"},
        2: {"task": "?????"},
        3: {"task": "profit!"},
    }
    passthrough = RESTService("todos", sample_data)
    passthrough.app.run(debug=True)
