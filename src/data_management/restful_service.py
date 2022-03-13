from flask import Flask
from flask_restful import Api

from src.data_management.resource_element import ResourceElement


class RESTService:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    @classmethod
    def build_from_resources(cls, resources, resource_class=ResourceElement):
        service = RESTService()
        service._add_resources(resources, resource_class)
        return service

    def _add_resources(self, resources, resource_class):
        for resource in resources:
            self.api.add_resource(
                resource_class,
                resource["url"],
                resource_class_kwargs=resource,
            )
