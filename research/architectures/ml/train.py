from preprocess.preprocess import prepare_data_training
from storage.save import save_joblib
from sklearn.metrics import accuracy_score
import pandas as pd


def train_ml(df: pd.DataFrame,
             clf,
             target_column="classification",
             test_size=0.2,
             test_acc: bool = False,
             save_path: str = None):
    """
    Train a machine learning classifier on a given DataFrame and optionally evaluate and save the model.
    Args:
        df (pandas.DataFrame): The input data for training.
        clf (sklearn.base.BaseEstimator): The classifier to be trained.
        target_column (str, optional): The name of the target column in the DataFrame. Defaults to "classification".
        test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
        test_acc (bool, optional): If True, evaluates and prints the test accuracy after training. Defaults to False.
        save_path (str, optional): The file path to save the trained model. If None, the model is not saved.
    Returns:
        tuple: The trained classifier and the predicted labels on the test set (if test_acc is True), otherwise None.
    """
    X_train, X_test, y_train, y_test = prepare_data_training(df,
                                                             target_column,
                                                             test_size=test_size)

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
