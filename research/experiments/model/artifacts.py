import wandb
import joblib


def build_model_and_log(config, model):
    """
        Create and log a model artifact with specified configuration using wandb.
    """
    model_artifact = wandb.Artifact(
        "convnet", type="model",
        description="Simple AlexNet style CNN",
        metadata=dict(config))

    joblib.dump(model, "RandomForest.joblib")
    model_artifact.add_file("RandomForest.joblib")
    wandb.save("RandomForest.joblib")

    return model
