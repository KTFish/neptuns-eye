from preprocess.preprocess import prepare_data
from storage.save import save_joblib
from sklearn.metrics import accuracy_score
import pandas as pd


def train_ml(df: pd.DataFrame,
             clf,
             test_acc: bool = False,
             save_path: str = None):

    X_train, X_test, y_train, y_test = prepare_data(df, purpose="training")

    print(f"\n[INFO] Training with {clf.__class__.__name__}:")
    clf.fit(X_train, y_train)
    y_pred = None

    if test_acc:
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        print(f"\nTest accuracy: {accuracy:.2f}%")

    if save_path is not None:
        save_joblib(clf, save_path)
    print("Training done!")

    return clf, y_pred

