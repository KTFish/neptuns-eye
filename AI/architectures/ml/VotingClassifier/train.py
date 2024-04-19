"""Trials for RandomForestClassifier"""
from sklearn.neighbors import KNeighborsClassifier

from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, HistGradientBoostingClassifier, \
    VotingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
import os


def test():
    las = read_las_file("../../../data/train/WMII_CLASS.las")
    las2 = read_las_file("../../../data/test/USER_AREA.las")

    las_strided = las[::40]
    las2_strided = las2[::40]

    X_train, X_test, y_train, y_test = prepare_data_training(las_strided)
    test_features, test_labels = prepare_data_prediction(las2_strided)

    params1 = {'rf_n_estimators': 79, 'rf_max_depth': 5, 'rf_criterion': 'entropy', 'rf_min_samples_split': 4,
               'rf_min_samples_leaf': 15, 'gb_learning_rate': 0.500201172974442, 'gb_max_iter': 57, 'gb_max_depth': 34,
               'knn_n_neighbors': 30, 'knn_weights': 'distance', 'et_n_estimators': 26, 'et_max_depth': 46,
               'et_criterion': 'gini', 'et_min_samples_split': 5, 'et_min_samples_leaf': 9, 'voting_type': 'hard'}

    clf_rf = RandomForestClassifier(n_estimators=params1['rf_n_estimators'], max_depth=params1['rf_max_depth'],
                                    criterion=params1['rf_criterion'], min_samples_split=params1['rf_min_samples_split'],
                                    min_samples_leaf=params1['rf_min_samples_leaf'], random_state=42)
    clf_gb = HistGradientBoostingClassifier(learning_rate=params1['gb_learning_rate'], max_iter=params1['gb_max_iter'],
                                            max_depth=params1['gb_max_depth'], random_state=42)

    clf_knn = KNeighborsClassifier(n_neighbors=params1['knn_n_neighbors'], weights=params1['knn_weights'])
    clf_et = ExtraTreesClassifier(n_estimators=params1['et_n_estimators'], max_depth=params1['et_max_depth'],
                                  criterion=params1['et_criterion'], min_samples_split=params1['et_min_samples_split'],
                                  min_samples_leaf=params1['et_min_samples_leaf'], random_state=42)

    # Create VotingClassifier
    clf = VotingClassifier(
        estimators=[('rf', clf_rf), ('gb', clf_gb), ('knn', clf_knn), ('et', clf_et)],
        voting=params1['voting_type']
    )

    clf.fit(X_train, y_train)
    predictions_las2 = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions_las2)

    print(accuracy)

    folder_path = 'saved_models'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_joblib(clf, f"{folder_path}/{clf.__class__.__name__}{1000 * accuracy:.0f}.joblib")


if __name__ == '__main__':
    test()



