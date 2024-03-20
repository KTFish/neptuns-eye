from architectures.ml.RandomForest.train import *
from architectures.ml.RandomForest.predict import *
from utils.preprocess import *
from storage.load import *
from storage.save import *

def main():
    wmii = read_las_file("data/train/WMII_CLASS.las")
    # kortowo = read_las_file("data/test/Kortowo.las")
    test = read_las_file("data/test/WMII.las")

    # preds, model = random_forest_classification(wmii, save_path="experiments/model/RandomForest.joblib")
    model = load_model("experiments/model/RandomForest.joblib")

    preds = predict(wmii, model)



if __name__ == '__main__':
    main()
