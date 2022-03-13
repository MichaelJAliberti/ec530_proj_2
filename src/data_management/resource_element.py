from flask_restful import Resource

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