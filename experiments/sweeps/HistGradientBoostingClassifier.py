parameters = {
    'learning_rate': {
        'min': 0.01,
        'max': 0.3
    },
    'max_iter': {
        'min': 100,
        'max': 1000
    },
    'max_depth': {
        'min': 10,
        'max': 30
    },
    'min_samples_leaf': {
        'min': 20,
        'max': 100
    },
    'l2_regularization': {
        'min': 0.0,
        'max': 1.0
    },
    'max_bins': {
        'min': 50,
        'max': 255  # Wartość maksymalna to 255
    },
    'max_leaf_nodes': {
        'min': 31,
        'max': 255
    }
}

ml_metric = {
    'name': 'accuracy',
    'goal': 'maximize'
}

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "HistGradientBoostingClassifier",
    'parameters': parameters
}