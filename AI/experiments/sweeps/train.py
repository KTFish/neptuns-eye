"""Function fo doing sweeps"""

from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from experiments.sweeps.HistGradientBoostingClassifier import sweep_config
from storage.load import read_las_file
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score
import wandb


def train(train_data, test_data, model, config=None):

    with wandb.init(config=config):

        config = wandb.config

        X_train, X_test, y_train, y_test = prepare_data_training(train_data)
        test_features, test_labels = prepare_data_prediction(test_data)

        clf = model(**config)

        clf.fit(X_train, y_train)

        y_pred = clf.predict(test_features)
        accuracy = accuracy_score(test_labels, y_pred)

        for param_name, param_values in config.items():
            wandb.log({param_name: param_values})
        wandb.log({"accuracy": accuracy})
        # https://docs.wandb.ai/guides/integrations/scikit


def test():

    train_data = read_las_file("../../data/train/WMII_CLASS.las")
    test_data = read_las_file("../../data/test/USER AREA.las")
    sweep = lambda: train(train_data, test_data, model=HistGradientBoostingClassifier)
    NUM_OF_TESTS = 3
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=sweep, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()
