import json
import logging
import re

from datetime import datetime, timezone
from src.utils.file import check_file

logger = logging.getLogger(__name__)


class DeviceInterface:
    def __init__(self):
        self.required_fields = ["mac", "type", "value", "time_received"]
        self.device_data = {}

    @classmethod
    def create_from_data(cls, data):
        """Creates a DeviceInterface object from a given set of data and
            verifies the integrity of said data

        :param data: information from a device
        :type data: dict
        ...
        :return: a DeviceInterface built with input data
        :rtype: DeviceInterface
        """
        interface = DeviceInterface()
        interface._read_device_data(device=data)
        interface._check_data()

        return interface

    @classmethod
    def fully_augmented(cls, data):
        """Creates a DeviceInterface object from a given set of data,
            verifies the integrity of said data, and augments data

        :param data: information from a device
        :type data: dict
        ...
        :return: a DeviceInterface built with input data
        :rtype: DeviceInterface
        """
        interface = DeviceInterface()
        interface._read_device_data(device=data)
        interface._check_data()
        interface._trim_data()
        interface._retrieve_db_data()

        return interface

    def _check_data(self):
        """Check if stored device_data has valid format

        :raise: ValueError
        """
        self._check_data_fields()
        self._check_data_mac()

    def _check_data_fields(self):
        """Determine if data has all required fields

        :raise: ValueError if any missing fields
        """
        missing_fields = []
        [
            missing_fields.append(key)
            for key in self.required_fields
            if key not in self.device_data
        ]
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.warning(error_msg)
            raise ValueError(error_msg)

    def _check_data_mac(self):
        """Checks mac address in device_data, determine if format is valid

        :raise: ValueError if mac address is invalid
        """
        mac = self.device_data.get("mac")
        if not isinstance(mac, str) or not bool(
            re.match("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac)
        ):
            error_msg = f"Invalid mac address: {self.device_data['mac']}"
            logger.warning(error_msg)
            raise ValueError(error_msg)

    def _read_device_data(self, device):
        """Read and store all data from a given device and timestamp recording

        :param device: path to json file or dictionary containing device info
        :type device: string or dict
        """
        reader = get_device_reader(device)
        self.device_data = reader(device)
        self.device_data["time_received"] = datetime.now(timezone.utc)

    def _retrieve_db_data(self):
        """Look up device information in database using mac_address and add data to
        device_data
        """
        if self.check_data_format():
            self.device_data.update({})

    def _trim_data(self):
        """Removes unexpected data from device stream"""
        excess_keys = [
            key for key in self.device_data if key not in self.required_fields
        ]
        [self.device_data.pop(field) for field in excess_keys]


def get_device_reader(device):
    """Factory function to read device data from different input types

    :param device: input data from some device
    :type device: str or dict
    """
    if isinstance(device, str):
        return _read_from_file
    elif isinstance(device, dict):
        return _read_from_dict
    else:
        logger.error(f"Invalid device type {type(device)}, reader failed")
        raise ValueError(device)


def _read_from_file(device):
    """Read device data from a json file

    :param device: path to a json file
    :type device: str
    """
    if check_file(device, "json"):
        with open(device) as f:
            return json.load(f)


def _read_from_dict(device):
    """Ingest device data from a dictionary

    :param device: dictionary of device data
    :type device: dict
    """
    return device
