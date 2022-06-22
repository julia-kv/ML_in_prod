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
        "train_dag",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=today("UTC").add(days=-5),
) as dag:

    # start = EmptyOperator(task_id="start_train_model")

    preprocess = DockerOperator(
        image="airflow-preprocess",
        task_id="docker-airflow-preprocess",
        command=["/data/{{ ds }}/generate/", "/data/{{ ds }}/processed/"],
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/", target="/data",
                      type='bind')]
    )

    split = DockerOperator(
        image="airflow-split",
        task_id="docker-airflow-split",
        command=["/data/{{ ds }}/processed/", "/data/{{ ds }}/split/"],
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/", target="/data",
                      type='bind')]
    )

    train = DockerOperator(
        image="airflow-model-train",
        task_id="docker-airflow-train",
        command=["/data/{{ ds }}/split/", "/data/{{ ds }}/models/"],
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source="/home/julia/git/techno/ML/julia_korpusova/airflow_ml_dags/data/", target="/data",
                      type='bind')]
    )

    finish = EmptyOperator(task_id="finish_train_model")

    preprocess >> split >> train >> finish
