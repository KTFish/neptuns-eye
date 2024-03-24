# # TODO: FOR NOW ABANDONED, FIX LATER
#
#
from storage.load import read_las_file
from experiments.sweeps.HistGradientBoostingClassifier import sweep_config
from sklearn.ensemble import HistGradientBoostingClassifier
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import wandb
from sklearn.ensemble import *


def train(train, test, model, config=None):
    with wandb.init(config=config):

        config = wandb.config

        # Data
        X_train, X_test, y_train, y_test = prepare_data_training(train)
        test_features, test_labels = prepare_data_prediction(test)

        # Initialaze model
        clf = model(**config)

        # Train
        clf.fit(X_train, y_train)

        # Prediction
        y_pred = clf.predict(test_features)
        accuracy = accuracy_score(test_labels, y_pred)

        # Log to Wandb
        # wandb.log({'accuracy': accuracy,
        #            'n_estimators': config.n_estimators,
        #            'max_depth': config.max_depth,
        #            'min_samples_split': config.min_samples_split,
        #            'min_samples_leaf': config.min_samples_leaf,
        #            'max_features': config.max_features,
        #            'min_impurity_decrease': config.min_impurity_decrease})


        for param_name, param_values in config.items():
            wandb.log({param_name: param_values})
        wandb.log({"accuracy": accuracy})
        # https://docs.wandb.ai/guides/integrations/scikit


def test():

    train_data = read_las_file("../../data/train/WMII_CLASS.las")
    test_data = read_las_file("../../data/test/USER AREA.las")
    test = lambda: train(train_data, test_data, model=HistGradientBoostingClassifier)
    NUM_OF_TESTS = 3
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=test, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()
