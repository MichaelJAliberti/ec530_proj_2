from threading import local
from flask_restful import reqparse, Resource

from src.data_management.error_handling import (
    abort_if_does_not_exist,
    abort_if_operation_unsupported,
)
from src.utils.class_utils import copy_class_def


class ResourceFactory:
    @classmethod
    def make_resources(cls, *, template_data, required_fields=[]):
        """generates resources based on template_data and returns them

        :param template_data: data to convert into resources
        :type: dict
        :param required_fields: fields required for POST requests
        :type: dict

        :return: list of dictionaries of resource classes and urls
        :rtype: list
        """
        data = _copy_keys_from_template(template_data)
        resources = []
        _gen_resources_per_layer(
            template_data=template_data,
            data=data,
            resources=resources,
            required_fields=required_fields,
        )

        return resources


def _copy_keys_from_template(template_data):
    """copies top-level keys and types from a template into a new dictionary

    :param template_data: partial of full api template data dictionary
    :type: dict

    :return: a new dictionary
    :rtype: dict
    """
    data = {}
    for key, value in template_data.items():
        data[key] = (
            {} if isinstance(value, dict) else [] if isinstance(value, list) else None
        )

    return data


def _get_url(key_chain):
    """creates an appropriate resource url from keys traversed in the template

    :param key_chain: list of keys traversed so far
    :type: list

    :return: a resource url
    :rtype: str
    """
    return "/" + "/".join(key_chain)


def _get_value_ref(value):
    """returns a value reference in a dictionary, attempts to parse
    past key words like "<id>"

    :param value: value at some key in a dictionary
    :type: any

    :return: a reference to a value in a dictionary
    :rtype: any
    """
    value_ref = value
    if isinstance(value, dict) and list(value.keys())[0] == "<id>":
        value_ref = value["<id>"]

    return value_ref


def _gen_resources_per_layer(
    *, template_data, data, resources, key_chain=[], required_fields=[]
):
    """recursively generates resources by parsing template_data and appends them
    to resources

    :param template_data: data to convert into resources
    :type: dict
    :param data: data for the api
    :type: dict
    :param resources: list of resources to append to
    :type: list
    :param key_chain: chain of keys so far to form url path for resource
    :type: list
    :param required_fields: fields required for POST requests
    :type: dict
    """
    if isinstance(template_data, dict): 
        for key, value in template_data.items():
            if not isinstance(value, dict): 
                continue

            data_ref = data
            local_chain = key_chain.copy()
            local_chain.append(key)
            url = _get_url(local_chain)

            put_parser, post_parser = _get_parsers(
                template_data=_get_value_ref(value), required_fields=required_fields
            )

            if list(value.keys())[0] == "<id>":
                data_ref = data[key] # make each branch its own dictionary?
                new_resource = _make_outer_dict_resource(data=data_ref, key_chain=local_chain, url=url, post_parser=post_parser)
            else:
                new_resource = _make_inner_dict_resource(data=data_ref, key_chain=local_chain, url=url, put_parser=put_parser)

            resources.append(
                {"class": new_resource, "url": url}
            )
            
            _gen_resources_per_layer(
                template_data=value,
                data=data,
                resources=resources,
                key_chain=local_chain
            )


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


def _make_outer_dict_resource(*, data, key_chain, url, post_parser):
    class OuterResource(Resource):
        def get(self):
            return data

        def delete(self):
            abort_if_operation_unsupported("DELETE", url)

        def put(self):
            abort_if_operation_unsupported("PUT", url)

        def post(self):
            args = post_parser.parse_args()
            id = str(int(max(data.keys())) + 1 if data.keys() else 1)
            data[id] = {}  # f"{url}<id>": id
            for field in args.keys():
                data[id][field] = args[field]
            return {id: data[id]}, 201

    return copy_class_def(name=url, class_def=OuterResource)


def _make_inner_dict_resource(*, data, key_chain, url, put_parser):
    class InnerResource(Resource):
        def get(self, id):
            return _traverse_key_chain(id=id, key_chain=key_chain, data=data)

        def delete(self, id):
            local_data = _traverse_key_chain(id=id, key_chain=key_chain[:-1], data=data)
            key = id if key_chain[-1] == "<id>" else key_chain[-1]
            abort_if_does_not_exist(key, local_data)
            
            del local_data[key]
            return "", 204

        def put(self, id):
            local_data = _traverse_key_chain(id=id, key_chain=key_chain, data=data)
            args = put_parser.parse_args()
            for field in args.keys():
                if args[field]:
                    local_data[field] = args[field]
            return local_data, 201

        def post(self, id):
            abort_if_operation_unsupported("POST", url)

    return copy_class_def(name=url, class_def=InnerResource)


def _traverse_key_chain(*, id, key_chain, data):
    """index into data along keys in key chain 

    :param id: numerical identifier within data
    :type: str
    :param key_chain: chain of keys to be traversed
    :type: list
    :param data: data for the api
    :type: dict

    :return: the value in data at the end of key_chain
    :rtype: any
    """
    local_data = data
    for key in key_chain:
        if key == "<id>":
            abort_if_does_not_exist(id, local_data)
            local_data = local_data[id]
        else:
            abort_if_does_not_exist(key, local_data)
            local_data = local_data[key]

    return local_data