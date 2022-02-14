from src.device.device_interface import DeviceInterface


def test_check_data_format():
    DeviceInterface("data/device.json")
    assert True


def test_check_file():
    DeviceInterface("data/device.json")
    assert True


def test_check_mac_format():
    DeviceInterface("data/device.json")
    assert True


def test_read_from_device():
    DeviceInterface("data/device.json")
    assert True


def test_retrieve_db_data():
    DeviceInterface("data/device.json")
    assert True


def test_trim_data():
    DeviceInterface("data/device.json")
    assert True
