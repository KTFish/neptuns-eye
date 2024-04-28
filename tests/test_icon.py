import os


def test_icon():
    icon_path = r"./neptunseye/resources/neptuns-eye-logo.ico"
    assert os.path.exists(icon_path)
