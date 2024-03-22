"""SWEEPS FOR RANDOM FOREST."""

import wandb
from sklearn.ensemble import RandomForestClassifier
from config import *
from storage.load import read_las_file
# from experiments.sweeps.RandomForest_config import *
from preprocess.preprocess import prepare_data_training
from sklearn.metrics import accuracy_score



def train(config=None):

    with wandb.init(config=config):
        config = wandb.config

        # Data
        df = read_las_file('../../../data/train/WMII_CLASS.las')
        X_train, X_test, y_train, y_test = prepare_data_training(df)
        # TODO: Create dataset artifact (should be easy do to generic)

        # Build model
        model = RandomForestClassifier(**config)
        # model = RandomForestClassifier(n_estimators=config.n_estimators,
        #                                max_depth=config.max_depth,
        #                                min_samples_split=config.min_samples_split,
        #                                min_samples_leaf=config.min_samples_leaf,
        #                                max_features=config.max_features,
        #                                bootstrap=config.bootstrap)
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
    """Test if basic sweep works."""
    parameters = {
        'n_estimators': {  # Number of trees in the forest
            'min': 10,
            'max': 20
        },
        'max_depth': {  # Maximum depth of the tree
            'min': 5,
            'max': 15
        },
        'min_samples_split': {  # Minimum number of samples required to split an internal node
            'min': 2,
            'max': 10
        },
        'min_samples_leaf': {  # Minimum number of samples required to be at a leaf node
            'min': 1,
            'max': 5
        },
        'max_features': {  # The number of features to consider when looking for the best split
            'values': ['auto', 'sqrt', 'log2']  # 'auto' is equivalent to 'sqrt' and None means max features
        },
        'bootstrap': {  # Whether bootstrap samples are used when building trees
            'values': [True, False]
        }
    }

    sweep_config = {
        'method': 'random',
        'metric': ml_metric,
        'project': "RandomFroest",
        'parameters': parameters,
    }

    NUM_OF_TESTS = 1
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=train, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()