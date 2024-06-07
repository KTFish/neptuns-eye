import optuna
from sklearn.neural_network import MLPClassifier
from preprocess.preprocess import prepare_data_training, prepare_data_prediction
from sklearn.metrics import accuracy_score
import sys
import os

sys.path.append(os.path.abspath('../../../'))
from config import wmii, user_area


def objective(trial, stride=40):
    las = wmii[::stride]
    las2 = user_area[::stride]

    X_train, X_test, y_train, y_test = prepare_data_training(las)
    test_features, test_labels = prepare_data_prediction(las2)

    mlp_hidden_layer_size1 = trial.suggest_int("hidden_layer_size1", 2, 500)
    mlp_hidden_layer_size2 = trial.suggest_int("hidden_layer_size2", 2, 500)
    mlp_activation = trial.suggest_categorical("activation", ["identity", "logistic", "tanh", "relu"])
    mlp_solver = trial.suggest_categorical("solver", ["lbfgs", "sgd", "adam"])
    mlp_alpha = trial.suggest_float("alpha", 1e-5, 1e-1, log=True)
    mlp_learning_rate = trial.suggest_categorical("learning_rate", ["constant", "invscaling", "adaptive"])
    mlp_max_iter = trial.suggest_int("max_iter", 100, 500)
    mlp_learning_rate_init = trial.suggest_float("learning_rate_init", 1e-5, 1e-1, log=True)
    mlp_power_t = trial.suggest_float("power_t", 0.1, 0.9)
    mlp_momentum = trial.suggest_float("momentum", 0.1, 0.9)
    mlp_early_stopping = trial.suggest_categorical("early_stopping", [True, False])
    mlp_validation_fraction = trial.suggest_float("validation_fraction", 0.1, 0.3)
    mlp_beta_1 = trial.suggest_float("beta_1", 0.1, 0.999)
    mlp_beta_2 = trial.suggest_float("beta_2", 0.1, 0.999)
    mlp_n_iter_no_change = trial.suggest_int("n_iter_no_change", 5, 50)

    clf = MLPClassifier(hidden_layer_sizes=(mlp_hidden_layer_size1, mlp_hidden_layer_size2),
                        activation=mlp_activation,
                        solver=mlp_solver,
                        alpha=mlp_alpha,
                        learning_rate=mlp_learning_rate,
                        max_iter=mlp_max_iter,
                        learning_rate_init=mlp_learning_rate_init,
                        power_t=mlp_power_t,
                        momentum=mlp_momentum,
                        early_stopping=mlp_early_stopping,
                        validation_fraction=mlp_validation_fraction,
                        beta_1=mlp_beta_1,
                        beta_2=mlp_beta_2,
                        n_iter_no_change=mlp_n_iter_no_change)

    clf.fit(X_train, y_train)
    preds = clf.predict(test_features)
    accuracy = accuracy_score(test_labels, preds)

    return accuracy


if __name__ == "__main__":

    folder_path = 'optuna_trials'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    storage_url = f"sqlite:///{folder_path}/MLPClassifier.db"
    study = optuna.create_study(direction="maximize", storage=storage_url)
    study.optimize(lambda trial: objective(trial, stride=45), n_trials=2)  # define a number of trials here
