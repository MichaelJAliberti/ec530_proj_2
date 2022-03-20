from flask_restful import reqparse, Resource

from src.data_management.error_handling import (
    abort_if_does_not_exist,
    abort_if_operation_unsupported,
)


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, template_data, required_fields=[]):
        resources = []
        data = _get_fields_from_template(template_data)

        for key, value in template_data.items():
            data_ref = _get_data_ref(key, value, data=data)
            value_ref = _get_value_ref(value)

            put_parser, post_parser = _get_parsers(
                template_data=value_ref, required_fields=required_fields
            )

            # NEED LOGIC FOR WHEN TO DO THIS
            resources.append(
                _make_outer_dict_resource(
                    name=key, data=data_ref, post_parser=post_parser
                )
            )
            resources.append(
                _make_inner_dict_resource(
                    name=key, data=data_ref, put_parser=put_parser
                )
            )

        return resources


def _define_new_resource(*, name, class_def):
    """creates a new class for each resource to circumvent flask_restful's
    1:1 class-to-resource restriction

    :param name: name for this resource
    :type: str
    :param class_def: the class definition for this resource
    :type: type

    :return: a copy of class_def with a new name
    :rtype: type
    """
    # source:
    # https://stackoverflow.com/questions/9363068/why-python-exec-define-class-not-working
    return type(name, (class_def,), {})


def _get_data_ref(key, value, *, data):
    """returns a data reference lower in a dictionary, attempts to parse
        past key words like "ID"
    
    :param key: key into data
    :type: str
    :param value: value at key in data
    :type: any
    :param data: data to derive a lower reference from
    :type: dict

    :return: a data reference lower in data
    :rtype: any
    """
    # TYPE CHECK?
    data_ref = data[key]
    if isinstance(value, dict) and list(value.keys())[0] == "ID":
        data_ref["ID"] = {} if isinstance(value["ID"], dict) else []
        data_ref = data_ref["ID"]

    return data_ref


def _get_value_ref(value):
    """returns a value reference in a dictionary, attempts to parse
        past key words like "ID"
    
    :param value: value at some key in a dictionary
    :type: any

    :return: a reference to a value in a dictionary
    :rtype: any
    """
    value_ref = value
    if isinstance(value, dict) and list(value.keys())[0] == "ID":
        value_ref = value["ID"]

    return value_ref


def _get_fields_from_template(template_data):
    """copies top-level keys and types from a template into a new dictionary
    
    :param template_data: partial of full api template data dictionary
    :type: dict

    :return: a new dictionary
    :rtype: dict
    """
    data = {}
    for key, value in template_data.items():
        data[key] = {} if isinstance(value, dict) else [] if isinstance(value, list) else None

    return data


def _get_parsers(*, template_data, required_fields=[]):
    """get parsers for PUT and POST operations
    
    :param template_data: partial of full api template data dictionary
    :type: dict
    :parm required_fields: a list of fields required for post operations
    :type: list

    :return: a parser for PUT requests, a parser for POST requests
    :rtype: tuple
    """
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
            id = str(int(max(data.keys())) + 1 if data.keys() else 1)
            data[id] = {}  # f"{name}ID": id
            for field in args.keys():
                data[id][field] = args[field]
            return {id: data[id]}, 201

    new_resource = _define_new_resource(name=name + "_outer", class_def=OuterResource)
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

    new_resource = _define_new_resource(name=name + "_inner", class_def=InnerResource)
    return {"class": new_resource, "url": f"/{name}/<id>"}
