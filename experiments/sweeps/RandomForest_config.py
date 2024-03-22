from config import *

parameters = {
        'n_estimators': {  # Number of trees in the forest
            'min': 10,
            'max': 20
        },
        'max_depth': {  # Maximum depth of the tree
            'min': 5,
            'max': 15
        },
        'min_samples_split': {  # Minimum number of samples required to split an internal node
            'min': 2,
            'max': 10
        },
        'min_samples_leaf': {  # Minimum number of samples required to be at a leaf node
            'min': 1,
            'max': 5
        },
        'max_features': {  # The number of features to consider when looking for the best split
            'values': ['auto', 'sqrt', 'log2']  # 'auto' is equivalent to 'sqrt' and None means max features
        },
        'bootstrap': {  # Whether bootstrap samples are used when building trees
            'values': [True, False]
        }
    }

sweep_config = {
    'method': 'random',
    'metric': ml_metric,
    'project': "RandomFroest",
    'parameters': parameters,
    'model': "RandomForestClassifier()",
    'data_path': WMII_CLASS
}
