import optuna
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from storage.load import read_las_file
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import os


def objective(trial):
    las = read_las_file("../../../data/train/WMII_CLASS.las")
    las2 = read_las_file("../../../data/test/USER_AREA.las")

    las = las[::40]
    las2 = las2[::40]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    rf_n_estimators = trial.suggest_int("rf_n_estimators", 10, 100)
    rf_max_depth = trial.suggest_int("rf_max_depth", 3, 50)
    rf_criterion = trial.suggest_categorical("rf_criterion", ["gini", "entropy"])
    rf_min_samples_split = trial.suggest_int("rf_min_samples_split", 2, 20)
    rf_min_samples_leaf = trial.suggest_int("rf_min_samples_leaf", 1, 20)

    # Suggest parameters for final estimator, here LogisticRegression
    C = trial.suggest_float("logreg_C", 0.01, 10.0)

    # Create the base models
    base_models = [
        ('rf', RandomForestClassifier(n_estimators=rf_n_estimators, max_depth=rf_max_depth,
                                      criterion=rf_criterion, min_samples_split=rf_min_samples_split,
                                      min_samples_leaf=rf_min_samples_leaf, random_state=42)),
        # Include other base models as needed
    ]

    clf = StackingClassifier(
        estimators=base_models,
        final_estimator=LogisticRegression(C=C, max_iter=1000),
        cv=5
    )

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/StackingClassifier1.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(objective, n_trials=20)
