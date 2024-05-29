from preprocess.preprocess import prepare_data
from storage.save import write_las_file


def predict(df, model, save_las_path: str = None):

    test_features, test_labels = prepare_data(df, purpose="prediction")
    preds = model.predict(test_features)

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds, test_labels
