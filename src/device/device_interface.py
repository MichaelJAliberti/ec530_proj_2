import json
import logging
import re

from datetime import datetime, timezone
from src.utils.file import check_file

logger = logging.getLogger(__name__)


class DeviceInterface:
    def __init__(self):
        self.require_fields = ["mac", "timestamp", "value"]
        self.device_data = {}

    def check_data_format(self):
        """Check if stored device_data has valid format

        :return: true if valid, false if not
        :rtype: bool
        """
        return self._check_data_fields() and self._check_data_mac_format()

    def _check_data_fields(self):
        """Determine if data has all required fields

        :return: true if valid, false if not
        :rtype: bool
        """
        missing_fields = []
        [
            missing_fields.append(key)
            for key in self.data_template
            if key not in self.device_data
        ]
        if not missing_fields:
            return True
        else:
            logger.warning(f"Missing required fields: {missing_fields.join(', ')}")
            return False

    def _check_data_mac_format(self):
        """Checks mac address in device_data, determine if format is valid

        :return: true if valid, false if not
        :rtype: bool
        """
        mac = self.device_data.get("mac")
        if isinstance(mac, str) and bool(
            re.match("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac)
        ):
            return True
        else:
            logger.warning(f"Invalid mac address: {self.device_data['mac']}")
            return False

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
        excess_keys = [key for key in self.device_data if key not in self.data_template]
        [self.device_data.pop(field) for field in excess_keys]


def get_device_reader(device):
    if isinstance(device, str):
        return _read_from_file
    elif isinstance(device, dict):
        return _read_from_dict
    else:
        logger.error(f"Invalid device type {type(device)}, reader failed")
        raise ValueError(device)


def _read_from_file(device):
    if check_file(device, "json"):
        with open(device) as f:
            return json.load(f)


def _read_from_dict(device):
    return device
