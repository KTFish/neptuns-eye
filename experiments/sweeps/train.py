# TODO: FOR NOW ABANDONED, FIX LATTER


import wandb
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
# from config import *
from storage.load import read_las_file
# from experiments.sweeps.RandomForest_config import *
from preprocess.preprocess import prepare_data_training
from sklearn.metrics import accuracy_score

# def train(config=None) -> None:
#     """This function will:
#     1. Access the config.
#     2. Load the model using the accessed config
#     3. Train the model (use a helper function).
#     4. Optional prints.
#     5. Log metrics to cloud.
#     """
#     pass

#
# def dataset_artifact():
#     raw_data = wandb.Artifact(
#         "mnist-raw", type="dataset",
#         description="Raw MNIST dataset, split into train/val/test",
#         metadata={"source": "torchvision.datasets.MNIST",
#                   "sizes": [len(dataset) for dataset in datasets]})


def train_ml(config=None):

    with wandb.init(config=config):
        config = wandb.config

        # Data
        df = read_las_file(config.data_path)
        X_train, y_train, X_test, y_test = prepare_data_training(df)
        # TODO: Create dataset artifact

        # Build model
        model = eval(config.model).set_params(**config.parameters)
        # TODO: Create model artifact

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        wandb.log({'accuracy': accuracy,
                   'n_estimators': config.n_estimators,
                   'max_depth': config.max_depth,
                   'min_samples_split': config.min_samples_split,
                   'min_samples_leaf': config.min_samples_leaf,
                   'max_features': config.max_features,
                   'bootstrap': config.bootstrap})


def test():
    NUM_OF_TESTS = 1
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=train_ml(), count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()