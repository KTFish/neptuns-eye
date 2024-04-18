"""Trials for RandomForestClassifier"""
from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import RandomForestClassifier
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

    params1 = {'n_estimators': 103, 'max_depth': 72, 'criterion': 'entropy', 'min_samples_split': 62,
               'min_samples_leaf': 84, 'min_weight_fraction_leaf': 0.0434597955820919, 'bootstrap': False,
               'class_0': 4, 'class_1': 9, 'class_11': 30, 'class_13': 13, 'class_15': 17, 'class_17': 13,
               'class_19': 26, 'class_25': 14}

    rf_class_weight = {}

    for key, value in params1.items():
        if key.startswith('class_'):
            class_number = int(key.split('_')[1])
            rf_class_weight[class_number] = value

    print(rf_class_weight)

    clf = RandomForestClassifier(n_estimators=params1['n_estimators'],
                                 max_depth=params1['max_depth'],
                                 criterion=params1['criterion'],
                                 min_samples_split=params1['min_samples_split'],
                                 min_samples_leaf=params1['min_samples_leaf'],
                                 min_weight_fraction_leaf=params1['min_weight_fraction_leaf'],
                                 bootstrap=params1["bootstrap"],
                                 class_weight=rf_class_weight,
                                 random_state=42)

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
