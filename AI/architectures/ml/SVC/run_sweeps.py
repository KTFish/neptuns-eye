from experiments.sweeps.train import train
from experiments.sweeps.SVC_config import sweep_config
from storage.load import read_las_file
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import wandb


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 3
    test = lambda: train(train_data, test_data, LinearSVC)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=test, count=NUM_OF_TESTS)


if __name__ == "__main__":
    test()
