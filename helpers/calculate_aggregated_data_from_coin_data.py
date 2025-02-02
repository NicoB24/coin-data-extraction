from db.postgres_connection import PostgreSQLConnection  # Import your PostgreSQL connection class here
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from db.queries.sql_queries import insert_aggregated_data_from_coin_data  # Import your query from the other file


def connect_to_database():
    db = PostgreSQLConnection(username='airflow', password='airflow', host='localhost', port=5432, database_name='postgres')
    db.connect()
    return db.get_session()


def calculate_aggregated_data_from_coin_data(coin_id: str) -> None:
    session = connect_to_database()

    try:
        session.execute(text(insert_aggregated_data_from_coin_data), {'coin_id': coin_id})
        session.commit()
        print("Data inserted into aggregated_data table successfully.")
    except ProgrammingError as e:
        session.rollback()
        print("Error inserting data into aggregated_data table:", e)
    finally:
        session.close()
        session.bind.dispose()  # Close the connection
