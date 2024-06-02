from AI.architectures.ml.predict import predict
from utils.data_visualizations import make_confusion_matrix
from config import wmii, user_area
from storage.load import load_joblib
from sklearn.metrics import accuracy_score

model = load_joblib("rf_kek.joblib")

user_area = user_area[::30]

preds, y_test = predict(user_area, model)

make_confusion_matrix(y_test, preds)

print(accuracy_score(y_test, preds))