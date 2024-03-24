parameters = {
    'n_neighbors': {
        'min': 3,
        'max': 50
    },
    'leaf_size': {
        'min': 7,
        'max': 100
    },
    'p': {
        'values': [1]
    }
}

ml_metric = {
    'name': 'accuracy',
    'goal': 'maximize'
}

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "KNeighborsClassifier",
    'parameters': parameters
}
