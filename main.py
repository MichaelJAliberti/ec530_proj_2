from src.data_management.restful_service import RESTService
from src.data_management.resource_factory import ResourceFactory
from src.data_management.template import DEVICE_TEMPLATE, USER_TEMPLATE


service = RESTService.build_from_templates(DEVICE_TEMPLATE, USER_TEMPLATE)
app = service.app


if __name__ == "__main__":
    app.run()
