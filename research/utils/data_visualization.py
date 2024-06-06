import sys
import os

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sys.path.append(os.path.abspath('../'))
from config import wmii, user_area


def make_correlation_matrix(df, text: str):
    """
    Generate and display a correlation matrix heatmap for a given DataFrame.
    Parameters:
    df (DataFrame): The DataFrame containing the data to be analyzed.
    text (str): The title text to display below the heatmap.
    """
    correlation_matrix = df.corr()

    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=.5,
                cbar_kws={"shrink": 0.8}, ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    ax.xaxis.tick_top()

    fig.text(0.5, 0.04, text, ha='center', fontsize=20)

    plt.show()


def make_confusion_matrix(y_test, y_pred):
    """
    Generate a confusion matrix plot.
    Parameters:
    y_test (array-like): True labels.
    y_pred (array-like): Predicted labels.
    Returns:
    None
    """
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    target_names = np.union1d(y_test, y_pred)

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')

    ax.xaxis.tick_top()

    plt.show()


if __name__ == '__main__':
    columns_to_keep = ['Z', 'red', 'green', 'blue', 'intensity', 'classification',
                       'number_of_returns', 'return_number', 'edge_of_flight_line', 'scan_angle_rank']
    wmii = wmii.loc[:, columns_to_keep]
    make_correlation_matrix(wmii, "placeholder")


