from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgreSQLConnection:
    def __init__(self, username, password, host, port, database_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.connection_url = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
        self.engine = create_engine(self.connection_url)
        self.Session = sessionmaker(bind=self.engine)
        self.connection = None

    def connect(self):
        self.connection = self.engine.connect()
        return self.connection

    def get_session(self):
        return self.Session()

    def close(self):
        self.connection.close()
