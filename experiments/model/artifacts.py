def create_model_artifact():
    pass


def build_model_and_log(config, model):
    # with wandb.init(project="artifacts-example", job_type="initialize", config=config) as run:
    # config = wandb.config

    model_artifact = wandb.Artifact(
        "convnet", type="model",
        description="Simple AlexNet style CNN",
        metadata=dict(config))

    joblib.dump(model, "RandomForest.joblib")
    # ➕ another way to add a file to an Artifact
    model_artifact.add_file("RandomForest.joblib")

    wandb.save("RandomForest.joblib")

    # run.log_artifact(model_artifact)
    return model


def create_dataset_artifact():
    pass