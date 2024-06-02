import sys
import os

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sys.path.append(os.path.abspath('../'))
from config import wmii, user_area, kortowo


def make_correlation_matrix(df):

    correlation_matrix = df.corr()

    # Wyświetl macierz korelacji w postaci heatmapy
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=.5,
                cbar_kws={"shrink": 0.8}, ax=ax)

    # Ustaw etykiety osi
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    # Przenieś etykiety osi X na górę
    ax.xaxis.tick_top()

    # Ustaw tytuł wykresu na dole
    fig.text(0.5, 0.04, 'Correlation Matrix (kortowo) with unnecessary data removed', ha='center', fontsize=20)

    plt.show()


def make_confusion_matrix(y_test, y_pred):
    # Generowanie macierzy konfuzji z normalizacją
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    # Pobranie unikalnych wartości z y_test i y_pred jako etykiet klas
    target_names = np.union1d(y_test, y_pred)

    # Rysowanie macierzy konfuzji
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')

    # Przenieś etykiety osi X na górę
    ax.xaxis.tick_top()

    plt.show()


if __name__ == '__main__':
    columns_to_keep = ['Z', 'red', 'green', 'blue', 'intensity', 'classification',
                       'number_of_returns', 'return_number', 'edge_of_flight_line', 'scan_angle_rank']
    kortowo = kortowo.loc[:, columns_to_keep]
    make_correlation_matrix(kortowo)


