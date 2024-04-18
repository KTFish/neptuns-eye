from preprocess.preprocess import prepare_data_prediction
from storage.save import write_las_file
from sklearn.metrics import accuracy_score


def predict(df, model, target_column="classification", save_las_path: str = None):

    test_features, test_labels = prepare_data_prediction(df, target_column)
    preds = model.predict(test_features)
    accuracy = accuracy_score(test_labels, preds) * 100
    print(f"\nPredictions accuracy: {accuracy:.2f}%")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds
