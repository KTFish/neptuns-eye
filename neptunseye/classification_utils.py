import joblib
from sklearn.preprocessing import MinMaxScaler


class ClassificationUtils:

    @staticmethod
    def prepare_data_prediction(df, columns_to_keep=None):

        if columns_to_keep is None:
            columns_to_keep = ["X", "Y", "Z", "intensity", "number_of_returns", "classification", "red", "green",
                               "blue"]

        df = df[columns_to_keep]
        test_features = df.drop(columns=["classification"])
        test_features = MinMaxScaler().fit_transform(test_features)
        test_labels = df["classification"]

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