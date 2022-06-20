import os
import pathlib
import click
import pickle
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("Split")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


@click.command("predict")
@click.argument("input-path")
@click.argument("prediction-path")
@click.argument("scaler-path")
@click.argument("model-path")
def predict(input_path: str, prediction_path: str, scaler_path: str, model_path: str) -> None:
    parent_path = pathlib.Path(__file__).parent.parent.parent

    full_input_path = parent_path.joinpath(str(input_path))
    full_prediction_path = parent_path.joinpath(str(prediction_path))
    full_scaler_path = parent_path.joinpath(str(scaler_path))
    full_model_path = parent_path.joinpath(str(model_path))

    with open(full_model_path.joinpath("model.pkl"), "rb") as handler:
        model = pickle.load(handler)
    with open(full_scaler_path.joinpath("scaler.pkl"), "rb") as handler:
        scaler = pickle.load(handler)

    data = pd.read_csv(full_input_path.joinpath("data.csv"), index_col=0)
    df = data.drop(columns='target')
    transformed_data = scaler.transform(df)
    prediction = model.predict(transformed_data)

    os.makedirs(full_prediction_path, exist_ok=True)
    np.savetxt(full_prediction_path.joinpath("predictions.csv"), prediction, delimiter=",")
    logger.info(f"Write prediction to {full_prediction_path!r}")


if __name__ == "__main__":
    predict()
