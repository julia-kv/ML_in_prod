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
    data_col = data.columns.tolist()[-30:]
    scaled_data = scaler.fit_transform(data[data_col])

    new_data = pd.DataFrame(scaled_data, columns=data_col)

    os.makedirs(output_dir, exist_ok=True)
    new_data.to_csv(os.path.join(output_dir, "data.csv"))
    target.to_csv(os.path.join(output_dir, "target.csv"))

    with open(os.path.join(output_dir, "scaler.pkl"), "wb") as handle:
        pickle.dump(scaler, handle)


if __name__ == "__main__":
    pass
    # s1 = "/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/2022-06-22/generate/"
    # s2 = "/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/2022-06-22/processed/"
    preprocess()
