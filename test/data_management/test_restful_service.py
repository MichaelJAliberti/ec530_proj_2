import pytest
import requests

from multiprocessing import Process

from src.data_management.restful_service import RESTService
from src.data_management.template import DATA_TEMPLATE


URL = "http://127.0.0.1:5000/"


@pytest.fixture(scope="module", autouse=True)
def service_setup():
    service = RESTService.build_from_templates(DATA_TEMPLATE)
    app = service.app
    server = Process(target=app.run)
    server.start()
    yield
    server.terminate()
    server.join()


def test_get():
    service = RESTService.build_from_templates(DATA_TEMPLATE)
    app = service.app
    app.run(threaded=True)
    assert URL == "http://127.0.0.1:5000/"