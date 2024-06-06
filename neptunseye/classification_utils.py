import joblib
import sklearn

class ClassificationUtils:

    @staticmethod
    def prepare_data_prediction(df, target_column="classification"):
        """
        Prepare prediction data by keeping specified columns and separating features from the target.

        Parameters:
        df (DataFrame): Input data frame.
        target_column (str): Column name to be used as the target variable. Default is "classification".

        Returns:
        tuple: Features and target labels for prediction.
        """
        columns_to_keep = ["X", "Y", "Z", "intensity", "return_number", "number_of_returns",
                           "scan_direction_flag", "edge_of_flight_line", "scan_angle_rank",
                           "red", "green", "blue", target_column]

        df = df[columns_to_keep]
        test_features = df.drop(columns=[target_column])
        test_labels = df[target_column]

        return test_features, test_labels

    @staticmethod
    def load_joblib(joblib_file_path):
        model = joblib.load(joblib_file_path)
        if model:
            return model
        else:
            return None
