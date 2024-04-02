parameters = {
    'n_estimators': {
        'min': 10,
        'max': 20
    },
    'max_depth': {
        'min': 5,
        'max': 15
    },
    'min_samples_split': {
        'min': 2,
        'max': 10
    },
    'min_samples_leaf': {
        'min': 1,
        'max': 5
    },
    'max_features': {
        'min': 0.1,
        'max': 1.0
    },
    'min_impurity_decrease': {
        'min': 0.0,
        'max': 0.1
    }
}

ml_metric = {
    'name': 'accuracy',
    'goal': 'maximize'
}

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "RandomForest",
    'parameters': parameters
}
