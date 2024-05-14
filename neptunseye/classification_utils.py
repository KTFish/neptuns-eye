import joblib


class ClassificationUtils:

    @staticmethod
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

    @staticmethod
    def load_joblib(joblib_file_path):
        model = joblib.load(joblib_file_path)
        if model:
            print("Model successfully loaded from the file.")
            return model
        else:
            print("Failed to load the model from the file.")
            return None