import laspy

class LasHandler(object):

    __file_path: str

    def __init__(self, file_path: str) -> None:

        self.__file_path = file_path
        try:
            self.las = laspy.read(self.__file_path)
        except FileNotFoundError:
            print("Las file not found!", self.__file_path)