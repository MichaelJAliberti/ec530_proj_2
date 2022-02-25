from flask_restful import reqparse, abort, Resource, fields, marshal_with

field_type_map = {
    int: fields.Integer,
    str: fields.String,
    list: fields.List,
}


class ResourceField(Resource):
    def __init__(self, data):
        self.data = data

    def get(self, id):
        abort_if_does_not_exist(id, self.data)
        return self.data[id]

    def put(self, id):
        abort_if_does_not_exist(id, self.data)
        args = put_parser.parse_args()
        for field in args.keys():
            self.data[id][field] = args[field]
        return self.data[id], 201


class ResourceElement(Resource):
    def __init__(self, data, put_parser):
        self.data = data

    def delete(self, id):
        abort_if_does_not_exist(id, self.data)
        del self.data[id]
        return "", 204

    def get(self, id):
        abort_if_does_not_exist(id, self.data)
        return self.data[id]

    def put(self, id):
        abort_if_does_not_exist(id, self.data)
        args = put_parser.parse_args()
        for field in args.keys():
            self.data[id][field] = args[field]
        return self.data[id], 201


class ResourceList(Resource):
    def __init__(self, data, post_parser):
        self.data = data

    def get(self):
        return self.data

    def post(self):
        args = post_parser.parse_args()
        id = str(int(max(self.data.keys())) + 1)
        self.data[id] = {"UserID": id}
        for field in args.keys():
            self.data[id][field] = args[field]
        return self.data[id], 201


class ResourceFactory:
    def __init__(self):
        pass

    @classmethod
    def set_parsers(cls, *, example, required_post_fields=None, required_put_fields=None):
        base_parser = reqparse.RequestParser()
        for field, value in example.items():
            base_parser.add_argument(field, type=type(value))

        put_parser = base_parser.copy()
        post_parser = base_parser.copy()

        return put_parser, post_parser



if __name__ == "__main__":
    print(fields)
    print(field_type_map)
    field_example = {
        "UserID": "0",
        "FullName": "John Doe",
        "Email": "example@example.com",
        "DoB": "1/1/2000",
        "Gender": "male",
        "Weight": 80.2,
        "Height": 156,
        "PrimaryDoctorID": "Jill Doe",
        "PrimaryContact": "Jane Doe",
        "SecondaryContact": "Jake Doe",
        "Address": "1 Road Rd",
        "Insurance": "Blue Cross",
        "InsuranceGroupID": "U57",
    }

    required_fields_example = []
