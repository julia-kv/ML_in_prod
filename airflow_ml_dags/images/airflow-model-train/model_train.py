import os
import pathlib
import click
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger("Split")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


@click.command("train")
@click.argument("split-path")
@click.argument("model-path")
def train_model(split_path: str, model_path: str) -> None:

    model = LogisticRegression(random_state=13, max_iter=1000)

    parent_path = pathlib.Path(__file__).parent.parent.parent
    full_input_path = parent_path.joinpath(str(split_path))
    full_model_path = parent_path.joinpath(str(model_path))

    dataframe = pd.read_csv(full_input_path.joinpath("train.csv"), index_col=0)
    y_train = dataframe.target.values
    x_train = dataframe.drop(["target"], axis=1).values

    model.fit(x_train, y_train)

    os.makedirs(full_model_path, exist_ok=True)
    with open(full_model_path.joinpath("model.pkl"), "wb") as handler:
        pickle.dump(model, handler)
    logger.info(f"Write model to {full_model_path!r}")


if __name__ == "__main__":
    train_model()
