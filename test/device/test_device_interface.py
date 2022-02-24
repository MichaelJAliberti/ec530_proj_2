import pytest

from contextlib import nullcontext as does_not_raise
from datetime import datetime
from src.device.device_interface import DeviceInterface


@pytest.mark.parametrize(
    "device_data, expected_exception",
    [
        [
            {
                "mac": "aB-cD-eF-01-23-45",
                "value": 145,
                "type": "thermometer",
                "time_received": "",
            },
            does_not_raise(),
        ],
        [
            {
                "value": 145,
                "type": "monitor",
                "time_received": "",
                "mac": "ff-ff-ff-ff-ff-ff",
                "excess": 120,
            },
            does_not_raise(),
        ],
        [
            {"mac": "ff-ff-ff-ff-ff-ff"},
            pytest.raises(ValueError, match="Missing required fields"),
        ],
        [
            {
                "mac": "gibberish",
                "value": 145,
                "type": "thermometer",
                "time_received": "",
            },
            pytest.raises(ValueError, match="Invalid mac address"),
        ],
        [
            {
                "mac": "aB-cD-eF-01-23-45-ec",
                "value": 145,
                "type": "thermometer",
                "time_received": "",
            },
            pytest.raises(ValueError, match="Invalid mac address"),
        ],
        [
            {
                "mac": "aB-cD-eF-01-23",
                "value": 145,
                "type": "thermometer",
                "time_received": "",
            },
            pytest.raises(ValueError, match="Invalid mac address"),
        ],
    ],
)
def test__check_data(device_data, expected_exception):
    device = DeviceInterface()
    device.device_data = device_data
    with expected_exception:
        device._check_data()


@pytest.mark.parametrize(
    "input, expected",
    [
        [
            "data/device/device_in_1.json",
            {"mac": "ff-ff-ff-ff-ff-ff", "value": 145, "excess": 120},
        ],
        [
            {
                "mac": "aB-cD-eF-01-23-45",
                "type": "thermometer",
                "value": 145,
            },
            {
                "mac": "aB-cD-eF-01-23-45",
                "type": "thermometer",
                "value": 145,
            },
        ],
    ],
)
def test__read_device_data(input, expected):
    # can't check datetime.now() directly
    device = DeviceInterface()
    device._read_device_data(input)

    data = device.device_data
    assert isinstance(data["time_received"], datetime)
    data.pop("time_received")
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
                "type": "thermometer",
                "value": 145,
                "time_received": datetime(2022, 2, 14),
            },
            {
                "mac": "aB-cD-eF-01-23-45",
                "type": "thermometer",
                "value": 145,
                "time_received": datetime(2022, 2, 14),
            },
        ],
        [
            {
                "mac": "ff-ff-ff-ff-ff-ff",
                "excess": 120,
                "type": "thermometer",
                "excess2": 121,
                "excess3": 122,
                "value": 145,
                "excess4": 123,
                "excess5": 124,
                "time_received": datetime(2022, 2, 14),
            },
            {
                "mac": "ff-ff-ff-ff-ff-ff",
                "type": "thermometer",
                "value": 145,
                "time_received": datetime(2022, 2, 14),
            },
        ],
    ],
)
def test__trim_data(data, expected):
    device = DeviceInterface()
    device.device_data = data
    device._trim_data()
    assert data == expected
