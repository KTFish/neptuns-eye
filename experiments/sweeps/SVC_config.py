parameters = {
    'C': {
        'min': 0.01,
        'max': 10.0
    },
    'penalty': {
        'values': ['l1', 'l2']
    },
    'tol': {
        'min': 0.0001,
        'max': 0.1
    },
    'fit_intercept': {
        'values': [True, False]
    },
    'intercept_scaling': {
        'min': 1,
        'max': 10
    },
    'class_weight': {
        'values': ['balanced']
    },
    'max_iter': {
        'min': 1000,
        'max': 10000
    }
}

ml_metric = {
    'name': 'accuracy',
    'goal': 'maximize'
}

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "LinearSVC",
    'parameters': parameters
}