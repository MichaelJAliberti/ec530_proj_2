import pytest

from src.utils.file import check_file


@pytest.mark.parametrize(
    "file_path, format, expected",
    [
        [
            "data/device/device_in_1.json",
            ".json",
            True,
        ],
        [
            "data/device/device_in_2.txt",
            "txt",
            True,
        ],
        [
            "data/device/device_in_2.txt",
            ".json",
            False,
        ],
        [
            "data/device/no_file.json",
            ".json",
            False,
        ],
    ],
)
def test_check_file(file_path, format, expected):
    assert check_file(file_path, format) == expected
