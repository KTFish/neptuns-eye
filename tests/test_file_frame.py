import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from neptunseye.file_frame import FileFrame
from neptunseye.las_handler import LasHandler


class TestFileFrame(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.las_handler = LasHandler()
        self.file_frame = FileFrame(master=self.root, las_handler=self.las_handler)
        self.root.withdraw()

    def test_initialization(self):
        self.assertIsInstance(self.file_frame, FileFrame)

    def test_widgets_created(self):
        self.assertIsNotNone(self.file_frame.frame_lb)
        self.assertIsNotNone(self.file_frame.file_description_lb)
        self.assertIsNotNone(self.file_frame.import_file_btn)

    def test_widgets_positioning(self):
        self.assertEqual(self.file_frame.file_path_tbox.grid_info()["row"], 1)
        self.assertEqual(self.file_frame.file_path_tbox.grid_info()["column"], 0)
        self.assertEqual(self.file_frame.import_file_btn.grid_info()["row"], 1)

    @patch('tkinter.filedialog.askopenfilename')
    def test_open_file_dialog(self, mock_askopenfilename):
        mock_askopenfilename.return_value = '/path/to/file.las'
        self.file_frame.open_file_dialog()
        self.assertEqual(self.file_frame.file_path, '/path/to/file.las')

    # @patch('neptunseye.las_handler.LasHandler.load_file')
    # def test_load_file(self, mock_load_file):
    #     self.file_frame.file_path = '/path/to/file.las'
    #     self.file_frame.load_file()
    #     mock_load_file.assert_called_once()

    def test_update_file_path_tbox(self):
        self.file_frame.update_file_path_tbox('/new/path/to/file.las')
        self.assertEqual(self.file_frame.file_path_tbox.get("1.0", "end-1c"), '/new/path/to/file.las')

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
