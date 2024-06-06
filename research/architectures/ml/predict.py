from preprocess.preprocess import prepare_data_prediction
from storage.save import write_las_file
from sklearn.metrics import accuracy_score


def predict(df, model, target_column="classification", save_las_path: str = None):
    """
    Make predictions on a given DataFrame using a specified model, and optionally save the results to a LAS file.
    Args:
        df (pandas.DataFrame): The input data for prediction.
        model (sklearn.base.BaseEstimator): trained model.
        target_column (str, optional): The name of the target column in the DataFrame. Defaults to "classification".
        save_las_path (str, optional): The file path to save the predictions as a LAS file.
    Returns:
        numpy.ndarray: The predicted labels.
    """
    test_features, test_labels = prepare_data_prediction(df, target_column)
    preds = model.predict(test_features)
    accuracy = accuracy_score(test_labels, preds) * 100
    print(f"\nPredictions accuracy: {accuracy:.2f}%")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds
