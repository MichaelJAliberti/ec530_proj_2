from src.device.device_interface import DeviceInterface


def test_placeholder():
    DeviceInterface("data/device.json")
    assert True
