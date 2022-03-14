from flask_restful import reqparse, abort, Resource


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist.")


def abort_if_operation_unsupported(operation, name):
    abort(405, message=f"{operation.upper()} not supported for resource {name}.")


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, name, sample, required_fields=[]):
        data = {"filler": "Hello World"}
        resources = []

        put_parser, post_parser = _get_parsers(
            sample=sample, required_fields=required_fields
        )

        resources.append(
            _make_outer_resource(name=name, data=data, post_parser=post_parser)
        )
        resources.append(
            _make_inner_resource(name=name, data=data, put_parser=put_parser)
        )

        return resources


def _get_parsers(*, sample, required_fields):
    """Get parsers for put and push operations"""
    put_parser = reqparse.RequestParser()
    post_parser = reqparse.RequestParser()

    for field, value in sample.items():
        put_parser.add_argument(field, type=type(value), required=False)
        post_parser.add_argument(
            field,
            type=type(value),
            required=True if field in required_fields else False,
        )

    return put_parser, post_parser


def _make_outer_resource(*, name, data, post_parser):
    class OuterResource(Resource):
        def get(self):
            return data

        def delete(self):
            abort_if_operation_unsupported("DELETE", name)

        def put(self):
            abort_if_operation_unsupported("PUT", name)

        def post(self):
            args = post_parser.parse_args()
            id = (
                str(int(max(data.keys()).lstrip(name)) + 1)
                if data.keys()
                else f"{name}1"
            )
            data[id] = {f"{name}ID": id}
            for field in args.keys():
                data[id][field] = args[field]
            return data[id], 201

    # source:
    # https://stackoverflow.com/questions/9363068/why-python-exec-define-class-not-working
    new_resource = type(name + "_outer", (OuterResource,), {})
    return {"class": new_resource, "url": f"/{name}"}


def _make_inner_resource(*, name, data, put_parser):
    class InnerResource(Resource):
        def get(self, id):
            abort_if_does_not_exist(id, data)
            return data[id]

        def delete(self, id):
            abort_if_does_not_exist(id, data)
            del data[id]
            return "", 204

        def put(self, id):
            abort_if_does_not_exist(id, data)
            args = put_parser.parse_args()
            for field in args.keys():
                if args[field]:
                    data[id][field] = args[field]
            return data[id], 201

        def post(self, id):
            abort_if_operation_unsupported("POST", name)

    new_resource = type(name + "_inner", (InnerResource,), {})
    return {"class": new_resource, "url": f"/{name}/<id>"}
