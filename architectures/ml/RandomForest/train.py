"""SWEEPS FOR RANDOM FOREST."""
import pandas as pd

import wandb
from sklearn.ensemble import RandomForestClassifier
from experiments.sweeps.train import train
from storage.load import read_las_file
import joblib
from experiments.sweeps.RandomForest_config import *


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 3
    test = lambda: train(train_data, test_data, RandomForestClassifier)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=test, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()