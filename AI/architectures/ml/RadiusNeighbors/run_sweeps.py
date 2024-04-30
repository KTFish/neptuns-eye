"""Work in progress, data must be denoise"""
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.metrics import accuracy_score


def radius_neighbors_classification(x_train, x_test, y_train, y_test, radius=160000):
    clf = RadiusNeighborsClassifier(radius=radius)
    print(f"\n[INFO] Training RadiusNeighborsClassifier on: radius: {radius}")
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.2f}")

    return y_pred, clf
