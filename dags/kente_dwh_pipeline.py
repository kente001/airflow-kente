from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.providers.standard.operators.bash import BashOperator

DBT = "dbt --no-use-colors"
DIRS = "--project-dir /opt/airflow/kente_dw --profiles-dir /opt/airflow/dbt-profiles"

default_args = {
    "owner": "kente",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="kente_dwh_pipeline",
    description="Bronze-to-gold warehouse build: silver models, tests, snapshot, gold star schema",
    start_date=datetime(2026, 7, 1),
    schedule="0 6 * * *",          # daily, 06:00
    catchup=False,
    default_args=default_args,
    tags=["dbt", "kente_dw"],
) as dag:

    run_silver = BashOperator(
        task_id="dbt_run_silver",
        bash_command=f"{DBT} run --select silver {DIRS}",
    )

    test_silver = BashOperator(
        task_id="dbt_test_silver",
        bash_command=f"{DBT} test --select silver {DIRS}",
    )

    snapshot_costs = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f"{DBT} snapshot {DIRS}",
    )

    run_gold = BashOperator(
        task_id="dbt_run_gold",
        bash_command=f"{DBT} run --select gold {DIRS}",
    )

    test_gold = BashOperator(
        task_id="dbt_test_gold",
        bash_command=f"{DBT} test --select gold {DIRS}",
    )

    run_silver >> test_silver >> snapshot_costs >> run_gold >> test_gold