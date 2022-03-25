from flask_restful import Resource

from src.data_management.error_handling import *

def define_resource(*, resource_type, key_chain, url, data, put_parser=None, post_parser=None):
    """selects a resource type to return based on resource_type
    """
    if resource_type == "outer_resource":
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
        return OuterResource
    