import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier

from storage.save import save_joblib


def train_evaluate_random_forest(point_cloud_df, feature_columns, label_column,
                                 validation_df=None, validation_label_column=None,
                                 test_size=0.4, random_state=42, n_estimators=100):
    """
    Trains and evaluates a RandomForestClassifier on a given point cloud dataset.

    Parameters:
    - point_cloud_df (pd.DataFrame): The input dataframe containing point cloud data.
    - feature_columns (list): List of column names to be used as features.
    - label_column (str): The column name to be used as the label.
    - validation_df (pd.DataFrame, optional): Validation dataframe.
    - validation_label_column (str, optional): Label column name in the validation dataframe.
    - test_size (float): Proportion of the dataset to include in the test split.
    - random_state (int): Random state for reproducibility.
    - n_estimators (int): Number of trees in the random forest.

    Returns:
    - report (dict): Classification report as a dictionary for the test set.
    - accuracy (float): Accuracy of the model on the test set.
    - validation_report (dict, optional): Classification report for the validation set.
    - validation_accuracy (float, optional): Accuracy on the validation set.
    """

    point_cloud_df = point_cloud_df[::720]

    # Extract features and labels
    features = point_cloud_df[feature_columns]
    labels = point_cloud_df[label_column]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=test_size,
                                                        random_state=random_state)

    # Initialize and train the RandomForestClassifier
    rf_classifier = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    save_joblib(rf_classifier, 'rf_kek.joblib')

    # Predict on the test set
    rf_predictions = rf_classifier.predict(X_test)

    # Evaluate the classifier performance
    report = classification_report(y_test, rf_predictions, output_dict=True)
    accuracy = accuracy_score(y_test, rf_predictions)

    results = {'test_report': report, 'test_accuracy': accuracy}

    if validation_df is not None and validation_label_column is not None:
        validation_df = validation_df[::30]
        validation_features = validation_df[feature_columns]
        validation_labels = validation_df[validation_label_column]

        validation_predictions = rf_classifier.predict(validation_features)
        validation_report = classification_report(validation_labels, validation_predictions, output_dict=True)
        validation_accuracy = accuracy_score(validation_labels, validation_predictions)

        results['validation_report'] = validation_report
        results['validation_accuracy'] = validation_accuracy

    return results


from config import wmii, user_area

feature_columns = ['Z', 'red', 'green', 'blue', 'intensity',
                   'number_of_returns', 'return_number', 'edge_of_flight_line', 'scan_angle_rank']
label_column = 'classification'

results = train_evaluate_random_forest(wmii, feature_columns, label_column, validation_df=user_area,
                                       validation_label_column=label_column)

print("Test Accuracy:", results['test_accuracy'])
print("Test Classification Report:")
print(pd.DataFrame(results['test_report']).transpose())

if 'validation_accuracy' in results:
    print("Validation Accuracy:", results['validation_accuracy'])
    print("Validation Classification Report:")
    print(pd.DataFrame(results['validation_report']).transpose())
