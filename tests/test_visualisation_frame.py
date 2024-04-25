import unittest
from unittest.mock import patch, MagicMock
import customtkinter
from neptunseye.visualisation_frame import VisualisationFrame
from neptunseye.las_handler import LasHandler


class TestVisualisationFrame(unittest.TestCase):

    def setUp(self):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        self.root = customtkinter.CTk()
        self.las_handler = LasHandler()
        self.las_handler.file_loaded = True
        self.frame = VisualisationFrame(master=self.root, las_handler=self.las_handler)
        self.root.withdraw()

    def test_initialization(self):
        self.assertIsInstance(self.frame, VisualisationFrame)
        self.assertIsNotNone(self.frame.method_cbox)
        self.assertIsNotNone(self.frame.render_btn)

    # @patch('customtkinter.CTkMessagebox')
    # def test_render_not_started_if_file_not_loaded(self, mock_messagebox):
    #     self.frame.las_handler.file_loaded = False
    #     self.frame.render_event()
    #     mock_messagebox.assert_called_once_with(title="File not loaded", message=any, icon="cancel")
    #
    # @patch('threading.Thread.start')
    # @patch('customtkinter.CTkMessagebox')
    # def test_render_started_with_plotly(self, mock_messagebox, mock_thread_start):
    #     self.frame.rendering_method = 'plotly'
    #     self.frame.render_event()
    #     mock_thread_start.assert_called_once()
    #     mock_messagebox.assert_called()
    #
    # @patch('os.environ.get')
    # @patch('subprocess.run')
    # def test_render_pptk(self, mock_run, mock_get):
    #     mock_get.return_value = '/fakepath'
    #     self.frame.rendering_method = 'PPTools'
    #     with patch('threading.Thread.start', new=MagicMock()):
    #         self.frame.render_event()
    #     mock_run.assert_called_once()

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
