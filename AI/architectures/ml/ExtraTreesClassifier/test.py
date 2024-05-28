from AI.architectures.ml.predict import predict
from utils.data_visualizations import make_confusion_matrix, print_classification_report
from config import wmii_filtered, user_area_filtered
from storage.load import load_joblib

model = load_joblib("saved_models/ExtraTreesClassifier680.joblib")

preds, y_test = predict(user_area_filtered, model)

make_confusion_matrix(y_test, preds)




