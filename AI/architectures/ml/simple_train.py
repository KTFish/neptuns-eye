import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, accuracy_score
from storage.save import save_joblib


def train_evaluate_classifier(point_cloud_df, feature_columns, label_column,
                              clf=None, test_size=0.4, random_state=42):
    """
    Trains and evaluates a given classifier on a point cloud dataset.

    Parameters:
    - point_cloud_df (pd.DataFrame): The input dataframe containing point cloud data.
    - feature_columns (list): List of column names to be used as features.
    - label_column (str): The column name to be used as the label.
    - clf (object): The classifier to be used. If None, a RandomForestClassifier will be used.
    - test_size (float): Proportion of the dataset to include in the test split.
    - random_state (int): Random state for reproducibility.

    Returns:
    - report (dict): Classification report as a dictionary for the test set.
    - accuracy (float): Accuracy of the model on the test set.
    """

    point_cloud_df = point_cloud_df[::80]

    # Extract features and labels
    features = point_cloud_df[feature_columns]
    labels = point_cloud_df[label_column]

    # Normalize features
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=test_size,
                                                        random_state=random_state)

    # Use the provided classifier or default to RandomForestClassifier
    if clf is None:
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100, random_state=random_state)

    # Initialize and train the classifier
    clf.fit(X_train, y_train)

    # Predict on the test set
    predictions = clf.predict(X_test)

    # Evaluate the classifier performance
    report = classification_report(y_test, predictions, output_dict=True)
    accuracy = accuracy_score(y_test, predictions)

    return report, accuracy, clf


