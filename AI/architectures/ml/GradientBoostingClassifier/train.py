"""Trials for GradientBoostingCLassifier"""
from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import GradientBoostingClassifier
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

    params1 = {'n_estimators': 24, 'max_depth': 2, 'min_samples_leaf': 21, 'learning_rate': 0.054760435890100975,
               'subsample': 0.9392221613418507}

    clf = GradientBoostingClassifier(n_estimators=params1['n_estimators'],
                                     max_depth=params1['max_depth'],
                                     min_samples_leaf=params1['min_samples_leaf'],
                                     learning_rate=params1['learning_rate'],
                                     subsample=params1['subsample'],
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
