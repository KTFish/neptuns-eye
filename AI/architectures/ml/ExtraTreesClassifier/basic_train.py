from sklearn.ensemble import ExtraTreesClassifier

from storage.save import save_joblib
import pandas as pd
from AI.architectures.ml.simple_train import train_evaluate_classifier


def run_training():
    # Example usage
    from config import wmii, user_area

    # Połączenie obu ramek danych
    combined_df = pd.concat([wmii, user_area])

    feature_columns = ['Z', 'red', 'green', 'blue', "intensity", "number_of_returns", "edge_of_flight_line"]
    label_column = 'classification'
    #
    # # Użycie domyślnego klasyfikatora (RandomForestClassifier)
    # report, accuracy, _ = train_evaluate_classifier(combined_df, feature_columns, label_column)
    #
    # print("Accuracy:", accuracy)
    # print("Classification Report:")
    # print(pd.DataFrame(report).transpose())

    # Użycie innego klasyfikatora
    svm_clf = ExtraTreesClassifier(n_estimators=1000, random_state=42)
    report, accuracy, clf = train_evaluate_classifier(combined_df, feature_columns, label_column, clf=svm_clf)

    print("Accuracy with ExtraTreesClassifier:", accuracy)
    print("Classification Report:")
    print(pd.DataFrame(report).transpose())

    save_joblib(clf, "aha77.joblib")


if __name__ == "__main__":
    run_training()
