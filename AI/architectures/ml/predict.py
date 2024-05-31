from preprocess.preprocess import prepare_data_prediction
from storage.save import write_las_file
from sklearn.metrics import accuracy_score


def predict(df, model, target_column="classification", save_las_path: str = None):
    """
    Make predictions using a pre-trained model and optionally save the results in a LAS file.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input data with features and the target column.

    model : sklearn.base.BaseEstimator
        Pre-trained model for predictions.

    target_column : str
        Name of the target column in `df`.

    save_las_path : str
        Path to save predictions in LAS format. If None, results are not saved.

    Returns:
    --------
    preds : numpy.ndarray
        Predicted labels.

    Side Effects:
    -------------
    - Prints prediction accuracy.
    - Saves predictions to a LAS file if `save_las_path` is provided.
    """

    test_features, test_labels = prepare_data_prediction(df, target_column)
    preds = model.predict(test_features)
    accuracy = accuracy_score(test_labels, preds) * 100
    print(f"\nPredictions accuracy: {accuracy:.2f}%")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds
