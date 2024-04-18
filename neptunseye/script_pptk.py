import pandas as pd
import pptk
import sys
import os
import numpy as np


def render_pptk(csv_path) -> None:

    print("Rendering point cloud using PPTK...")
    df = pd.read_csv(csv_path)
    print(csv_path)
    classified = df['classification'].values

    """
    Render a point cloud visualization using PPTK (Point Processing Toolkit).

    Reads a CSV file containing point cloud data from the specified path. The CSV
    file should have columns 'X', 'Y', 'Z' representing point coordinates and columns
    'red', 'green', 'blue' representing RGB color values normalized to the range [0, 1].
    The function renders the point cloud using PPTK, setting point size and color attributes.
    After rendering, the CSV file is removed from the filesystem.

    Args:
        csv_path (str): The path to the CSV file containing point cloud data.

    Returns:
        None
    """
  
    xyz = df[['X', 'Y', 'Z']].values
    rgb = df[['red', 'green', 'blue']].values / 65025  # Assuming the normal range of RGB is 0-255

    class_color_map = {
        0: [1.0, 1.0, 1.0],  # 0 never classified - white
        1: [0.0, 0.0, 0.0],  # 1 unclassified - black
        11: [0.0, 0.0, 1.0],  # 11 ground - blue
        13: [0.0, 0.5, 0.0],  # 13 vegetation - green
        15: [0.0, 1.0, 1.0],  # 15 building - cyan
        17: [0.5, 0.5, 0.5],  # 17 main road - gray
        19: [1.0, 0.0, 0.0],  # 19 power lines - red
        25: [0.6, 0.29, 0.0],  # 25 minor road - brown
    }

    # Ensure all classifications have a corresponding color
    max_class = max(class_color_map.keys())
    color_array = np.array([[1.0, 1.0, 1.0]] * (max_class + 1))
    for key, color in class_color_map.items():
        color_array[key] = color

    v = pptk.viewer(xyz)
    v.set(point_size=0.009)
    v.attributes(classified, rgb)  # RGB values should be normalized
    v.color_map(color_array, scale=[0, max_class])  # Ensure color map is used with the right scale

    os.remove(csv_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: script.py <path_to_csv>")
    csv_path = sys.argv[1]
    render_pptk(csv_path)