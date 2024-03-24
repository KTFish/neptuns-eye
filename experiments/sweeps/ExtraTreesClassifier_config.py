parameters = {
    'n_estimators': {
        'min': 10,
        'max': 25
    },
    'criterion': {
        'values': ['gini', 'entropy']
    },
    'max_depth': {
        'min': 1,
        'max': 30  # Ustawienie `None` pozwala drzewom rosnąć aż do momentu, kiedy wszystkie liście są czyste lub zawierają mniej próbek niż `min_samples_split`.
    },
    'min_samples_split': {
        'min': 2,
        'max': 10
    },
    'min_samples_leaf': {
        'min': 1,
        'max': 10
    }
}

ml_metric = {
    'name': 'accuracy',
    'goal': 'maximize'
}

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "ExtraTreesClassifier",
    'parameters': parameters
}