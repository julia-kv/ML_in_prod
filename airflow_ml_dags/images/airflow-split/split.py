import os
import pathlib
import click
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger("Split")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


@click.command("split")
@click.argument("preprocessed-path")
@click.argument("split-path")
def split(preprocessed_path: str, split_path: str) -> None:
    parent_path = pathlib.Path(__file__).parent.parent.parent
    full_preprocessed_path = parent_path.joinpath(str(preprocessed_path))
    full_output_path = parent_path.joinpath(str(split_path))

    dataframe = pd.read_csv(full_preprocessed_path.joinpath("data.csv"), index_col=0)
    logger.info(f"Read data from {full_preprocessed_path!r} {dataframe.shape}")

    train, val = train_test_split(dataframe, random_state=13,)

    os.makedirs(full_output_path, exist_ok=True)
    train.to_csv(full_output_path.joinpath("train.csv"))
    val.to_csv(full_output_path.joinpath("val.csv"))
    logger.info(f"Write split data to {full_output_path!r}")


if __name__ == "__main__":
    split()
