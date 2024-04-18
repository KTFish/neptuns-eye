import joblib
import laspy
from sklearn.ensemble import RandomForestClassifier


def save_joblib(model, filename):
    joblib.dump(model, filename=filename)


def write_las_file(df, new_classification, output_file_path):

    df['classification'] = new_classification

    las = laspy.create(point_format=2)

    for column in df.columns:
        if column in las.point_format.dimension_names:
            setattr(las, column, df[column].values)

    las.write(output_file_path)
