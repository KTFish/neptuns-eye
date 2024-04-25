import unittest
from unittest.mock import patch, MagicMock
import customtkinter
from neptunseye.classification_frame import ClassificationFrame
from neptunseye.las_handler import LasHandler


class TestClassificationFrame(unittest.TestCase):

    def setUp(self):
        customtkinter.set_appearance_mode("System")  # Required because customtkinter needs an appearance mode
        customtkinter.set_default_color_theme("blue")  # Set a default theme
        self.root = customtkinter.CTk()  # Create a main window for the tests
        self.las_handler = LasHandler()
        self.las_handler.file_loaded = True  # Assume file is loaded for most tests
        self.frame = ClassificationFrame(master=self.root, las_handler=self.las_handler)
        self.root.withdraw()  # Hide the main window

    def test_initialization(self):
        self.assertIsInstance(self.frame, ClassificationFrame)
        self.assertIsNotNone(self.frame.model_cbox)
        self.assertIsNotNone(self.frame.classification_btn)

    # @patch('customtkinter.CTkMessagebox')
    # def test_classification_not_started_if_file_not_loaded(self, mock_messagebox):
    #     self.frame.las_handler.file_loaded = False
    #     result = self.frame.classification_event()
    #     mock_messagebox.assert_called_once_with(title="File not loaded", message=any, icon="cancel")
    #     self.assertFalse(result)
    #
    # @patch('threading.Thread.start')
    # @patch('customtkinter.CTkMessagebox')
    # def test_classification_started(self, mock_messagebox, mock_thread_start):
    #     self.frame.classification_event()
    #     mock_thread_start.assert_called_once()
    #     mock_messagebox.assert_called()
    #
    # @patch('neptunseye.classification_utils.ClassificationUtils.load_joblib')
    # def test_run_classification(self, mock_load_joblib):
    #     model_mock = MagicMock()
    #     mock_load_joblib.return_value = model_mock
    #     model_mock.predict.return_value = [0, 1, 2]
    #     self.frame.run_classification()
    #     self.assertEqual(self.las_handler.data_frame['classification'].tolist(), [0, 1, 2])
    #     self.assertTrue(self.frame.classification_btn.state() == customtkinter.NORMAL)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
