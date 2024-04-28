import os
import pytest
import pandas as pd

import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from neptunseye.las_handler import LasHandler

LAS_FILES = {
    "WMII_CLASS": "./neptunseye/resources/data/WMII_CLASS.las",  # Faculty of Mathematics and Computer Science
    "Kortowo": "./neptunseye/resources/data/Kortowo.las",  # University Campus
    'USER_AREA': "./neptunseye/resources/data/USER_AREA.las"  # Słoneczna street
}

EXPECTED_POINT_COUNT = {
    'WMII_CLASS': 6_375_629,
    "Kortowo": 122_973_708,
    "USER_AREA": 6_215_173
}


@pytest.mark.parametrize("file_name, file_path", LAS_FILES.items())
def test_file_existence(file_name, file_path):
    assert os.path.exists(file_path), f"{file_name} file does not exist."


@pytest.fixture(params=LAS_FILES.keys(), scope="session")
def las_data(request):
    file_path = LAS_FILES[request.param]
    df = LasHandler(file_path).create_dataframe()
    return df, request.param


def test_df_not_empty(las_data):
    df, file_name = las_data
    assert len(df) > 0, f"{file_name} Data Frame is empty."


def test_df_type(las_data):
    df, file_name = las_data
    assert isinstance(df, pd.DataFrame), f"{file_name} Data Frame has wrong type."


def test_df_columns(las_data):
    df, file_name = las_data
    expected_cols = ['X', 'Y', 'Z', "red", "green", "blue", 'classification']
    for col in expected_cols:
        assert col in df.columns, f"{file_name} missing column '{col}'."


def test_point_count(las_data):
    df, file_name = las_data
    assert len(df) == EXPECTED_POINT_COUNT[file_name], f"WMII_CLASS: Wrong number of points: {len(df)} instead of {EXPECTED_POINT_COUNT[file_name]}."
