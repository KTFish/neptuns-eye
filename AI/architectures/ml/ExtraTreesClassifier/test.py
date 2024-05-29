from AI.architectures.ml.predict import predict
from utils.data_visualizations import make_confusion_matrix
from config import wmii, user_area
from storage.load import load_joblib

model = load_joblib("saved_models/ExtraTreesClassifier558.joblib")

preds, y_test = predict(user_area, model)

make_confusion_matrix(y_test, preds)



