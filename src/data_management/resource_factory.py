from flask_restful import reqparse, abort, Resource


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist.")


def abort_if_operation_unsupported(operation, name):
    abort(405, message=f"{operation.upper()} not supported for resource {name}.")


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, template_data, required_fields=[]):
        data = _get_fields_from_template(template_data)
        resources = []

        for key, value in template_data.items():
            data_ref = _get_data_ref(key, value, data=data)
            value_ref = _get_value_ref(value)

            put_parser, post_parser = _get_parsers(
                template_data=value_ref, required_fields=required_fields
            )
            resources.append(
                _make_outer_dict_resource(name=key, data=data_ref, post_parser=post_parser)
            )
            resources.append(
                _make_inner_dict_resource(name=key, data=data_ref, put_parser=put_parser)
            )

        return resources


def _get_data_ref(key, value, *, data):
    data_ref = data[key]
    if isinstance(value, dict) and list(value.keys())[0] == "ID":
        data_ref["ID"] = {} if isinstance(value["ID"], dict) else []
        data_ref = data_ref["ID"]

    return data_ref


def _get_value_ref(value):
    value_ref = value
    if isinstance(value, dict) and list(value.keys())[0] == "ID":
        value_ref = value["ID"]

    return value_ref


def _get_fields_from_template(template_data):
    data = {}
    for key, value in template_data.items():
        # could be broader:
        data[key] = {} if isinstance(value, dict) else []

    return data


def _get_parsers(*, template_data, required_fields):
    """Get parsers for put and push operations"""
    put_parser = reqparse.RequestParser()
    post_parser = reqparse.RequestParser()

    for field, value in template_data.items():
        put_parser.add_argument(field, type=type(value), required=False)
        post_parser.add_argument(
            field,
            type=type(value),
            required=True if field in required_fields else False,
        )

    return put_parser, post_parser


def _make_outer_dict_resource(*, name, data, post_parser):
    class OuterResource(Resource):
        def get(self):
            return data

        def delete(self):
            abort_if_operation_unsupported("DELETE", name)

        def put(self):
            abort_if_operation_unsupported("PUT", name)

        def post(self):
            args = post_parser.parse_args()
            id = str(
                int(max(data.keys())) + 1
                if data.keys()
                else 1
            )
            data[id] = {} # f"{name}ID": id
            for field in args.keys():
                data[id][field] = args[field]
            return {id: data[id]}, 201

    # source:
    # https://stackoverflow.com/questions/9363068/why-python-exec-define-class-not-working
    new_resource = type(name + "_outer", (OuterResource,), {})
    return {"class": new_resource, "url": f"/{name}"}


def _make_inner_dict_resource(*, name, data, put_parser):
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
