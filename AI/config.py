from storage.load import read_las_file, read_las_file_filtered
import os
# TODO: Uncomment when pytorch will be used
# import torch
# device = "cuda" if torch.cuda.is_available() else "cpu"
# from storage.load import read_las_file
# from pathlib import Path

# WEIGHTS AND BIASES

# DIRECTORY PATHS

# Ustaw ścieżkę bazową do katalogu, w którym znajduje się plik config
base_path = os.path.dirname(os.path.abspath(__file__))

# Definiuj zmienne z odpowiednio zmodyfikowanymi ścieżkami
wmii = read_las_file(os.path.join(base_path, "data/train/WMII_CLASS.las"))
user_area = read_las_file(os.path.join(base_path, "data/test/USER_AREA.las"))

wmii_filtered = read_las_file_filtered(os.path.join(base_path, "data/train/WMII_CLASS.las"))
user_area_filtered = read_las_file_filtered(os.path.join(base_path, "data/test/USER_AREA.las"))

