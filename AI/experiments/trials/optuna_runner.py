import sys
import json
import os
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier, GradientBoostingClassifier, \
    HistGradientBoostingClassifier, RandomForestClassifier, StackingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from preprocess.preprocess import prepare_data

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def load_hyperparameter_config(model_type):
    with open(f"../../../experiments/trials/{model_type}.json", "r") as f:
        return json.load(f)


def get_hyperparameters(trial, model_type):
    config = load_hyperparameter_config(model_type)
    params = {}
    for param_name, param_info in config.items():
        if param_info[0] == "int":
            params[param_name] = trial.suggest_int(param_name, param_info[1], param_info[2])
        elif param_info[0] == "float":
            params[param_name] = trial.suggest_float(param_name, param_info[1], param_info[2])
        elif param_info[0] == "categorical":
            # Konwersja wartości stringowych "true" i "false" na bool
            categorical_values = [param == "true" if param == "true" or param == "false" else param for param in param_info[1]]
            params[param_name] = trial.suggest_categorical(param_name, categorical_values)
        else:
            raise ValueError(f"Nieznany typ parametru: {param_info[0]}")
    return params


def create_model(model_type, params):
    if model_type == "Bagging":
        estimator = DecisionTreeClassifier(
            criterion=params.pop("criterion"),
            max_depth=params.pop("max_depth"),
            min_samples_split=params.pop("min_samples_split"),
            min_samples_leaf=params.pop("min_samples_leaf"),
            min_weight_fraction_leaf=params.pop("min_weight_fraction_leaf")
        )
        return BaggingClassifier(base_estimator=estimator, random_state=42, **params)
    elif model_type == "GradientBoosting":
        return GradientBoostingClassifier(random_state=42, **params)
    elif model_type == "HistGradientBoosting":
        return HistGradientBoostingClassifier(random_state=42, **params)
    elif model_type == "KNeighbors":
        return KNeighborsClassifier(**params)
    elif model_type == "RandomForest":
        return RandomForestClassifier(random_state=42, **params)
    elif model_type == "Stacking":
        base_models = [
            ('rf', RandomForestClassifier(n_estimators=params.pop("rf_n_estimators"), max_depth=params.pop("rf_max_depth"),
                                          criterion=params.pop("rf_criterion"), min_samples_split=params.pop("rf_min_samples_split"),
                                          min_samples_leaf=params.pop("rf_min_samples_leaf"), random_state=42)),
            # Add other base models as needed
        ]
        final_estimator_params = {
            'C': params.pop("logreg_C")
        }
        final_estimator = LogisticRegression(**final_estimator_params, max_iter=1000)
        return StackingClassifier(estimators=base_models, final_estimator=final_estimator, cv=5)
    elif model_type == "Voting":
        clf_rf = RandomForestClassifier(n_estimators=params.pop("rf_n_estimators"), max_depth=params.pop("rf_max_depth"),
                                        criterion=params.pop("rf_criterion"), min_samples_split=params.pop("rf_min_samples_split"),
                                        min_samples_leaf=params.pop("rf_min_samples_leaf"), random_state=42)
        clf_gb = HistGradientBoostingClassifier(learning_rate=params.pop("gb_learning_rate"), max_iter=params.pop("gb_max_iter"),
                                                max_depth=params.pop("gb_max_depth"), random_state=42)
        clf_knn = KNeighborsClassifier(n_neighbors=params.pop("knn_n_neighbors"), weights=params.pop("knn_weights"))
        clf_et = ExtraTreesClassifier(n_estimators=params.pop("et_n_estimators"), max_depth=params.pop("et_max_depth"),
                                      criterion=params.pop("et_criterion"), min_samples_split=params.pop("et_min_samples_split"),
                                      min_samples_leaf=params.pop("et_min_samples_leaf"), random_state=42)
        return VotingClassifier(estimators=[('rf', clf_rf), ('gb', clf_gb), ('knn', clf_knn), ('et', clf_et)], voting=params.pop("voting_type"))
    elif model_type == "MLP":
        hidden_layer_sizes = (params.pop("hidden_layer_size1"), params.pop("hidden_layer_size2"))
        return MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, random_state=42, **params)
    elif model_type == "AdaBoost":
        estimator = DecisionTreeClassifier(
            max_depth=params.pop("base_estimator_max_depth"),
            min_samples_split=params.pop("base_estimator_min_samples_split"),
            min_samples_leaf=params.pop("base_estimator_min_samples_leaf")
        )
        return AdaBoostClassifier(estimator=estimator, random_state=42, **params)
    elif model_type == "ExtraTrees":
        return ExtraTreesClassifier(random_state=42, **params)
    else:
        raise ValueError(f"Nieznany typ modelu: {model_type}")


def objective(trial, model_type, training_set=wmii, validation_set=user_area, stride=720):
    las = training_set[::720]
    las2 = validation_set[::30]

    X_train, X_test, y_train, y_test = prepare_data(las, purpose="training")
    test_features, test_labels = prepare_data(las2, purpose="prediction")

    params = get_hyperparameters(trial, model_type)
    clf = create_model(model_type, params)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)
    return accuracy


