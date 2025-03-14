from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import balance_monitor

# Define default arguments for the DAG
default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 3, 14),  # Starting from today
}

# Create the DAG
dag = DAG(
    'daily_pipeline',
    default_args=default_args,
    description='Daily execution of DBT models and balance monitor script',
    schedule_interval='0 9 * * *',
    catchup=False,
)

script_path = 'balance_monitor.py'

# Task to run all DBT models
run_dbt_models = BashOperator(
    task_id='run_dbt_models',
    bash_command=f'dbt build',
    dag=dag,
)

# Define the task to run the balance monitor script
run_balance_monitor_task = PythonOperator(
    task_id='run_balance_monitor',
    python_callable=balance_monitor.main,
    dag=dag,
)

# Set the task dependencies
run_dbt_models >> run_balance_monitor_task

if __name__ == "__main__":
    dag.cli()