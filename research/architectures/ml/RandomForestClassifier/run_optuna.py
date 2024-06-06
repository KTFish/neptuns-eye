import optuna
from sklearn.ensemble import RandomForestClassifier
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

    rf_n_estimators = trial.suggest_int("n_estimators", 2, 150)
    rf_max_depth = trial.suggest_int("max_depth", 2, 100)
    rf_criterion = trial.suggest_categorical("criterion", ["gini", "entropy", "log_loss"])
    rf_min_samples_split = trial.suggest_int("min_samples_split", 2, 100)
    rf_min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 100)
    rf_min_weight_fraction_leaf = trial.suggest_float("min_weight_fraction_leaf", 0.0, 0.5)
    rf_bootstrap = trial.suggest_categorical("bootstrap", [True, False])

    rf_class_0 = trial.suggest_int("class_0", 1, 30)
    rf_class_1 = trial.suggest_int("class_1", 1, 30)
    rf_class_11 = trial.suggest_int("class_11", 1, 30)
    rf_class_13 = trial.suggest_int("class_13", 1, 30)
    rf_class_15 = trial.suggest_int("class_15", 1, 30)
    rf_class_17 = trial.suggest_int("class_17", 1, 30)
    rf_class_19 = trial.suggest_int("class_19", 1, 30)
    rf_class_25 = trial.suggest_int("class_25", 1, 30)

    rf_class_weight = {0: rf_class_0,
                       1: rf_class_1,
                       11: rf_class_11,
                       13: rf_class_13,
                       15: rf_class_15,
                       17: rf_class_17,
                       19: rf_class_19,
                       25: rf_class_25}

    clf = RandomForestClassifier(criterion=rf_criterion,
                                 max_depth=rf_max_depth,
                                 n_estimators=rf_n_estimators,
                                 min_samples_split=rf_min_samples_split,
                                 min_samples_leaf=rf_min_samples_leaf,
                                 min_weight_fraction_leaf=rf_min_weight_fraction_leaf,
                                 bootstrap=rf_bootstrap,
                                 class_weight=rf_class_weight,
                                 random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/RandomForestClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)  # define a number of trials here
