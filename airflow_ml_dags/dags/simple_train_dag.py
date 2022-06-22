# import os
# import pickle
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import f1_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# import pathlib
#
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
#
# from pendulum import today
# from datetime import timedelta
#
# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": today("UTC").add(days=-9),
#     "email": ["airflow@example.com"],
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
# }
#
#
# def transform_data(data):
#     feature_columns: object = data.columns.tolist()
#     scaler = StandardScaler()
#     features = scaler.fit_transform(data)
#     features_df = pd.DataFrame(features)
#     features_df.columns = feature_columns
#     return features_df, scaler
#
#
# def preprocess() -> None:
#     parent_path = pathlib.Path(__file__).parent.parent
#     full_input_path = parent_path.joinpath('data/raw')
#     full_preprocessed_path = parent_path.joinpath('data/preprocess')
#
#     data = pd.read_csv(full_input_path.joinpath('data.csv'), index_col=0)
#     target = data["target"]
#     features = data.drop(["target"], axis=1)
#
#     new_data, transformer = transform_data(features)
#
#     os.makedirs(full_preprocessed_path, exist_ok=True)
#     new_data.to_csv(full_preprocessed_path.joinpath('data.csv'))
#     target.to_csv(full_preprocessed_path.joinpath('target.csv'))
#
#     with open(full_preprocessed_path.joinpath('scaler.pkl'), "wb") as handler:
#         pickle.dump(transformer, handler)
#
#
# def split() -> None:
#     parent_path = pathlib.Path(__file__).parent.parent
#     full_preprocessed_path = parent_path.joinpath('data/preprocess')
#     full_output_path = parent_path.joinpath('data/split')
#
#     data = pd.read_csv(full_preprocessed_path.joinpath("data.csv"), index_col=0)
#     target = pd.read_csv(full_preprocessed_path.joinpath("target.csv"), index_col=0)
#     data_train, data_val, target_train, target_val = train_test_split(data, target, random_state=42)
#
#     os.makedirs(full_output_path, exist_ok=True)
#     data_train.to_csv(full_output_path.joinpath('data_train.csv'))
#     data_val.to_csv(full_output_path.joinpath('data_val.csv'))
#     target_train.to_csv(full_output_path.joinpath('target_train.csv'))
#     target_val.to_csv(full_output_path.joinpath('target_val.csv'))
#
#
# def train_model() -> None:
#     parent_path = pathlib.Path(__file__).parent.parent
#     full_input_path = parent_path.joinpath('data/split')
#     full_model_path = parent_path.joinpath('data/models')
#
#     data = pd.read_csv(full_input_path.joinpath("data_train.csv"), index_col=0)
#     target = pd.read_csv(full_input_path.joinpath("target_train.csv"), index_col=0)
#
#     model = LogisticRegression(random_state=13, max_iter=1000)
#     model.fit(data, target)
#
#     os.makedirs(full_model_path, exist_ok=True)
#     with open(full_model_path.joinpath('model.pkl'), "wb") as handler:
#         pickle.dump(model, handler)
#
#
# def validate():
#     parent_path = pathlib.Path(__file__).parent.parent
#     full_input_path = parent_path.joinpath('data/split')
#     full_model_path = parent_path.joinpath('data/models')
#
#     data = pd.read_csv(full_input_path.joinpath('data_val.csv'), index_col=0)
#     target = pd.read_csv(full_input_path.joinpath('target_val.csv'), index_col=0)
#
#     with open(full_model_path.joinpath('model.pkl'), "rb") as f:
#         model = pickle.load(f)
#
#     metric = f1_score(target, model.predict(data).round())
#
#     with open(full_model_path.joinpath('model.pkl'), 'wb') as f:
#         pickle.dump({'model': model, "f1_score": metric}, f)
#
#
# with DAG(
#     dag_id="simple_model_train",
#     default_args=default_args,
#     schedule_interval="@weekly",
# ) as dag:
#     processing = PythonOperator(
#         task_id="processing",
#         python_callable=preprocess,
#     )
#
#     splitting = PythonOperator(
#         task_id="splitting",
#         python_callable=split,
#     )
#
#     training = PythonOperator(
#         task_id="training",
#         python_callable=train_model,
#     )
#
#     validate = PythonOperator(
#         task_id="validating",
#         python_callable=validate,
#     )
#
#     processing >> splitting >> training >> validate
