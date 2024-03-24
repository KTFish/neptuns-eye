import joblib
import laspy
import onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from sklearn.ensemble import RandomForestClassifier


def save_onnx(sklearn_model, output_file):

    initial_type = [('float_input', FloatTensorType([None, sklearn_model.n_features_]))]
    onnx_model = convert_sklearn(sklearn_model, initial_types=initial_type)

    onnx.save_model(onnx_model, output_file)
    print("Model RandomForestClassifier został zapisany w formacie ONNX pod nazwą:", output_file)

def save_joblib(model, filename):
    joblib.dump(model, filename=filename)

def write_las_file(df, new_classification, output_file_path):
    # Tworzenie nowego DataFrame z nową wartością classification
    df['classification'] = new_classification

    # Tworzenie nowego obiektu pliku LAS
    las = laspy.create(point_format=2)

    # Przypisanie danych z DataFrame do odpowiednich pól w pliku LAS
    for column in df.columns:
        if column in las.point_format.dimension_names:
            setattr(las, column, df[column].values)

    # Zapisanie pliku LAS
    las.write(output_file_path)

def test_save_onnx():
    model = RandomForestClassifier()
    save_joblib(model, "model.joblib")

if __name__ == "__main__":
    test_save_onnx()