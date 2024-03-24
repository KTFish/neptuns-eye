import wandb
from experiments.sweeps.HistGradientBoostingClassifier import sweep_config
from sklearn.ensemble import HistGradientBoostingClassifier
from experiments.sweeps.train import train
from storage.load import read_las_file


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 10
    sweep = lambda: train(train_data, test_data, HistGradientBoostingClassifier)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=sweep, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()