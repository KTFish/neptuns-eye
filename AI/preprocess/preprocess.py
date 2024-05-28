from sklearn.model_selection import train_test_split


def prepare_data_training(df, test_size=0.2, random_state=42, keep_colors=True):

    columns_to_keep = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns",
                       "edge_of_flight_line", "classification", "scan_angle_rank"]

    if keep_colors:
        columns_to_keep.append("grayscale")

    print(columns_to_keep)

    df = df[columns_to_keep]
    x = df.drop(columns=["classification"])
    y = df["classification"]

    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_prediction(df, keep_colors=True):

    columns_to_keep = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns",
                       "edge_of_flight_line", "classification", "scan_angle_rank"]

    if keep_colors:
        columns_to_keep.append("grayscale")

    print(columns_to_keep)

    df = df[columns_to_keep]
    test_features = df.drop(columns=["classification"])
    test_labels = df["classification"]

    return test_features, test_labels
