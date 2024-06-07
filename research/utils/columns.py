import laspy


def print_columns_names(las_file_path):
    """
    Print the names of the columns in a LAS file.

    Args:
        las_file_path (str): The path to the LAS file.
    """
    las = laspy.read(las_file_path)
    column_names = [dimension.name for dimension in las.point_format.dimensions]
    print(column_names)

