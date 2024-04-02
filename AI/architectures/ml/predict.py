from preprocess.preprocess import prepare_data_prediction
from storage.save import write_las_file
from sklearn.metrics import accuracy_score


def predict(df, model, target_column="classification", sample_rate=0.1, random_state=42, save_las_path: str = None):
    """
    Use a trained machine learning model to make predictions on the provided DataFrame.

    Parameters:
    - df (DataFrame): The input DataFrame containing the dataset to be predicted.
    - model (object): The trained machine learning model object.
    - target_column (str): The name of the target column in the DataFrame. Default is "classification".
    - sample_rate (float): The fraction of samples to include in the prediction dataset.
    Should be between 0 and 1. Default is 0.1.
    - random_state (int): Controls the randomness of the data sampling. Default is 42.
    - save_las_path (str): The file path to save the predicted LAS file. Default is None.

    Returns:
    - array-like: An array containing the predicted labels.

    This function prepares the data for prediction, uses the trained model to make predictions, calculates the
    prediction accuracy, and optionally saves the predicted LAS file if a save path is provided.
    """
    test_features, test_labels = prepare_data_prediction(df, target_column, sample_rate=sample_rate,
                                                         random_state=random_state)
    preds = model.predict(test_features)
    accuracy = accuracy_score(test_labels, preds) * 100
    print(f"\nPredictions accuracy: {accuracy:.2f}%")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds
