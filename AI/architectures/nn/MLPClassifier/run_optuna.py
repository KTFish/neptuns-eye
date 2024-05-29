import optuna
from experiments.trials.optuna_runner import objective
import sys
import os

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    model_type = "MLP"

    storage_url = f"sqlite:///{folder_path}/{model_type}_Classifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial,
                                           model_type=model_type,
                                           stride=45,
                                           training_set=wmii,
                                           validation_set=user_area), n_trials=2)
