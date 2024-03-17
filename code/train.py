from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# def random_forest_classification(X_train, X_test, y_train, y_test, n_estimators=10):
#     clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
#     print(f"\n[INFO] Training random forest on: n_estimators: {n_estimators}")
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)
#     print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
#     return y_pred, clf
#     # return np.concatenate((y_pred, y_train), axis=0)
#
#
# def knn_classification(X_train, X_test, y_train, y_test, n_neighbors=5):
#     clf = KNeighborsClassifier(n_neighbors=n_neighbors)
#     print(f"\n[INFO] Training K-Nearest Neighbors on: n_neighbors: {n_neighbors}")
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)
#     print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
#     return y_pred, clf

# need to be denoised \/


def radius_neighbors_classification(x_train, x_test, y_train, y_test, radius=160000):
    clf = RadiusNeighborsClassifier(radius=radius)
    print(f"\n[INFO] Training RadiusNeighborsClassifier on: radius: {radius}")
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.2f}")

    return y_pred, clf


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


def train(x_train, x_test, y_train, y_test, model, n=5):
    clf = model(n)
    print(f"\n[INFO] Training {model} on: n: {n}")
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred, clf


def predict(test_features, test_labels, train_model):
    y_pred = train_model.predict(test_features)

    print(f"y_test shape: {test_labels.shape}, y_pred shape: {y_pred.shape}")
    print(f"y_test type: {type(test_labels)}, y_pred type: {type(y_pred)}")

    accuracy = accuracy_score(test_labels, y_pred)
    print(f"\nAccuracy: {accuracy:.2f}")

    return y_pred
