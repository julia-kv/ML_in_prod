import os
import pickle
import pandas as pd
import click
from sklearn.preprocessing import StandardScaler
import logging
import pathlib

logger = logging.getLogger("Preprocess")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def transform_data(data):
    feature_columns: object = data.columns.tolist()

    scaler = StandardScaler()
    features = scaler.fit_transform(data)
    features_df = pd.DataFrame(features)
    features_df.columns = feature_columns
    return features_df, scaler


@click.command("preprocess")
@click.argument("input_path")
@click.argument("preprocessed-path")
@click.argument("transform-path")
def preprocess(input_path: str, preprocessed_path: str, transform_path: str) -> None:
    parent_path = pathlib.Path(__file__).absolute().parent.parent.parent
    full_input_path = parent_path.joinpath(str(input_path))
    full_preprocessed_path = parent_path.joinpath(str(preprocessed_path))
    full_transform_path = parent_path.joinpath(str(transform_path))

    dataframe = pd.read_csv(full_input_path.joinpath("data.csv"), index_col=0)
    target = dataframe["target"]
    features = dataframe.drop(["target"], axis=1)

    logger.info(f"Read data from {full_input_path!r} {dataframe.shape}")

    transformed_features, transformer = transform_data(features)
    new_data = transformed_features.merge(target, right_index=True, left_index=True)

    os.makedirs(full_preprocessed_path, exist_ok=True)
    new_data.to_csv(full_preprocessed_path.joinpath("data.csv"))
    logger.info(f"Write transformed data to {full_preprocessed_path!r}")

    os.makedirs(full_transform_path, exist_ok=True)
    with open(full_transform_path.joinpath("scaler.pkl"), "wb") as handler:
        pickle.dump(transformer, handler)
    logger.info(f"Write transformer to {full_transform_path!r}")


if __name__ == "__main__":
    preprocess()
