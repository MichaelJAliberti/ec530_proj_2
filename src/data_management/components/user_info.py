from flask_restful import reqparse, abort, Resource, fields, marshal_with


USER_DATA = {
    "0": {
        "UserID": "0",
        "FullName": "John Doe",
        "Email": "example@example.com",
        "DoB": "1/1/2000",
        "Gender": "male",
        "Weight": 80.2,
        "Height": 156,
        "PrimaryContact": "Jane Doe",
        "SecondaryContact": "Jake Doe",
        "Address": "1 Road Rd",
        "Insurance": "Blue Cross",
        "InsuranceGroupID": "U57",
    },
}

fields = {
    "UserID": fields.Integer,
    "FullName": fields.String,
    "Email": fields.String,
    "DoB": fields.String,
    "Gender": fields.String,
    "Weight": fields.Arbitrary,
    "Height": fields.Arbitrary,
    "PrimaryContact": fields.String,
    "SecondaryContact": fields.String,
    "Address": fields.String,
    "Insurance": fields.String,
    "InsuranceGroupID": fields.String,
}

base_parser = reqparse.RequestParser()
base_parser.add_argument("DoB", type=str, required=False)
base_parser.add_argument("Gender", type=str, required=False)
base_parser.add_argument("Weight", type=float, required=False)
base_parser.add_argument("Height", type=float, required=False)
base_parser.add_argument("PrimaryContact", type=str, required=False)
base_parser.add_argument("SecondaryContact", type=str, required=False)
base_parser.add_argument("Address", type=str, required=False)
base_parser.add_argument("Insurance", type=str, required=False)
base_parser.add_argument("InsuranceGroupID", type=str, required=False)

parser = base_parser.copy()
parser.add_argument("FullName", type=str, required=True, help="FullName cannot be blank.")
parser.add_argument("Email", type=str, required=True, help="Email cannot be blank.")

put_parser = base_parser.copy()
put_parser.add_argument("FullName", type=str, required=False)
put_parser.add_argument("Email", type=str, required=False)


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist")


class User(Resource):
    def delete(self, id):
        abort_if_does_not_exist(id, USER_DATA)
        del USER_DATA[id]
        return "", 204

    def get(self, id):
        abort_if_does_not_exist(id, USER_DATA)
        return USER_DATA[id]

    def put(self, id):
        abort_if_does_not_exist(id, USER_DATA)
        args = put_parser.parse_args()
        for field in args.keys():
            USER_DATA[id][field] = args[field]
        return USER_DATA[id], 201


class UserList(Resource):
    def get(self):
        return USER_DATA

    def post(self):
        args = parser.parse_args()
        id = str(int(max(USER_DATA.keys())) + 1)
        USER_DATA[id] = {"UserID": id}
        for field in args.keys():
            USER_DATA[id][field] = args[field]
        return USER_DATA[id], 201


user_info = [
    {
        "resource": UserList,
        "sub_url": "/users",
    },
    {
        "resource": User,
        "sub_url": "/users/<id>",
    },
]
