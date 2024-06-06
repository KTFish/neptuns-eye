import os
import sys


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both dev and PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_config(file_path, *args):
    """
    Get a specific setting from the configuration file.

    Args:
        file_path (str): The path to the configuration file.
        *args (str): Two arguments specifying the section and option in the configuration file.

    Returns:
        str: The value of the specified setting from the configuration file.
    """
    import configparser
    config = configparser.ConfigParser()
    config.read(file_path)
    return config[args[0]][args[1]].strip('"')
