from datetime import datetime, timezone
import json
import logging
import re


data_template = ["mac", "value"]


def check_mac_format(mac):
    """Take in mac_address, determine if its format is valid

    :param mac: mac address for a device
    :type mac: string
    ...
    :return: true if valid, false if not
    :rtype: bool
    """
    return bool(re.match("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac))


def check_valid_data(device_data):
    """Take in mac_address, determine if its format is valid

    :param device_data: mac address for a device
    :type device_data: dictionary
    ...
    :return: true if valid, false if not
    :rtype: bool
    """
    if not all([data_type in device_data for data_type in data_template]):
        logging.warning("Insufficient data fields")
        return False
    if not check_mac_format(device_data["mac"]):
        logging.warning(f"Invalid mac address: {device_data['mac']}")
        return False

    return True


def read_from_device(device):
    """Take in mac_address and readout_value of a given device

    :param device: path to file for a given device
    :type device: string
    ...
    :return: a dictionary of device data, UTC timestamp, and error codes
    :rtype: dictionary
    """
    with open(device) as f:
        device_data = json.load(f)
    if not check_valid_data(device_data):
        return {}
    trim_data(device_data)
    device_data["timestamp"] = datetime.now(timezone.utc)

    return device_data


def retrieve_db_data(mac_address):
    """Look up device information given its mac_address

    :param mac_address: identifier for device
    :type mac_address: string
    ...
    :return: a dictionary of device information
    :rtype: dictionary
    """
    pass


def trim_data(device_data):
    """Removes unnecessary data from device stream

    :param mac_address: identifier for device
    :type mac_address: string
    """
    excess_fields = [key for key in device_data if key not in data_template]
    [device_data.pop(field) for field in excess_fields]


if __name__ == "__main__":
    data = read_from_device("data/device.json")
    print(data)
