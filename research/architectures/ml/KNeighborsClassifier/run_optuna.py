import optuna
from sklearn.neighbors import KNeighborsClassifier
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

    knn_n_neighbors = trial.suggest_int("n_neighbors", 1, 100)
    knn_weights = trial.suggest_categorical("weights", ["uniform", "distance"])
    knn_algorithm = trial.suggest_categorical("algorithm", ["auto", "ball_tree", "kd_tree"])
    knn_leaf_size = trial.suggest_int("leaf_size", 1, 100)
    knn_p = trial.suggest_categorical("p", [1, 2])
    knn_n_jobs = trial.suggest_categorical("n_jobs", [1, -1])

    clf = KNeighborsClassifier(n_neighbors=knn_n_neighbors,
                               weights=knn_weights,
                               algorithm=knn_algorithm,
                               leaf_size=knn_leaf_size,
                               p=knn_p,
                               n_jobs=knn_n_jobs)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/KNeighborsClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)
