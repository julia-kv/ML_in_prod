import os
import click
from sklearn.datasets import load_breast_cancer


@click.command("download")
@click.argument("output_dir")
def download(output_dir: str):
    data, target = load_breast_cancer(return_X_y=True, as_frame=True)

    df = data.reset_index(drop=True)
    tar_df = target.reset_index(drop=True)

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(os.path.join(output_dir, "data.csv"))
    tar_df.to_csv(os.path.join(output_dir, "target.csv"))


if __name__ == '__main__':
    download()
