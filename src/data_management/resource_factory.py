from flask_restful import reqparse, abort


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist.")


def abort_if_operation_unsupported(operation, name):
    abort(405, message=f"{operation.upper()} not supported for resource {name}.")


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, name, sample, required_fields=[]):
        data = {}
        resources = []

        put_parser, post_parser = _get_parsers(
            sample=sample, required_fields=required_fields
        )

        resources.append(
            _make_outer_resource(name=name, data=data, post_parser=post_parser)
        )
        # resources.append(_make_inner_resource(name=name, data=data, put_parser=put_parser))

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
    def get(**kwargs):
        return data

    def delete(**kwargs):
        abort_if_operation_unsupported("DELETE", name)

    def put(**kwargs):
        abort_if_operation_unsupported("PUT", name)

    def post(**kwargs):
        args = post_parser.parse_args()
        id = str(int(max(data.keys()).lstrip(name)) + 1) if data.keys() else f"{name}1"
        data[id] = {f"{name}ID": id}
        for field in args.keys():
            data[id][field] = args[field]
        return data[id], 201

    return {"get": get, "delete": delete, "put": put, "post": post, "url": f"/{name}"}


def _make_inner_resource(*, name, data, put_parser):
    def get(**kwargs):
        abort_if_does_not_exist(kwargs[id], data)
        return data[kwargs[id]]
    
    def delete(**kwargs):
        abort_if_does_not_exist(kwargs[id], data)
        del data[kwargs[id]]
        return "", 204

    def put(**kwargs):
        abort_if_does_not_exist(kwargs[id], data)
        args = put_parser.parse_args()
        for field in args.keys():
            data[kwargs[id]][field] = args[field]
        return data[kwargs[id]], 201

    def post(**kwargs):
        abort_if_operation_unsupported("POST", name)

    return {"get": get, "delete": delete, "put": put, "post": post, "url": f"/{name}/<id>"}
