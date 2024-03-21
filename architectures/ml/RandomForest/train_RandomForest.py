from sklearn.ensemble import RandomForestClassifier
from architectures.ml.train import *
from architectures.ml.predict import *
from storage.load import read_las_file


wmii = read_las_file("../../../data/train/WMII_CLASS.las")
test = read_las_file("../../../data/test/USER AREA.las")
clf = RandomForestClassifier(n_estimators=10, random_state=2137)
model, preds = train_ml(wmii, clf, test_acc=True)

prediction = predict(test, model)
