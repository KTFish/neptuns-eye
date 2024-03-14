import os
from preprocess import *
from train import *
from saving import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def main():
    # test = laspy.read("../data/WMII.las")
    # column_names = [dimension.name for dimension in test.point_format.dimensions]
    # print(column_names)

    # las file to DataFrame:
    filepath = "../data/WMII_CLASS.las"
    wmii_df = read_las_file(filepath)
    # kortowo = read_las_file("../data/Kortowo.las")
    # print(wmii_df)

    # Datesets:
    X_train, X_test, y_train, y_test = prepare_data_training(wmii_df, "classification", sample_rate=0.1, random_state=420)
    # print(f"X_train: {len(X_train)} | X_test: {len(X_test)} | y_train: {len(y_train)} | y_test {len(y_test)}")


    # Training:
    # preds, model_0 = random_forest_classification(X_train, X_test, y_train, y_test)
    # preds, model_1 = train(X_train, X_test, y_train, y_test, model=KNeighborsClassifier, n=10)
    # preds, model_2 = svc_classification(X_train, X_test, y_train, y_test)
    preds, model_3 = radius_neighbors_classification( X_train, X_test, y_train, y_test)

    # Saving model
    save_model(model_3, "../models/radius_neighbors_classification.joblib")

    #Loading models
    # model_2_loaded = load_model("../models/model_2.joblib")

    # Kortowo prediction
    # X_train, X_test, y_train, y_test = prepare_data_training(kortowo, "classification", sample_rate=0.1, random_state=2137)
    # preds = model_2_loaded.predict(X_test)
    # print(f"Accuracy on test set: {accuracy_score(y_test, preds)}")

    #Saving las file
    write_las_file(df=X_test, new_classification=preds, output_file_path="../data/radius_neighbors_classification.las")
    # las = laspy.read("../data/pred3.las")


if __name__ == '__main__':
    main()
