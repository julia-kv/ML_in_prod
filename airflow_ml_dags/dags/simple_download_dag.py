# import os
# import pathlib
# import random
# from sklearn.datasets import load_breast_cancer
# from sklearn.utils import shuffle
# from pendulum import today
# from datetime import timedelta
#
# import pandas as pd
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
#
#
# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": today("UTC").add(days=-10),
#     "email": ["airflow@example.com"],
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
# }
#
#
# def make_data():
#     num = random.randint(50, 568)
#     data, target = load_breast_cancer(return_X_y=True, as_frame=True)
#     daff = pd.concat([data, target], axis=1)
#     df = shuffle(daff)
#     df.reset_index(inplace=True, drop=True)
#     return df[:num]
#
#
# def generate_data() -> None:
#     parent_path = pathlib.Path(__file__).parent.parent
#     full_output_path = parent_path.joinpath('data/raw')
#
#     data = make_data()
#
#     os.makedirs(full_output_path, exist_ok=True)
#     data.to_csv(full_output_path.joinpath("data.csv"))
#
#
# with DAG(
#         dag_id="simple_download_dag",
#         default_args=default_args,
#         schedule_interval="@daily",
# ) as dag:
#     generator = PythonOperator(
#         task_id="generate_data",
#         python_callable=generate_data
#     )
#
#     generator
