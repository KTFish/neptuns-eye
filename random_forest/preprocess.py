import laspy
from sample_points import sample_las_file
import numpy as np


def split_las_file(file_path, train_ratio=0.8):
    las_file = laspy.read(file_path)
    total_points = len(las_file.points)
    indices = np.arange(total_points)
    np.random.shuffle(indices)

    train_size = int(total_points * train_ratio)
    train_indices = indices[:train_size]
    test_indices = indices[train_size:]

    train_points = las_file.points[train_indices]
    test_points = las_file.points[test_indices]

    train_las = laspy.create(point_format=las_file.header.point_format, file_version=las_file.header.version)
    test_las = laspy.create(point_format=las_file.header.point_format, file_version=las_file.header.version)

    train_las.points = train_points
    test_las.points = test_points

    base_file_name = file_path.replace(".las", "")
    train_file_name = f"{base_file_name}_TRAIN.las"
    test_file_name = f"{base_file_name}_TEST.las"

    train_las.write(train_file_name)
    test_las.write(test_file_name)

    return train_file_name, test_file_name


def preprocess_pipeline(sample_rate=0.01):
    if sample_rate is False:
        file_path = '../data/WMII_CLASS.las'
    else:
        file_path = sample_las_file('../data/WMII_CLASS.las', sample_rate=sample_rate)
        print(f"[INFO] Files have been preprocessed with sample rate {sample_rate}")
    train_file, test_file = split_las_file(file_path)


if __name__ == '__main__':
    preprocess_pipeline(sample_rate=False)
