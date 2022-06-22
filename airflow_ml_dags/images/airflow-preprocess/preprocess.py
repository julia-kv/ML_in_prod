import os
import pickle
import pandas as pd
import click
from sklearn.preprocessing import MinMaxScaler


@click.command("preprocess")
@click.argument("input-dir")
@click.argument("output-dir")
def preprocess(input_dir: str, output_dir):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=False)
    target = pd.read_csv(os.path.join(input_dir, "target.csv"), index_col=False)

    scaler = MinMaxScaler()

    data[data.columns] = scaler.fit_transform(data[data.columns])
    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(os.path.join(output_dir, "data.csv"))
    target.to_csv(os.path.join(output_dir, "target.csv"))

    with open(os.path.join(output_dir, "scaler.pkl"), "wb") as handle:
        pickle.dump(scaler, handle)


if __name__ == "__main__":
    preprocess()
