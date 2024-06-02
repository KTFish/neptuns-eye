from sklearn.ensemble import AdaBoostClassifier
import os

from sklearn.tree import DecisionTreeClassifier

from storage.save import save_joblib
import pandas as pd
from AI.architectures.ml.simple_train import train_evaluate_classifier

def run_training():
    # Example usage
    from config import wmii, user_area

    # Połączenie obu ramek danych
    df = wmii
    df2 = user_area

    feature_columns = ['Z', 'red', 'green', 'blue', "intensity", "number_of_returns", "edge_of_flight_line"]
    label_column = 'classification'

    clf = AdaBoostClassifier(estimator=DecisionTreeClassifier(), n_estimators=100, random_state=42)
    report, accuracy, report2, accuracy2, clf = train_evaluate_classifier(df,
                                                                          feature_columns,
                                                                          label_column,
                                                                          validation_df=df2,
                                                                          clf=clf)

    print("Accuracy with AdaBoostClassifier on training dataset:", accuracy)
    print("Classification Report:")
    print(pd.DataFrame(report).transpose())

    print("Accuracy with AdaBoostClassifier on validation dataset:", accuracy2)
    print("Classification Report:")
    print(pd.DataFrame(report2).transpose())

    folder_path = 'saved_models'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    save_joblib(clf, f"{folder_path}/aha77.joblib")


if __name__ == "__main__":
    run_training()