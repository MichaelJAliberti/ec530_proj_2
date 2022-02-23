from flask_restful import reqparse, abort, Resource  # , fields


USER_DATA = {
    "1": {"task": "build an API"},
    "2": {"task": "?????"},
    "3": {"task": "profit!"},
}


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message="Element {} doesn't exist".format(id))


parser = reqparse.RequestParser()
parser.add_argument("task")


class User(Resource):
    def delete(self, id):
        abort_if_does_not_exist(id, USER_DATA)
        del USER_DATA[id]
        return "", 204

    def get(self, id):
        abort_if_does_not_exist(id, USER_DATA)
        return USER_DATA[id]

    def put(self, id):
        args = parser.parse_args()
        task = {"task": args["task"]}
        USER_DATA[id] = task
        return task, 201


class UserList(Resource):
    def get(self):
        return USER_DATA

    def post(self):
        args = parser.parse_args()
        # id = int(max(USER_DATA.keys()).lstrip("todo")) + 1
        # id = "todo%i" % id
        id = int(max(USER_DATA.keys())) + 1
        USER_DATA[id] = {"task": args["task"]}
        return USER_DATA[id], 201


user_info = {
    "sub_urls": ["/users", "/users/<id>"],
    "resources": [UserList, User],
}
