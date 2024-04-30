import optuna
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
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

    ab_n_estimators = trial.suggest_int("n_estimators", 10, 50)
    ab_learning_rate = trial.suggest_float("learning_rate", 0.01, 1.0)
    ab_algorithm = trial.suggest_categorical("algorithm", ["SAMME", "SAMME.R"])

    dtc_max_depth = trial.suggest_int("base_estimator_max_depth", 1, 10)
    dtc_min_samples_split = trial.suggest_int("base_estimator_min_samples_split", 2, 20)
    dtc_min_samples_leaf = trial.suggest_int("base_estimator_min_samples_leaf", 1, 20)

    base_estimator = DecisionTreeClassifier(max_depth=dtc_max_depth,
                                            min_samples_split=dtc_min_samples_split,
                                            min_samples_leaf=dtc_min_samples_leaf)

    clf = AdaBoostClassifier(base_estimator=base_estimator,
                             n_estimators=ab_n_estimators,
                             learning_rate=ab_learning_rate,
                             algorithm=ab_algorithm,
                             random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/AdaBoostClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)  # define a number of trials here
