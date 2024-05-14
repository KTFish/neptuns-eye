from sklearn.model_selection import train_test_split


def prepare_data_training(df, target_column="classification", test_size=0.2, random_state=42):
    """
        Split data into training and test sets by keeping specified columns and using specified target.
    """
    columns_to_keep = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns",
                       "scan_direction_flag", "edge_of_flight_line", "scan_angle_rank",
                       "red", "green", "blue", target_column]

    # Usuwamy wszystkie kolumny, które nie są w liście columns_to_keep
    df = df[columns_to_keep]

    # Rozdzielamy kolumny na zmienne niezależne i zmienną docelową
    x = df.drop(columns=[target_column])
    y = df[target_column]

    # Dzielimy dane na zestawy treningowe i testowe
    return train_test_split(x, y, test_size=test_size, random_state=random_state)


def prepare_data_prediction(df, target_column="classification"):
    """
        Prepare prediction data by keeping specified columns and separating features from the target.
    """
    columns_to_keep = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns",
                       "scan_direction_flag", "edge_of_flight_line", "scan_angle_rank",
                       "red", "green", "blue", target_column]

    # Usuwamy wszystkie kolumny, które nie są w liście columns_to_keep
    df = df[columns_to_keep]

    # Rozdzielamy kolumny na zmienne niezależne i zmienną docelową
    test_features = df.drop(columns=[target_column])
    test_labels = df[target_column]

    return test_features, test_labels
