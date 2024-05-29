from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def prepare_data(df, test_size=0.3, random_state=42, columns_to_keep=None, purpose='prediction'):
    if columns_to_keep is None:
        columns_to_keep = ["X", "Y", "Z", "intensity", "number_of_returns", "classification", "red", "green", "blue"]

    allowed_purposes = {'prediction', 'training'}

    if purpose not in allowed_purposes:
        raise ValueError(f"Nieznany typ danych: {purpose}. Dozwolone wartości to: {', '.join(allowed_purposes)}")

    missing_columns = [col for col in columns_to_keep if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Brakujące kolumny w DataFrame: {', '.join(missing_columns)}")

    df = df[columns_to_keep]
    features = df.drop(columns=["classification"])
    features = MinMaxScaler().fit_transform(features)
    labels = df["classification"]

    if purpose == 'prediction':
        # Logika dla danych predykcji
        return features, labels
    elif purpose == 'training':
        # Logika dla danych treningowych
        return train_test_split(features, labels, test_size=test_size, random_state=random_state)
