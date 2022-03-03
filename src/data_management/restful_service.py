from flask import Flask
from flask_restful import Api


class RESTService:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    @classmethod
    def build_from_resources(cls, resources):
        service = RESTService()
        service._add_resources(resources)
        return service

    def _add_resources(self, resources):
        for resource in resources:
            self.api.add_resource(
                resource, resource.url
            )


if __name__ == "__main__":
    passthrough = RESTService()
    passthrough.app.run(debug=True)
