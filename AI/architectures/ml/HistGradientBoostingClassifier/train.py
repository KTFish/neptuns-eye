from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
import os
import sys

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def test():
    las_strided = wmii[::40]
    las2_strided = user_area[::40]

    X_train, X_test, y_train, y_test = prepare_data_training(las_strided)
    test_features, test_labels = prepare_data_prediction(las2_strided)

    params1 = {'n_estimators': 89, 'max_depth': 3, 'min_samples_leaf': 67, 'learning_rate': 0.12935930291728567, 'max_bins': 57}

    clf = HistGradientBoostingClassifier(max_iter=params1['n_estimators'],
                                         max_depth=params1['max_depth'],
                                         min_samples_leaf=params1['min_samples_leaf'],
                                         learning_rate=params1['learning_rate'],
                                         max_bins=params1['max_bins'],
                                         random_state=42)

    clf.fit(X_train, y_train)
    predictions_las2 = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions_las2)

    folder_path = 'saved_models'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_joblib(clf, f"{folder_path}/{clf.__class__.__name__}{1000 * accuracy:.0f}.joblib")


if __name__ == '__main__':
    test()
