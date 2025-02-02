from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.dialects.postgresql import JSON
from postgres_connection import PostgreSQLConnection

# Define the table classes using SQLAlchemy's declarative syntax
Base = declarative_base()


class CoinData(Base):
    __tablename__ = 'coin_data'

    id = Column(Integer, primary_key=True)
    coin_id = Column(String(255), nullable=False)
    price_usd = Column(Numeric(15, 2), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    json_response = Column(JSON, nullable=False)


class AggregatedData(Base):
    __tablename__ = 'aggregated_data'

    id = Column(Integer, primary_key=True)
    coin_id = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    max_value = Column(Numeric(15, 2), nullable=False)
    min_value = Column(Numeric(15, 2), nullable=False)


def create_tables_if_not_exist(engine):
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except ProgrammingError as e:
        print("Error creating tables:", e)


# PostgreSQL connection configuration
username = 'airflow'
password = 'airflow'
host = 'localhost'
port = 5432
database_name = 'postgres'

# Create PostgreSQLConnection instance
db = PostgreSQLConnection(username, password, host, port, database_name)
connection = db.connect()

# Create tables if they don't exist
create_tables_if_not_exist(db.engine)

# Close the connection
db.close()
