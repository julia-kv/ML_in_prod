from datetime import timedelta
from pendulum import today
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount
from airflow.models import Variable

MOUNT_DIR = Variable.get("MOUNT_DIR")
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
TRANSFORM_DIR = "data/transform"
SPLIT_DIR = "data/split"
MODEL_DIR = "data/models"

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
        "train_model",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=today('UTC').add(days=-3)
) as dag:
    data_sensor = FileSensor(
        task_id="data_sensor",
        filepath="/data/raw/data.csv"
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        # command="python preprocess.py {{ RAW_DIR }} {{ PROCESSED_DIR }} {{TRANSFORM_DIR}}",
        task_id="preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=MOUNT_DIR, target="/data", type="bind")]
    )

    train_val_split = DockerOperator(
        image="airflow-split",
        # command="python split.py {{ PROCESSED_DIR }} {{ SPLIT_DIR }}",
        task_id="train_val_split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=MOUNT_DIR, target="/data", type="bind")]
    )

    train_model = DockerOperator(
        image="airflow-model-train",
        # command="python train_model.py {{ SPLIT_DIR }} {{ MODEL_DIR }}",
        task_id="train_model",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=MOUNT_DIR, target="/data", type="bind")]
    )

    data_sensor >> preprocess >> train_val_split >> train_model
