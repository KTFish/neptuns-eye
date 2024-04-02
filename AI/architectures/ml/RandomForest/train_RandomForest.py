from sklearn.ensemble import RandomForestClassifier
from architectures.ml.train import *
from architectures.ml.predict import *
from storage.load import read_las_file
from experiments.sweeps.RandomForest_config import *
from experiments.sweeps.RandomForest_config import sweep_config
from experiments.sweeps.train import train

wmii = read_las_file("../../../data/train/WMII_CLASS.las")
test = read_las_file("../../../data/test/USER AREA.las")

clf = RandomForestClassifier(n_estimators=10, random_state=2137)
model, preds = train_ml(wmii, clf)

preds_test = predict(test, model)

sweep_config1 = {
    'method': 'random',
    'metric': {
      'name': 'accuracy',
      'goal': 'maximize'
    },
    'parameters': {
        'n_estimators': {
            'values': [10, 15, 20]
        },
        'max_depth': {
            'values': [None, 10, 20, 30]
        }
    }
}


def train_model(df, target_column="classification", sample_rate=0.1, test_size=0.2, random_state=42):
    # Definicja wewnętrznej funkcji trenującej
    def train():
        # Inicjalizacja sesji wandb
        with wandb.init() as run:
            config = run.config

            # Wczytanie danych - załóżmy, że funkcja prepare_data_training jest zdefiniowana gdzie indziej
            X_train, X_test, y_train, y_test = prepare_data_training(df, target_column, sample_rate, test_size, random_state)

            # Tworzenie i trenowanie modelu
            model = RandomForestClassifier(n_estimators=config.n_estimators, max_depth=config.max_depth)
            model.fit(X_train, y_train)

            # Predykcje i ocena modelu
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)

            # Rejestracja metryki
            wandb.log({'accuracy': accuracy})

    return train


# Inicjalizacja sweep
sweep_id = wandb.sweep(sweep=sweep_config1, project="random_forest_sweep")

# Definiowanie funkcji trenującej z dostępem do df
train_function = train_model(wmii)

# Dołączenie do sweep i rozpoczęcie trenowania
wandb.agent(sweep_id, train_function)

if __name__ == '__main__':
    # Setup model
    # Train
    train(config)