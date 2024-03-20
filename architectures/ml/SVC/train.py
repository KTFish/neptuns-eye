from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def svc_classification(x_train, x_test, y_train, y_test, kernel='linear', c=1.0):

    # Inicjalizacja i trenowanie modelu SVC
    clf = SVC(kernel=kernel, C=c, random_state=42, cache_size=5000)
    print(f"\n[INFO] Training SVC on: kernel: {kernel}, C: {c}")
    clf.fit(x_train, y_train)

    # Predykcja na danych testowych
    y_pred = clf.predict(x_test)

    # Obliczanie i wyświetlanie dokładności
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.2f}")

    return y_pred, clf
