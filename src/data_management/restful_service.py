from flask import Flask
from flask_restful import Api

from src.data_management.resource_factory import ResourceFactory


class RESTService:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    @classmethod
    def build_from_samples(cls, sample):
        service = RESTService()
        service._add_resources(
            ResourceFactory.make_resources(name="user", sample=sample)
        )
        return service

    @classmethod
    def build_from_resources(cls, resources):
        service = RESTService()
        service._add_resources(resources)
        return service

    def _add_resources(self, resources):
        for resource in resources:
            self.api.add_resource(resource["class"], resource["url"])
