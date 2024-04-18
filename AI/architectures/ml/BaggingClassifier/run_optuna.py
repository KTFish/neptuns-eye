import optuna
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

from storage.load import read_las_file
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import os

def objective(trial):
    las = read_las_file("../../../data/train/WMII_CLASS.las")
    las2 = read_las_file("../../../data/test/USER_AREA.las")

    las = las[::40]
    las2 = las2[::40]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    bc_n_estimators = trial.suggest_int("n_estimators", 2, 150)
    bc_bootstrap = trial.suggest_categorical("bootstrap", [True, False])

    dtc_max_depth = trial.suggest_int("max_depth", 2, 100)
    dtc_criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
    dtc_min_samples_split = trial.suggest_int("min_samples_split", 2, 100)
    dtc_min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 100)
    dtc_min_weight_fraction_leaf = trial.suggest_float("min_weight_fraction_leaf", 0.0, 0.5)

    base_estimator = DecisionTreeClassifier(criterion=dtc_criterion,
                                            max_depth=dtc_max_depth,
                                            min_samples_split=dtc_min_samples_split,
                                            min_samples_leaf=dtc_min_samples_leaf,
                                            min_weight_fraction_leaf=dtc_min_weight_fraction_leaf)

    clf = BaggingClassifier(base_estimator=base_estimator,
                            n_estimators=bc_n_estimators,
                            bootstrap=bc_bootstrap,
                            random_state=42)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/BaggingClassifier1.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(objective, n_trials=10)
