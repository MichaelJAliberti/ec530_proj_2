import logging

from os.path import exists

logger = logging.getLogger(__name__)


def check_file(file_path, format):
    """Determine if file exists and is of correct format

    :param file_path: path to a file
    :type file_path: str
    :param format: file type (i.e. txt)
    :type format: str
    
    :return: true if valid, false if not
    :rtype: bool
    """
    if exists(file_path):
        if file_path.split(".")[-1] == format.removeprefix("."):
            return True
        else:
            logger.warning(f"{file_path} is not a {format} file")
            return False
    else:
        logger.warning(f"{file_path} does not exist")
        return False
