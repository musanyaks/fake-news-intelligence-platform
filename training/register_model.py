"""MLflow model registration."""

import argparse

import mlflow


def register(model_path: str, model_name: str, run_id: str = None):
    mlflow.set_tracking_uri("http://localhost:5000")

    if run_id:
        result = mlflow.register_model(f"runs:/{run_id}/model", model_name)
    else:
        result = mlflow.register_model(model_path, model_name)

    print(f"Registered model: {result.name} version {result.version}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--model-name", default="fake-news-model")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    register(args.model_path, args.model_name, args.run_id)


if __name__ == "__main__":
    main()
