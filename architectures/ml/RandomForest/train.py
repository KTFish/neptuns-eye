from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def random_forest_classification(X_train, X_test, y_train, y_test, n_estimators=10):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    print(f"\n[INFO] Training random forest on: n_estimators: {n_estimators}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred, clf
