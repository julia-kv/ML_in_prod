from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator

from pendulum import today
from datetime import timedelta
from airflow.models import Variable
from docker.types import Mount

MOUNT_DIR = Variable.get("MOUNT_DIR")
default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
        "generate_data",
        default_args=default_args,
        description="A DAG to generate synthetic data",
        schedule_interval="@daily",
        start_date=today("UTC").add(days=-2),
) as dag:
    start = EmptyOperator(task_id="Start generate data")

    download = DockerOperator(
        dag=dag,
        task_id="Load_data",
        image="airflow-generate",
        # command=["data/raw", ],  # Does not work
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=MOUNT_DIR, target="/data", type="bind")]
    )
    finish = EmptyOperator(task_id="Finish generate data")

    start >> download >> finish
