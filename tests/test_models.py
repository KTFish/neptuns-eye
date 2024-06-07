import os
import sys
from time import time
import pytest
import joblib
from pathlib import Path
from sklearn.metrics import accuracy_score

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from neptunseye.classification_utils import ClassificationUtils
from neptunseye.las_handler import LasHandler

TIME_LIMIT = 30
ACCURACY_THRESHOLD = 0.8
DATA_PATH = Path('neptunseye', 'resources', 'data', 'WMII_CLASS.las')
MODELS_PATH = Path('neptunseye', 'resources', 'models')

MODELS = ['AdaBoostClassifier731.joblib',
          'BaggingClassifier650.joblib',
          'ExtraTreesClassifier851.joblib',
          'GradientBoostingClassifier653.joblib',
          'HistGradientBoostingClassifier720.joblib',
          'KNeighborsClassifier795.joblib',
          'RandomForestClassifier851.joblib',
          'StackingClassifier673.joblib',
          'VotingClassifier751.joblib']


@pytest.fixture(scope="session")
def test_data():
    """Fixture to load and prepare test data only once per test session, with cleanup."""
    df = LasHandler(str(DATA_PATH)).create_dataframe()
    test_data = ClassificationUtils.prepare_data_prediction(df)
    yield test_data
    del df, test_data  # Explicit cleanup to free memory if necessary


@pytest.fixture(params=MODELS)
def model_path(request):
    """ Fixture to generate paths to model files based on the model filenames list. """
    return MODELS_PATH / request.param


def test_joblib_presence(model_path):
    """ Test to ensure that each model file exists at the specified path. """
    assert model_path.exists(), f"Model file {model_path} not available locally."


@pytest.fixture
def predictions(model_path, test_data):
    """Fixture to perform predictions, measuring time taken and returning predictions."""
    model = ClassificationUtils.load_joblib(model_path)
    X_test, _ = test_data
    start = time()
    y_pred = model.predict(X_test)
    end = time()
    duration = end - start
    return y_pred, duration


def test_model_speed(predictions):
    """Test to ensure that model predictions are made within a specified time limit."""
    _, duration = predictions
    assert duration <= TIME_LIMIT, f"Prediction time exceeded time limit. Limit: {TIME_LIMIT}s, Actual: {duration:.2f}s."


def test_model_accuracy(predictions, test_data):
    """Test to ensure that the model's predictions meet accuracy standards."""
    y_pred, _ = predictions
    _, y_test = test_data
    accuracy = accuracy_score(y_test, y_pred)
    assert accuracy >= ACCURACY_THRESHOLD, f"Model accuracy {accuracy * 100:.2f}% is below the threshold of {ACCURACY_THRESHOLD * 100}%."

# TODO: Model files should be load from a remote source for example AWS bucket
