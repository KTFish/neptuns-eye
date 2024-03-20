from utils.preprocess import prepare_data_training
from storage.save import save_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd


def random_forest_classification(df: pd.DataFrame,
                                 target_column="classification",
                                 sample_rate=0.1,
                                 test_size=0.2,
                                 random_state=42,
                                 n_estimators=10,
                                 save_path: str = None):

    X_train, X_test, y_train, y_test = prepare_data_training(df,
                                                             target_column,
                                                             sample_rate=sample_rate,
                                                             test_size=test_size,
                                                             random_state=random_state)

    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)

    print(f"\n[INFO] Training random forest on: n_estimators: {n_estimators}")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")

    if save_path is not None:
        save_model(clf, save_path)

    return y_pred, clf
