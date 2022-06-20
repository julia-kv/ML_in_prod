import pathlib
import pickle
import pandas as pd
import logging
import click

logger = logging.getLogger('Load')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


@click.command("load-data")
@click.option("--input-path")
def load_data(input_path: str) -> None:
    if not input_path:
        input_path = 'data'

    parent_path = pathlib.Path(__file__).parent.parent.parent
    full_input_path = parent_path.joinpath(input_path)

    features = pd.read_csv(full_input_path.joinpath("data.csv"), index_col=0)
    target = pd.read_csv(full_input_path.joinpath("target.csv"), index_col=0)
    dataframe = features.merge(target, right_index=True, left_index=True)

    logger.info(f"Read data from {full_input_path!r} {dataframe.shape}")
    return dataframe


@click.command("load-model")
@click.option("--input-path")
def load_model(model_dir: str, file_name: str):
    parent_path = pathlib.Path(__file__).parent.parent.parent
    full_model_path = parent_path.joinpath(model_dir).joinpath(file_name)
    with open(full_model_path, "rb") as file:
        model = pickle.load(file)
    logger.info(f"Read model from {full_model_path!r}")
    return model


if __name__ == "__main__":
    pass
