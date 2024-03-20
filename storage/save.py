import joblib
import laspy


def save_model(model, filename):
    joblib.dump(model, filename=filename)


def write_las_file(df, output_file_path, new_classification):
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
