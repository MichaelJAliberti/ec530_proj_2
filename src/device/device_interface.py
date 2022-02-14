from datetime import datetime, timezone
import json


data_template = ["mac", "value"]


def check_mac_format(mac):
    pass


def read_from_device(file):
    """ Take in mac_address and readout_value of a given device

    :param file: path to a given device
    :type file: string
    ...
    :return: a dictionary of device data, UTC timestamp, and error codes
    :rtype: dictionary
    """

    with open(file) as f:
        device_data = json.load(f)
    if check_mac_format(device_data["mac"]):
        pass
    device_data["timestamp"] = datetime.now(timezone.utc)

    return device_data


def retrieve_db_info(mac_address):
    """ Look up device information given its mac_address

    :param mac_address: identifier for device
    :type mac_address: string
    ...
    :return: a dictionary of device information
    :rtype: dictionary
    """
    pass


if __name__ == "__main__":
    data = read_from_device("data/device.json")
    print(data)
