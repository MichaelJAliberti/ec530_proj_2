import pytest

from datetime import datetime
from src.device.device_interface import DeviceInterface


@pytest.mark.parametrize(
    "device_data, expected",
    [
        [
            {"mac": "aB-cD-eF-01-23-45", "value": 145, "timestamp": "", "excess": 120},
            True,
        ],
        [
            {"mac": "ff-ff-ff-ff-ff-ff", "value": 145, "timestamp": ""},
            True,
        ],
        [
            {"mac": "ff-ff-ff-ff-ff-ff"},
            False,
        ],
        [
            {"excess": 0},
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


@pytest.mark.parametrize(
    "file_path, expected",
    [
        [
            "data/device/device_in_1.json",
            {"mac": "ff-ff-ff-ff-ff-ff", "value": 145, "excess": 120},
        ],
    ],
)
def test_read_from_device(file_path, expected):
    # can't check datetime.now() directly
    data = DeviceInterface.read_from_device(file_path)
    assert isinstance(data["timestamp"], datetime)
    data.pop("timestamp")
    assert data == expected


def test_retrieve_db_data():
    # unfinished until later
    assert True


@pytest.mark.parametrize(
    "data, expected",
    [
        [
            {
                "mac": "aB-cD-eF-01-23-45",
                "value": 145,
                "timestamp": datetime(2022, 2, 14),
            },
            {
                "mac": "aB-cD-eF-01-23-45",
                "value": 145,
                "timestamp": datetime(2022, 2, 14),
            },
        ],
        [
            {
                "mac": "ff-ff-ff-ff-ff-ff",
                "excess": 120,
                "excess2": 121,
                "excess3": 122,
                "excess4": 123,
                "excess5": 124,
            },
            {
                "mac": "ff-ff-ff-ff-ff-ff",
            },
        ],
    ],
)
def test_trim_data(data, expected):
    DeviceInterface.trim_data(data)
    assert data == expected
