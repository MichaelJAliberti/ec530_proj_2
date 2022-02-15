import pytest

from src.device.device_interface import DeviceInterface


@pytest.mark.parametrize(
    "device_data, expected",
    [
        [
            {
                "mac": "aB-cD-eF-01-23-45",
                "value": 145,
                "timestamp": "",
                "excess": 120
            },
            True,
        ],
        [
            {
                "mac": "ff-ff-ff-ff-ff-ff",
                "value": 145,
                "timestamp": ""
            },
            True,
        ],
        [
            {
                "mac": "ff-ff-ff-ff-ff-ff"
            },
            False,
        ],
        [
            {
                "excess": 0
            },
            False,
        ],
    ],
)
def test_check_data_format(device_data, expected):
    assert DeviceInterface.check_data_format(device_data) == expected


@pytest.mark.parametrize(
    "file_path, expected",
    [
        [
            "data/device/device_in_1.json",
            True,
        ],
        [
            "data/device/device_in_2.txt",
            False,
        ],
        [
            "data/device/no_file.json",
            False,
        ],
    ],
)
def test_check_file(file_path, expected):
    assert DeviceInterface.check_file(file_path) == expected


@pytest.mark.parametrize(
    "mac, expected",
    [
        [
            "aB-cD-eF-01-23-45",
            True,
        ],
        [
            "aB-cD-eF-01-23-45-ec",
            False,
        ],
        [
            "aB-cD-eF-01-23",
            False,
        ],
        [
            "gibberish",
            False,
        ],
        [
            100,
            False,
        ],
    ],
)
def test_check_mac_format(mac, expected):
    assert DeviceInterface.check_mac_format(mac) == expected


def test_read_from_device():
    DeviceInterface("data/device.json")
    assert True


def test_retrieve_db_data():
    # unfinished until later
    assert True


def test_trim_data():
    DeviceInterface("data/device.json")
    assert True
