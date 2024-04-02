import joblib
import laspy
import onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import RandomForestClassifier


def save_joblib(model, filename):
    joblib.dump(model, filename=filename)


def save_onnx(sklearn_model, output_file):

    initial_type = [('float_input', FloatTensorType([None, sklearn_model.n_features_]))]
    onnx_model = convert_sklearn(sklearn_model, initial_types=initial_type)

    onnx.save_model(onnx_model, output_file)
    print("Model RandomForestClassifier został zapisany w formacie ONNX pod nazwą:", output_file)


def write_las_file(df, new_classification, output_file_path):
    """
    Write data from a pandas DataFrame to a LAS (Log ASCII Standard) file with updated classification values.

    Parameters:
    - df (DataFrame): The pandas DataFrame containing the data to be written to the LAS file.
    - new_classification (array-like): An array-like object containing the new classification values to be assigned.
    - output_file_path (str): The path to save the output LAS file.

    Returns:
    - None

    Note:
    The function modifies the 'classification' column of the DataFrame with the provided new_classification values
    and writes the data to a LAS file specified by the output_file_path.
    """
    df['classification'] = new_classification

    las = laspy.create(point_format=2)

    for column in df.columns:
        if column in las.point_format.dimension_names:
            setattr(las, column, df[column].values)

    las.write(output_file_path)


def test_save_onnx():
    model = RandomForestClassifier()
    save_joblib(model, "model.joblib")


if __name__ == "__main__":
    test_save_onnx()
