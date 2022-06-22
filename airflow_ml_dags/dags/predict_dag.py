from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator

from pendulum import today
from datetime import timedelta
from airflow.models import Variable
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
        "predict_dag",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=today("UTC").add(days=-3),
) as dag:

    predict = DockerOperator(
        image="airflow-predict",
        task_id="docker-airflow-predict",
        command=["/data/{{ ds }}/raw/", "/data/{{ ds }}/processed/", "/data/{{ ds }}/models/",
                 "/data/{{ ds }}/prediction/"],
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/", target="/data",
                      type='bind')]
    )

    finish = EmptyOperator(task_id="finish_predict")

    predict >> finish
