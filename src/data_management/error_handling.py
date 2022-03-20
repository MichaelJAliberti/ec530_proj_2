from flask_restful import abort


def abort_if_does_not_exist(id, data):
    if id not in data:
        abort(404, message=f"Element {id} doesn't exist.")


def abort_if_operation_unsupported(operation, name):
    abort(405, message=f"{operation.upper()} not supported for resource {name}.")
