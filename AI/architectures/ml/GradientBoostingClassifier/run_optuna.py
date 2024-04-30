import optuna
from sklearn.ensemble import GradientBoostingClassifier
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

    gb_n_estimators = trial.suggest_int("n_estimators", 2, 30)  # Zmniejszone zakresy
    gb_max_depth = trial.suggest_int("max_depth", 2, 30)  # Zmniejszone zakresy
    gb_min_samples_leaf = trial.suggest_int("min_samples_leaf", 5, 40)  # Zwiększone minimum
    gb_learning_rate = trial.suggest_float("learning_rate", 0.01, 0.1)  # Zwiększona dolna granica
    gb_subsample = trial.suggest_float("subsample", 0.5, 1.0)  # Dodanie subsample

    clf = GradientBoostingClassifier(n_estimators=gb_n_estimators,
                                     max_depth=gb_max_depth,
                                     min_samples_leaf=gb_min_samples_leaf,
                                     learning_rate=gb_learning_rate,
                                     subsample=gb_subsample,  # Dodanie subsample
                                     random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/GradientBoostingClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)  # define a number of trials here
