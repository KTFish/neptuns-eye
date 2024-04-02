from preprocess.preprocess import prepare_data_training
from storage.save import save_joblib
from sklearn.metrics import accuracy_score
import pandas as pd


def train_ml(df: pd.DataFrame,
             clf,
             target_column="classification",
             sample_rate=0.1,
             test_size=0.2,
             random_state=42,
             test_acc: bool = False,
             save_path: str = None):
    """
    Train a machine learning model using the provided DataFrame and specified classifier.

    Parameters:
    - df (DataFrame): The input DataFrame containing the dataset.
    - clf (object): The classifier object to be trained.
    - target_column (str): The name of the target column in the DataFrame. Default is "classification".
    - sample_rate (float): The fraction of samples to include in the training dataset.
    Should be between 0 and 1. Default is 0.1.
    - test_size (float): The proportion of the dataset to include in the test split.
    Should be between 0 and 1. Default is 0.2.
    - random_state (int): Controls the randomness of the data splitting. Default is 42.
    - test_acc (bool): Whether to calculate and print the test accuracy after training. Default is False.
    - save_path (str): The file path to save the trained model. Default is None.

    Returns:
    - Tuple: A tuple containing the trained classifier object and the predicted labels if test_acc is True,
    else only the trained classifier.

    This function prepares the data for training, fits the classifier to the training data, and optionally calculates
    and prints the test accuracy. If specified, the trained model can be saved to a file.
    """
    X_train, X_test, y_train, y_test = prepare_data_training(df,
                                                             target_column,
                                                             sample_rate=sample_rate,
                                                             test_size=test_size,
                                                             random_state=random_state)

    print(f"\n[INFO] Training with {clf.__class__.__name__}:")
    clf.fit(X_train, y_train)
    y_pred = None

    if test_acc:
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        print(f"\nTest accuracy: {accuracy:.2f}%")

    if save_path is not None:
        save_joblib(clf, save_path)
    print("Training done!")

    return clf, y_pred
