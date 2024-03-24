parameters = {
    'n_estimators': {
        'min': 10,
        'max': 50
    },
    'criterion': {
        'values': ['gini', 'entropy']
    },
    'max_depth': {
        'min': 1,
        'max': 30
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
