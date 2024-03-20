from sklearn.metrics import accuracy_score


def predict(test_features, test_labels, train_model):
    y_pred = train_model.predict(test_features)

    print(f"y_test shape: {test_labels.shape}, y_pred shape: {y_pred.shape}")
    print(f"y_test type: {type(test_labels)}, y_pred type: {type(y_pred)}")

    accuracy = accuracy_score(test_labels, y_pred)
    print(f"\nAccuracy: {accuracy:.2f}")

    return y_pred


def prepare_data_prediction(df, sample_rate=0.1, random_state=None, columns_to_delete=None):
    if columns_to_delete is None:
        columns_to_delete = ['synthetic', 'key_point', 'withheld', 'user_data', 'point_source_id']

    df_cleaned = df.drop(columns=columns_to_delete)

    df_sampled = df_cleaned.sample(frac=sample_rate, random_state=random_state)

    return df_sampled

