from sklearn.metrics import accuracy_score


def train(x_train, x_test, y_train, y_test, model, n=5):
    clf = model(n)
    print(f"\n[INFO] Training {model} on: n: {n}")
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
    return y_pred, clf
