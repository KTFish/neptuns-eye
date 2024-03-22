# TODO: Uncomment when pytorch will be used
# import torch
# device = "cuda" if torch.cuda.is_available() else "cpu"
from storage.load import read_las_file

from pathlib import Path

# WEIGHTS AND BIASES
PROJECT_NAME = ''
ml_metric = {
        'name': 'accuracy',
        'goal': 'maximize'
    }


# DIRECTORY PATHS
# wmii = read_las_file()