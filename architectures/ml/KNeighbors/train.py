from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def knn_classification(X_train, X_test, y_train, y_test, n_neighbors=5):
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    print(f"\n[INFO] Training K-Nearest Neighbors on: n_neighbors: {n_neighbors}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred, clf
