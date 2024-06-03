import os
import sys


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both dev and PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)