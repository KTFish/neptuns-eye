from sklearn.ensemble import StackingClassifier, RandomForestClassifier, GradientBoostingClassifier, \
    HistGradientBoostingClassifier
import os

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from storage.save import save_joblib
import pandas as pd
from AI.architectures.ml.simple_train import train_evaluate_classifier


def run_training():
    # Example usage
    from config import wmii, user_area

    # Połączenie obu ramek danych
    # combined_df = pd.concat([wmii, user_area])
    df = wmii
    df2 = user_area

    feature_columns = ['Z', 'red', 'green', 'blue', "intensity", "number_of_returns", "edge_of_flight_line"]
    label_column = 'classification'

    clf = StackingClassifier(estimators=[('rf', RandomForestClassifier(n_estimators=100)),
                                         ('KNN', KNeighborsClassifier()),
                                         ('hgb', HistGradientBoostingClassifier())],
                             final_estimator=LogisticRegression(max_iter=2000))

    report, accuracy, report2, accuracy2, clf = train_evaluate_classifier(df,
                                                                          feature_columns,
                                                                          label_column,
                                                                          validation_df=df2,
                                                                          clf=clf)

    print("Accuracy with ExtraTreesClassifier on training dataset:", accuracy)
    print("Classification Report:")
    print(pd.DataFrame(report).transpose())

    print("Accuracy with ExtraTreesClassifier on validation dataset:", accuracy2)
    print("Classification Report:")
    print(pd.DataFrame(report2).transpose())

    folder_path = 'saved_models'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_joblib(clf, f"{folder_path}/aha77.joblib")


if __name__ == "__main__":
    run_training()

