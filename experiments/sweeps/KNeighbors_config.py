parameters = {
    'n_neighbors': {
        'min': 3,
        'max': 20
    },
    'leaf_size': {
        'min': 10,
        'max': 50
    },
    'p': {
        'values': [1, 2]
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