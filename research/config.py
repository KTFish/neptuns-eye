from storage.load import read_las_file
import os

base_path = os.path.dirname(os.path.abspath(__file__))

wmii = read_las_file(os.path.join(base_path, "data/train/WMII_CLASS.las"))
user_area = read_las_file(os.path.join(base_path, "data/test/USER AREA.las"))
