from storage.load import read_las_file
import os

# TODO: Uncomment when pytorch will be used
# import torch
# device = "cuda" if torch.cuda.is_available() else "cpu"
# from storage.load import read_las_file
# from pathlib import Path

# WEIGHTS AND BIASES

# DIRECTORY PATHS

base_path = os.path.dirname(os.path.abspath(__file__))

wmii = read_las_file(os.path.join(base_path, "data/train/WMII_CLASS.las"))
user_area = read_las_file(os.path.join(base_path, "data/test/USER_AREA.las"))
# kortowo = read_las_file(os.path.join(base_path, "data/test/Kortowo.las"))


