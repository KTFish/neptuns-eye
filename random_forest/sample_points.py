import laspy
import numpy as np


def sample_las_file(file_path, sample_rate=0.01):
    input_las = laspy.read(file_path)
    total_points = len(input_las.points)
    sample_size = int(total_points * sample_rate)

    indices = np.random.choice(total_points, sample_size, replace=False)
    sampled_points = input_las.points[indices]

    output_las = laspy.create(point_format=input_las.header.point_format, file_version=input_las.header.version)
    output_las.points = sampled_points

    new_file_name = file_path.replace(".las", "_LIGHT.las")
    output_las.write(new_file_name)
    return new_file_name
