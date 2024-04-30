from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import ExtraTreesClassifier
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

    params1 = {'n_estimators': 68, 'max_depth': 52, 'criterion': 'entropy', 'min_samples_split': 46,
               'min_samples_leaf': 66,
               'min_weight_fraction_leaf': 0.00026385974415840387, 'bootstrap': True, 'class_0': 29, 'class_1': 29,
               'class_11': 29,
               'class_13': 9, 'class_15': 8, 'class_17': 2, 'class_19': 6, 'class_25': 3}
    params2 = {'n_estimators': 145, 'max_depth': 43, 'criterion': 'log_loss', 'min_samples_split': 37,
               'min_samples_leaf': 26,
               'min_weight_fraction_leaf': 0.00027492164326257723, 'bootstrap': True, 'class_0': 87, 'class_1': 93,
               'class_11': 89, 'class_13': 19, 'class_15': 43, 'class_17': 56, 'class_19': 10, 'class_25': 11}
    rf_class_weight = {}

    for key, value in params2.items():
        if key.startswith('class_'):
            class_number = int(key.split('_')[1])
            rf_class_weight[class_number] = value

    clf = ExtraTreesClassifier(n_estimators=params2['n_estimators'],
                               max_depth=params2['max_depth'],
                               criterion=params2['criterion'],
                               min_samples_split=params2['min_samples_split'],
                               min_samples_leaf=params2['min_samples_leaf'],
                               min_weight_fraction_leaf=params2['min_weight_fraction_leaf'],
                               bootstrap=params2["bootstrap"],
                               class_weight=rf_class_weight,
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
