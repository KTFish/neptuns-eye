import optuna
from sklearn.ensemble import ExtraTreesClassifier
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import sys
import os

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area

from config import wmii_filtered, user_area_filtered

def objective(trial, stride=40):
    las = wmii_filtered[::stride]
    las2 = user_area_filtered[::stride]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    rf_n_estimators = trial.suggest_int("n_estimators", 2, 200)
    rf_max_depth = trial.suggest_int("max_depth", 2, 200)
    rf_criterion = trial.suggest_categorical("criterion", ["gini", "entropy", "log_loss"])
    rf_min_samples_split = trial.suggest_int("min_samples_split", 2, 200)
    rf_min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 200)
    rf_min_weight_fraction_leaf = trial.suggest_float("min_weight_fraction_leaf", 0.0, 0.5)
    rf_bootstrap = trial.suggest_categorical("bootstrap", [True, False])

    clf = ExtraTreesClassifier(criterion=rf_criterion,
                               max_depth=rf_max_depth,
                               n_estimators=rf_n_estimators,
                               min_samples_split=rf_min_samples_split,
                               min_samples_leaf=rf_min_samples_leaf,
                               min_weight_fraction_leaf=rf_min_weight_fraction_leaf,
                               bootstrap=rf_bootstrap,
                               # class_weight=rf_class_weight,
                               random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)
    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/ExtraTreesClassifier1.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=100)  # define a number of trials here
