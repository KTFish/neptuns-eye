import pandas as pd
import pptk
import sys
import os


def render_pptk(csv_path) -> None:
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
    print("Rendering point cloud using PPTK...")
    df = pd.read_csv(csv_path)
    print(csv_path)
    classified = df.classification
    xyz = df[['X', 'Y', 'Z']].values
    rgb = df[['red', 'green', 'blue']].values / 65025

    colors = [(255, 0, 0),
              (0, 0, 255),
              (255, 255, 0),
              (128, 0, 128),
              (0, 128, 0),
              (255, 165, 0),
              (0, 255, 255),
              (255, 192, 203)]

    scaled_colors = [(r / 255.0, g / 255.0, b / 255.0, 1.0) for r, g, b in colors]

    v = pptk.viewer(xyz)
    v.set(point_size=0.009)
    v.attributes(classified, rgb)
    v.color_map(c=scaled_colors)

    os.remove(csv_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    csv_path = sys.argv[1]
    render_pptk(csv_path)