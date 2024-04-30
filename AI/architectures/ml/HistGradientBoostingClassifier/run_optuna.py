import optuna
from sklearn.ensemble import HistGradientBoostingClassifier
from storage.load import read_las_file
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import sys
import os

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def objective(trial, stride=40):
    las = wmii[::stride]
    las2 = user_area[::stride]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    hgb_n_estimators = trial.suggest_int("n_estimators", 2, 150)
    hgb_max_depth = trial.suggest_int("max_depth", 2, 100)
    hgb_min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 100)
    hgb_learning_rate = trial.suggest_float("learning_rate", 0.001, 1.0)
    hgb_max_bins = trial.suggest_int("max_bins", 2, 255)

    clf = HistGradientBoostingClassifier(max_iter=hgb_n_estimators,
                                         max_depth=hgb_max_depth,
                                         min_samples_leaf=hgb_min_samples_leaf,
                                         learning_rate=hgb_learning_rate,
                                         max_bins=hgb_max_bins,
                                         random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/HistGradientBoostingClassifier1.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)  # define a number of trials here
