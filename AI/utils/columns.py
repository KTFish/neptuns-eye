import laspy


def print_columns_names(las_file_path):
    """
    Print the names of the columns (dimensions) in a LAS file.
    Parameters:
    -----------
    las_file_path : str
        Path to the LAS file.
    Side Effects:
    -------------
    - Prints the names of the columns in the LAS file.
    """
    las = laspy.read(las_file_path)
    column_names = [dimension.name for dimension in las.point_format.dimensions]
    print(column_names)
