from flask import Flask
from flask_restful import Api

from components.user_info import user_info


class RESTService:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self._collect_components()
        self._add_resources()

    def _collect_components(self):
        self.components = [user_info]

    def _add_resources(self):
        for component in self.components:
            for resource_info in component:
                self.api.add_resource(
                    resource_info["resource"], resource_info["sub_url"]
                )


if __name__ == "__main__":
    passthrough = RESTService()
    passthrough.app.run(debug=True)