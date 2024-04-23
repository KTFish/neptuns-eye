from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.neighbors import KNeighborsClassifier
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

    params1 = {'n_neighbors': 84, 'weights': 'uniform', 'algorithm': 'auto', 'leaf_size': 55, 'p': 1, 'n_jobs': -1}

    clf = KNeighborsClassifier(n_neighbors=params1['n_neighbors'],
                               weights=params1['weights'],
                               algorithm=params1['algorithm'],
                               leaf_size=params1['leaf_size'],
                               p=params1['p'],
                               n_jobs=params1['n_jobs'])

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
