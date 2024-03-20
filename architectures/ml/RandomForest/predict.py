from storage.save import write_las_file
from sklearn.metrics import accuracy_score
from utils.preprocess import prepare_data_prediction


def predict(df, model, target_column="classification", sample_rate=0.1, random_state=42, save_las_path: str = None):
    # Przygotowanie danych do predykcji
    test_features, test_labels = prepare_data_prediction(df, target_column, sample_rate=sample_rate,
                                                         random_state=random_state)

    # Dokonanie predykcji przy użyciu modelu
    preds = model.predict(test_features)
    print(f"\nPredictions accuracy: {accuracy_score(test_labels, preds):.2f}")

    if save_las_path is not None:
        write_las_file(test_features, preds, save_las_path)
    return preds


# def predict(trained_modell):
#     y_pred = train_model.predict(test_features)
#
#     print(f"y_test shape: {test_labels.shape}, y_pred shape: {y_pred.shape}")
#     print(f"y_test type: {type(test_labels)}, y_pred type: {type(y_pred)}")
#
#     accuracy = accuracy_score(test_labels, y_pred)
#     print(f"\nAccuracy: {accuracy:.2f}")
#
#     return y_pred
