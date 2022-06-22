import os
import click
import pickle
import pandas as pd


@click.command("predict")
@click.argument("input-dir")
@click.argument("preprocess-dir")
@click.argument("model-dir")
@click.argument("output-dir")
def predict(input_dir: str, preprocess_dir: str, model_dir: str, output_dir: str):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=False)
    data_col = data.columns.tolist()[-30:]

    with open(os.path.join(preprocess_dir, "scaler.pkl"), "rb") as handle:
        scaler = pickle.load(handle)
    with open(os.path.join(model_dir, "model.pkl"), "rb") as handle:
        model = pickle.load(handle)

    transformed_data = scaler.transform(data[data_col])
    prediction = model.predict(transformed_data)

    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(prediction, columns=['target'])
    df.to_csv(os.path.join(output_dir, "prediction.csv"))


if __name__ == "__main__":
    predict()
