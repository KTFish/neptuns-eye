from sklearn.svm import LinearSVC
from storage.load import read_las_file
import wandb
from experiments.sweeps.train import train
from experiments.sweeps.SVC_config import sweep_config
from sklearn.metrics import accuracy_score


# def svc_classification(x_train, x_test, y_train, y_test, kernel='linear', c=1.0):
#
#     # Inicjalizacja i trenowanie modelu SVC
#     clf = SVC(kernel=kernel, C=c, random_state=42, cache_size=5000)
#     print(f"\n[INFO] Training SVC on: kernel: {kernel}, C: {c}")
#     clf.fit(x_train, y_train)
#
#     # Predykcja na danych testowych
#     y_pred = clf.predict(x_test)
#
#     # Obliczanie i wyświetlanie dokładności
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"\nAccuracy: {accuracy:.2f}")
#
#     return y_pred, clf


def test():
    train_data = read_las_file('../../../data/train/WMII_CLASS.las')
    test_data = read_las_file('../../../data/test/USER AREA.las')
    NUM_OF_TESTS = 3
    test = lambda: train(train_data, test_data, LinearSVC)
    sweep_id = wandb.sweep(sweep_config, project=sweep_config["project"])
    wandb.agent(sweep_id, function=test, count=NUM_OF_TESTS)


if __name__ == "__main__":
    test()
