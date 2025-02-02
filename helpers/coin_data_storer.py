import datetime
import logging
import json
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text

from db.postgres_connection import PostgreSQLConnection
from db.queries.sql_queries import insert_coin_data


class DataStorer:
    def store(self, data, date, coin_id):
        pass


class LocalDataStorer(DataStorer):
    def store(self, data: str, date: str, coin_id: str) -> None:
        try:
            filename = f"{date}_{coin_id}.json"
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

            logging.info(f"Data saved locally in {filename}")
        except Exception as e:
            logging.error(f"Error while saving data locally: {e}")


class DatabaseDataStorer(DataStorer):
    def __init__(self):
        self.db = PostgreSQLConnection(username='airflow', password='airflow', host='localhost', port=5432, database_name='postgres')
        self.db.connect()
        self.session = self.db.get_session()

    def store(self, data: str, date: str, coin_id: str) -> None:
        self.insert_data_into_coin_data_table(data, date)

    def close_connection(self) -> None:
        self.session.close()
        self.db.close()

    def insert_data_into_coin_data_table(self, coin_data: json, date: str) -> None:
        coin_id = coin_data['id']
        price_usd = coin_data['market_data']['current_price']['usd']
        date = datetime.datetime.strptime(date, "%d-%m-%Y")

        json_response = json.dumps(coin_data)

        try:
            stmt = text(insert_coin_data)
            self.session.execute(stmt, {'coin_id': coin_id, 'price_usd': price_usd, 'date': date, 'json_response': json_response})
            self.session.commit()
            print("Data inserted into coin_data table successfully.")
        except ProgrammingError as e:
            self.session.rollback()
            print("Error inserting data into coin_data table:", e)
