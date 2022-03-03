from flask_restful import reqparse, abort, Resource, fields, marshal_with

# field_type_map = {
#     int: fields.Integer,
#     str: fields.String,
#     list: fields.List,
# }

# add_arguments has kwarg input for input parameters!

USER_INFO = {}


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist.")


def abort_if_operation_unsupported(operation):
    abort(405, message=f"{operation.upper()} not supported for this resource.")


class ResourceElement(Resource):
    def __init__(self, **kwargs):
        self.get = kwargs["get"]
        self.delete = kwargs["delete"]
        self.put = kwargs["put"]
        self.post = kwargs["post"]

    def get(self, id):
        return self.get(id)

    def delete(self, id):
        return self.delete(id)

    def put(self, id):
        return self.put(id)

    def post(self):
        return self.post()


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, name, sample, required_fields=[]):
        data = {}
        resources = []

        type_map = _get_type_map(sample=sample)
        put_parser, post_parser = _get_parsers(sample=sample, required_fields=required_fields)

        resources.append(_make_outer_resource(name=name, data=data, post_parser=post_parser))
        # resources.append(_make_inner_resource(name=name, data=data, put_parser=put_parser))

        return resources


def _get_type_map(*, sample):
    """Returns dictionary of types of all input fields"""
    type_map = {}
    for key, value in sample.items():
        type_map[key] = value if isinstance(value, type) else type(value)

    return type_map


def _get_parsers(*, sample, required_fields):
    """Get parsers for put and push operations"""
    put_parser = reqparse.RequestParser()
    post_parser = reqparse.RequestParser()

    for field, value in sample.items():
        put_parser.add_argument(field, type=type(value), required=False)
        post_parser.add_argument(field, type=type(value), required=True if field in required_fields else False)

    return put_parser, post_parser


def _make_outer_resource(*, name, data, post_parser):
    def get(**kwargs):
        return data

    def delete(**kwargs):
        abort_if_operation_unsupported("delete")

    def put(**kwargs):
        abort_if_operation_unsupported("put")

    def post(**kwargs):
        args = post_parser.parse_args()
        id = str(int(max(USER_DATA.keys())) + 1)
        data[id] = {"UserID": id}
        for field in args.keys():
            data[id][field] = args[field]
        return data[id], 201

    return {"get": get, "delete": delete, "put": put, "post": post, "url": f"/{name}"}


def _make_inner_resource(*, name, data, put_parser):
    pass
