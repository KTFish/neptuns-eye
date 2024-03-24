"""SWEEPS FOR RANDOM FOREST."""

import wandb
from sklearn.ensemble import RandomForestClassifier
# from config import *
from storage.load import read_las_file
# from experiments.sweeps.RandomForest_config import *
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
from storage.save import save_joblib
import joblib


def create_model_artifact():
    pass


def build_model_and_log(config):
    # with wandb.init(project="artifacts-example", job_type="initialize", config=config) as run:
    # config = wandb.config

    model = RandomForestClassifier(**config)

    model_artifact = wandb.Artifact(
        "convnet", type="model",
        description="Simple AlexNet style CNN",
        metadata=dict(config))

    joblib.dump(model, "RandomForest.joblib")
    # ➕ another way to add a file to an Artifact
    model_artifact.add_file("RandomForest.joblib")

    wandb.save("RandomForest.joblib")

    # run.log_artifact(model_artifact)
    return model


def create_dataset_artifact():
    pass


def train(config=None):

    with wandb.init(config=config):
        config = wandb.config

        # Data
        df = read_las_file('../../../data/train/WMII_CLASS.las')
        test = read_las_file('../../../data/test/USER AREA.las')
        X_train, X_test, y_train, y_test = prepare_data_training(df)
        test_features, test_labels = prepare_data_prediction(test)

        # TODO: Create dataset artifact (should be easy do to generic)
        # https://docs.wandb.ai/tutorials/artifacts#-what-are-artifacts-and-why-should-i-care
        # https://docs.wandb.ai/ref/python/artifact

        # Build model and create artifact
        # model = RandomForestClassifier(**config)
        # TODO: Create model artifact

        # Initialaze model
        model = RandomForestClassifier(**config)

        # Train
        model.fit(X_train, y_train)

        # Prediction
        y_pred = model.predict(test_features)
        accuracy = accuracy_score(test_labels, y_pred)

        # Log to Wandb
        wandb.log({'accuracy': accuracy,
                   'n_estimators': config.n_estimators,
                   'max_depth': config.max_depth,
                   'min_samples_split': config.min_samples_split,
                   'min_samples_leaf': config.min_samples_leaf})
        # https://docs.wandb.ai/guides/integrations/scikit


def test():
    """Test if basic sweep works."""
    parameters = {
        'n_estimators': {
            'min': 10,
            'max': 20
        },
        'max_depth': {
            'min': 5,
            'max': 15
        },
        'min_samples_split': {
            'min': 2,
            'max': 10
        },
        'min_samples_leaf': {
            'min': 1,
            'max': 5
        }
    }
    ml_metric = {
        'name': 'accuracy',
        'goal': 'maximize'
    }

    sweep_config = {
        'method': 'random',
        'metric': ml_metric,
        'project': "user_area prediction",
        'parameters': parameters
    }

    NUM_OF_TESTS = 10
    # https://docs.wandb.ai/guides/sweeps
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=train, count=NUM_OF_TESTS)


if __name__ == '__main__':
    test()