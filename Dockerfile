FROM apache/airflow:3.3.0
RUN pip install --no-cache-dir dbt-core==1.7.19 dbt-mysql==1.7.0
