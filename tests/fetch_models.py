from azure.storage.blob import BlobServiceClient
import os

blob_names = ["AdaBoostClassifier731.joblib",
              "BaggingClassifier650.joblib",
              "ExtraTreesClassifier851.joblib",
              "GradientBoostingClassifier653.joblib",
              "HistGradientBoostingClassifier720.joblib",
              "KNeighborsClassifier795.joblib",
              "RandomForestClassifier851.joblib",
              "StackingClassifier673.joblib",
              "VotingClassifier751.joblib"]

container_name = "kontenernadrzewa"

blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

for blob_name in blob_names:
    local_file_path = f'neptunseye/resources/models/{blob_name}'

    if not os.path.exists(local_file_path):
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        blob_data = blob_client.download_blob().readall()
        with open(local_file_path, 'wb') as file:
            file.write(blob_data)
