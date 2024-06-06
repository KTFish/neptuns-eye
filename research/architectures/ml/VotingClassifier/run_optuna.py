import optuna
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, \
    HistGradientBoostingClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import os
import sys

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def objective(trial, stride):

    las = wmii[::stride]
    las2 = user_area[::stride]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    rf_n_estimators = trial.suggest_int("rf_n_estimators", 10, 100)
    rf_max_depth = trial.suggest_int("rf_max_depth", 3, 50)
    rf_criterion = trial.suggest_categorical("rf_criterion", ["gini", "entropy"])
    rf_min_samples_split = trial.suggest_int("rf_min_samples_split", 2, 20)
    rf_min_samples_leaf = trial.suggest_int("rf_min_samples_leaf", 1, 20)

    gb_learning_rate = trial.suggest_float("gb_learning_rate", 0.01, 1.0)
    gb_max_iter = trial.suggest_int("gb_max_iter", 50, 200)
    gb_max_depth = trial.suggest_int("gb_max_depth", 3, 50)

    knn_n_neighbors = trial.suggest_int("knn_n_neighbors", 3, 30)
    knn_weights = trial.suggest_categorical("knn_weights", ["uniform", "distance"])

    et_n_estimators = trial.suggest_int("et_n_estimators", 10, 100)
    et_max_depth = trial.suggest_int("et_max_depth", 3, 50)
    et_criterion = trial.suggest_categorical("et_criterion", ["gini", "entropy"])
    et_min_samples_split = trial.suggest_int("et_min_samples_split", 2, 20)
    et_min_samples_leaf = trial.suggest_int("et_min_samples_leaf", 1, 20)

    voting_type = trial.suggest_categorical("voting_type", ["hard", "soft"])

    clf_rf = RandomForestClassifier(n_estimators=rf_n_estimators, max_depth=rf_max_depth,
                                    criterion=rf_criterion, min_samples_split=rf_min_samples_split,
                                    min_samples_leaf=rf_min_samples_leaf, random_state=42)
    clf_gb = HistGradientBoostingClassifier(learning_rate=gb_learning_rate, max_iter=gb_max_iter,
                                            max_depth=gb_max_depth, random_state=42)
    clf_knn = KNeighborsClassifier(n_neighbors=knn_n_neighbors, weights=knn_weights)
    clf_et = ExtraTreesClassifier(n_estimators=et_n_estimators, max_depth=et_max_depth,
                                  criterion=et_criterion, min_samples_split=et_min_samples_split,
                                  min_samples_leaf=et_min_samples_leaf, random_state=42)

    clf = VotingClassifier(
        estimators=[('rf', clf_rf), ('gb', clf_gb), ('knn', clf_knn), ('et', clf_et)],
        voting=voting_type
    )

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/VotingClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)
