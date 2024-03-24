from experiments.sweeps.train import train
from storage.load import read_las_file
import wandb
from sklearn.neighbors import KNeighborsClassifier
from experiments.sweeps.train import train
from experiments.sweeps.KNeighbors_config import sweep_config
from sklearn.metrics import accuracy_score


def knn_classification(X_train, X_test, y_train, y_test, n_neighbors=5):
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    print(f"\n[INFO] Training K-Nearest Neighbors on: n_neighbors: {n_neighbors}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred, clf


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 3
    test = lambda: train(train_data, test_data, KNeighborsClassifier)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=test, count=NUM_OF_TESTS)



if __name__ == "__main__":
    test()
