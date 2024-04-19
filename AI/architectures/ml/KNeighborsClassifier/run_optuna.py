import optuna
from sklearn.neighbors import KNeighborsClassifier
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

    knn_n_neighbors = trial.suggest_int("n_neighbors", 1, 100)  # Liczba najbliższych sąsiadów
    knn_weights = trial.suggest_categorical("weights", ["uniform", "distance"])  # Waga przypisywana sąsiadom
    knn_algorithm = trial.suggest_categorical("algorithm", ["auto", "ball_tree", "kd_tree"])
    knn_leaf_size = trial.suggest_int("leaf_size", 1, 100)  # Rozmiar liścia przekazywany algorytmowi 'ball_tree' lub 'kd_tree'
    knn_p = trial.suggest_categorical("p", [1, 2])  # Miarę odległości: 1 - Manhattan, 2 - Euklidesowa
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
    study.optimize(objective, n_trials=10)