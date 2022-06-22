import os
import click
import pickle
import pandas as pd
import logging

# logger = logging.getLogger("Split")
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
# logger.addHandler(handler)


@click.command("predict")
@click.argument("input-dir")
@click.argument("preprocess-dir")
@click.argument("model-dir")
@click.argument("output-dir")
def predict(input_dir: str, preprocess_dir: str, model_dir: str, output_dir: str):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))

    with open(os.path.join(preprocess_dir, "scaler.pkl"), "rb") as handle:
        scaler = pickle.load(handle)
    with open(os.path.join(model_dir, "model.pkl"), "rb") as handle:
        model = pickle.load(handle)

    transformed_data = scaler.transform(data)
    prediction = model.predict(transformed_data)
    # loger.info(f"DATA SHAPE {data.shape}")
    # loger.info(f"TARGET SHAPE {target.shape}")

    os.makedirs(output_dir, exist_ok=True)
    prediction.to_csv(os.path.join(output_dir, "prediction.csv"))


#
# @click.command("predict")
# @click.argument("input-path")
# @click.argument("prediction-path")
# @click.argument("scaler-path")
# @click.argument("model-path")
# def predict(input_path: str, prediction_path: str, scaler_path: str, model_path: str) -> None:
#     parent_path = pathlib.Path(__file__).parent.parent.parent
#
#     full_input_path = parent_path.joinpath(str(input_path))
#     full_prediction_path = parent_path.joinpath(str(prediction_path))
#     full_scaler_path = parent_path.joinpath(str(scaler_path))
#     full_model_path = parent_path.joinpath(str(model_path))
#
#     with open(full_model_path.joinpath("model.pkl"), "rb") as handler:
#         model = pickle.load(handler)
#     with open(full_scaler_path.joinpath("scaler.pkl"), "rb") as handler:
#         scaler = pickle.load(handler)
#
#     data = pd.read_csv(full_input_path.joinpath("data.csv"), index_col=0)
#     df = data.drop(columns='target')
#     transformed_data = scaler.transform(df)
#     prediction = model.predict(transformed_data)
#
#     os.makedirs(full_prediction_path, exist_ok=True)
#     np.savetxt(full_prediction_path.joinpath("predictions.csv"), prediction, delimiter=",")
#     logger.info(f"Write prediction to {full_prediction_path!r}")


if __name__ == "__main__":
    predict()
