import laspy


def print_columns_names(las_file_path):
    las = laspy.read(las_file_path)
    column_names = [dimension.name for dimension in las.point_format.dimensions]
    print(column_names)
