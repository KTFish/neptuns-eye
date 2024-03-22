from preprocess.preprocess import prepare_data_training
from storage.save import save_model
from sklearn.metrics import accuracy_score
import pandas as pd
import wandb


def train_ml(df: pd.DataFrame,
             clf,
             target_column="classification",
             sample_rate=0.1,
             test_size=0.2,
             random_state=42,
             test_acc: bool = False,
             save_path: str = None):
    X_train, X_test, y_train, y_test = prepare_data_training(df,
                                                             target_column,
                                                             sample_rate=sample_rate,
                                                             test_size=test_size,
                                                             random_state=random_state)

    print(f"\n[INFO] Training with {clf.__class__.__name__}:")
    clf.fit(X_train, y_train)
    y_pred = None

    if test_acc:
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        print(f"\nTest accuracy: {accuracy:.2f}%")

    if save_path is not None:
        save_model(clf, save_path)
    print("Training done!")

    return clf, y_pred
