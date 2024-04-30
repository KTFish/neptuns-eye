from storage.save import write_las_file
from sklearn.metrics import accuracy_score
from utils.preprocess import prepare_data_prediction


def predict(df, model, target_column="classification", sample_rate=0.1, random_state=42, save_las_path: str = None):

    test_features, test_labels = prepare_data_prediction(df, target_column, sample_rate=sample_rate,
                                                         random_state=random_state)

    preds = model.predict(test_features)
    print(f"\nPredictions accuracy: {accuracy_score(test_labels, preds):.2f}")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds
