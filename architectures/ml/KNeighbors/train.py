"""Sweeps for KNeighborsClassifier"""
from experiments.sweeps.train import train
from experiments.sweeps.KNeighbors_config import sweep_config
from storage.load import read_las_file
from sklearn.neighbors import KNeighborsClassifier
import wandb


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 30
    sweep = lambda: train(train_data, test_data, KNeighborsClassifier)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=sweep, count=NUM_OF_TESTS)


if __name__ == "__main__":
    test()
