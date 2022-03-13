# from src.utils.file import check_file
# from src.device.device_interface import DeviceInterface

from src.data_management.restful_service import RESTService
from src.data_management.resource_factory import ResourceFactory

if __name__ == "__main__":
    sample = {
        "FullName": "John Doe",
        "Email": "example@example.com",
        "DoB": "1/1/2000",
        "Gender": "male",
        "Weight": 80.2,
        "Height": 156,
        "PrimaryContact": "Jane Doe",
        "SecondaryContact": "Jake Doe",
        "Address": "1 Road Rd",
        "Insurance": "Blue Cross",
        "InsuranceGroupID": "U57",
    }

    sample2 = {
        "FullName": "John Doe",
        "Email": "example@example.com",
        "DoB": "1/1/2000",
        "Gender": "male",
        "Weight": 80.2,
        "Height": 156,
        "PrimaryContact": "Jane Doe",
        "SecondaryContact": "Jake Doe",
        "Address": "1 Road Rd",
        "Insurance": "Blue Cross",
        "InsuranceGroupID": "U57",
    }

    resources = ResourceFactory.make_resources(name="user", sample=sample)
    # for element in ResourceFactory.make_resources(name="what", sample=sample):
    #     resources.append(element)
    # for element in ResourceFactory.make_resources(name="why", sample=sample):
    #     resources.append(element)
    # for element in ResourceFactory.make_resources(name="how", sample=sample):
    #     resources.append(element)

    service = RESTService.build_from_resources(resources)
    service.app.run(debug=True)
