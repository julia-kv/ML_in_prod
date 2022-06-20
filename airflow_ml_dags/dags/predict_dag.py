from datetime import timedelta
from pendulum import today
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount
from airflow.models import Variable

MOUNT_DIR = Variable.get("MOUNT_DIR")

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
        "predict_data",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=today('UTC').add(days=-3)
) as dag:
    data_sensor = FileSensor(
        task_id="data_sensor",
        filepath="/opt/airflow/data/models/model.pkl"
    )

    predict = DockerOperator(
        image="airflow-predict",
        command="python model_predict.py data/raw data/predictions data/transform data/models",
        task_id="predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=MOUNT_DIR, target="/data", type="bind")]
    )

    data_sensor >> predict
