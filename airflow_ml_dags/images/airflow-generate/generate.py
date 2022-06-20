import os
import pathlib
import click
import pandas as pd
from random import randint
from sklearn.datasets import load_breast_cancer
from sklearn.utils import shuffle
import logging


logger = logging.getLogger("Generate")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def make_data():
    num = randint(50, 568)

    data, target = load_breast_cancer(return_X_y=True, as_frame=True)
    daff = pd.concat([data, target], axis=1)
    df = shuffle(daff)
    df.reset_index(inplace=True, drop=True)
    return df


@click.command("generate")
@click.argument("output-path", required=True)
def generate_data(output_path: str) -> None:
    logger.warning(output_path)
    data = make_data()

    parent_path = pathlib.Path(__file__).absolute().parent.parent.parent
    logger.warning(str(__file__))
    full_output_path = parent_path.joinpath(str(output_path))

    os.makedirs(full_output_path, exist_ok=True)

    data.to_csv(full_output_path.joinpath("data.csv"))
    logger.info(f"Generate data in {full_output_path!r}")

    temp_df = pd.read_csv(full_output_path.joinpath("data.csv"))
    logger.info(f"Files read from a {full_output_path.joinpath('data.csv')} directory into shape {temp_df.shape}")


if __name__ == '__main__':
    generate_data()
