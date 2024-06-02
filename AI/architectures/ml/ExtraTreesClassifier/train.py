from storage.save import save_joblib
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from preprocess.preprocess import prepare_data
import os
import sys

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def test():
    las_strided = wmii[::720]
    las2_strided = user_area[::30]

    X_train, X_test, y_train, y_test = prepare_data(las_strided, purpose="training")
    test_features, test_labels = prepare_data(las2_strided, purpose="prediction")

    params2 = {'n_estimators': 56, 'max_depth': 163, 'criterion': 'entropy', 'min_samples_split': 69,
               'min_samples_leaf': 8, 'min_weight_fraction_leaf': 1.807024458708799e-05, 'bootstrap': False}
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
                               # class_weight=rf_class_weight,
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