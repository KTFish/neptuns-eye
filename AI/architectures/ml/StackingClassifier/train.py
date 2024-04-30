from storage.load import read_las_file
from storage.save import save_joblib
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
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

    params1 = {'rf_n_estimators': 50, 'rf_max_depth': 33, 'rf_criterion': 'entropy', 'rf_min_samples_split': 17,
               'rf_min_samples_leaf': 17, 'logreg_C': 6.34298337340139}

    base_models = [
        ('rf', RandomForestClassifier(n_estimators=params1["rf_n_estimators"],
                                      max_depth=params1["rf_max_depth"],
                                      criterion=params1["rf_criterion"],
                                      min_samples_split=params1["rf_min_samples_split"],
                                      min_samples_leaf=params1["rf_min_samples_leaf"],
                                      random_state=42)),
        # Include other base models as needed
    ]

    # Create StackingClassifier
    clf = StackingClassifier(
        estimators=base_models,
        final_estimator=LogisticRegression(C=params1["logreg_C"], max_iter=1000),
        cv=5
    )

    clf.fit(X_train, y_train)
    predictions_las2 = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions_las2)

    folder_path = 'saved_models'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_joblib(clf, f"{folder_path}/{clf.__class__.__name__}{1000 * accuracy:.0f}.joblib")


if __name__ == '__main__':
    test()



