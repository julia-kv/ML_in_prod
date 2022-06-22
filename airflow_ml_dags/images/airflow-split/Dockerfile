FROM airflow-ml-base:latest

COPY split.py /split.py

ENTRYPOINT ["python", "split.py"]
CMD ["/data/processed", "/data/split"]