from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.slack import SlackAPIPostOperator
from datetime import datetime, timedelta
# DAG settings
default_args = {
    "start_date": datetime(2025, 3, 13),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
with DAG("dbt_airflow_pipeline",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dag:
    # Task 1: Run dbt models
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="dbt build",
    )
    # Task 2: Send Slack Alert on Failure
    slack_alert = SlackAPIPostOperator(
        task_id="slack_alert",
        token="slack-api-token",
        text="🚨 dbt run failed in Airflow! Check logs.",
        channel="#alerts",
        trigger_rule="one_failed"
    )
    # Task dependencies
    dbt_build >> slack_alert