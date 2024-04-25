import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from neptunseye.las_handler import LasHandler
import laspy


class TestLasHandler(unittest.TestCase):
    def setUp(self):
        self.file_path = 'valid_path.las'
        self.invalid_file_path = 'invalid_path.las'
        self.las_handler = LasHandler(self.file_path)

    @patch('laspy.read')
    def test_successful_file_load(self, mock_read):
        mock_read.return_value = MagicMock(spec=laspy.LasData)
        handler = LasHandler(self.file_path)
        self.assertTrue(handler.file_loaded)

    @patch('laspy.read', side_effect=FileNotFoundError("File not found"))
    def test_file_not_found(self, mock_read):
        handler = LasHandler(self.invalid_file_path)
        self.assertFalse(handler.file_loaded)
        self.assertIsInstance(handler.exception, FileNotFoundError)

    # def test_create_dataframe(self):
    #     mock_las = MagicMock(spec=laspy.LasData)
    #     mock_las.point_format.dimensions = [MagicMock(name='X'), MagicMock(name='Y'), MagicMock(name='Z')]
    #     mock_las.X = np.array([1, 2, 3])
    #     mock_las.Y = np.array([4, 5, 6])
    #     mock_las.Z = np.array([7, 8, 9])
    #     self.las_handler.las = mock_las
    #
    #     df = self.las_handler.create_dataframe()
    #     self.assertIsInstance(df, pd.DataFrame)
    #     self.assertEqual(list(df.columns), ['X', 'Y', 'Z'])
    #     self.assertEqual(len(df), 3)

    def test_unique_classes(self):
        df = pd.DataFrame({'classification': [1, 2, 2, 3]})
        self.las_handler.data_frame = df
        unique_classes = self.las_handler.unique_classes
        self.assertListEqual(unique_classes, [1, 2, 3])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
