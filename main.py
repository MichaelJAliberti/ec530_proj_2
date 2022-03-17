from src.data_management.restful_service import RESTService
from src.data_management.resource_factory import ResourceFactory

user_sample = {
    "FullName": "John Doe",
    "Email": "example@example.com",
    "DoB": "1/1/2000",
    "Gender": "male",
    "Weight": 80.2,
    "Height": 156,
    "PrimaryContact": "Jane Doe",
    "SecondaryContact": "Jake Doe",
    "Address": "1 Road Rd"
}

device_sample = {
   "mac":"ff-ff-ff-ff-ff-ff",
   "value":145,
   "excess":120
}

resources = []
for resource in ResourceFactory.make_resources(name="user", sample=user_sample):
    resources.append(resource)
for resource in ResourceFactory.make_resources(name="device", sample=device_sample):
    resources.append(resource)

service = RESTService.build_from_resources(resources)
app = service.app


if __name__ == "__main__":
    app.run()
