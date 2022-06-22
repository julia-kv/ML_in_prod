import os
import pathlib
import click
import pandas as pd
from random import randint
from sklearn.datasets import load_breast_cancer
from sklearn.utils import shuffle
import logging


@click.command("generate")
@click.argument("input-dir")
@click.argument("output-dir")
def generate_data(input_dir: str, output_dir: str):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"), index_col=False)
    target = pd.read_csv(os.path.join(input_dir, "target.csv"), index_col=False)

    data.reset_index(inplace=True, drop=True)
    os.makedirs(output_dir, exist_ok=True)

    data.to_csv(os.path.join(output_dir, "data.csv"))
    target.to_csv(os.path.join(output_dir, "target.csv"))


if __name__ == '__main__':
    generate_data()
