from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
import json
import requests

# Define default_args for the DAG
default_args = {
    'owner': 'NicoB',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def create_table_if_not_exists():
    """
    Create the coin_data table if it doesn't exist in the database.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS coin_data(
        coin_id VARCHAR NOT NULL,
        date DATE NOT NULL,
        price_usd FLOAT,
        json_response JSON
    );
    """
    pg_hook = PostgresHook(postgres_conn_id="postgres_connection")
    pg_hook.run(create_table_sql)


def fetch_and_store_data_for_date(date, coin_id):
    """
    Fetch crypto data for a specific date and store it in the database.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date}"
    response = requests.get(url)
    data = response.json()

    price_usd = data['market_data']['current_price']['usd']
    json_response = json.dumps(data)
    formatted_date = datetime.strptime(date, '%d-%m-%Y')

    insert_query = """
        INSERT INTO coin_data (coin_id, price_usd, date, json_response)
        VALUES (%s, %s, %s, %s);
    """

    values = (coin_id, price_usd, formatted_date, json_response)

    pg_hook = PostgresHook(postgres_conn_id="postgres_connection")
    pg_hook.run(insert_query, parameters=values)


def fetch_and_store_data_for_range(start_date, end_date, coin_id):
    """
    Fetch and store crypto data for a date range.
    """
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime('%d-%m-%Y')
        fetch_and_store_data_for_date(formatted_date, coin_id)
        current_date += timedelta(days=1)


# Define the DAG
with DAG('crypto_data_download',
         default_args=default_args,
         schedule_interval=timedelta(days=1),
         catchup=False,) as dag:

    create_table_task = PythonOperator(
        task_id='create_table_task',
        python_callable=create_table_if_not_exists,
    )

    fetch_and_store_task = PythonOperator(
        task_id='fetch_and_store_task',
        python_callable=fetch_and_store_data_for_range,
        op_args=[
            datetime.strptime(Variable.get("start_date"), '%d-%m-%Y'),
            datetime.strptime(Variable.get("end_date"), '%d-%m-%Y'),
            Variable.get("coin_id")
        ],
        provide_context=True,
    )

# Set task dependencies
create_table_task >> fetch_and_store_task


if __name__ == "__main__":
    dag.cli()
