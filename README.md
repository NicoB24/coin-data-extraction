# Coin data extraction 

## Version 📌

Python version: Python 3.9.2

## Installation ⚙️

_Go to the airflow directory (only for this 2 commands)  and run the docker containers:_
```
docker-compose up airflow-init
docker-compose up -d
```

For running Python, I suggest using a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments)

_Create a virtualenv:_
```
python3 -m venv env
```

_Activate virtualenv:_
```
source env/bin/activate
```

_Install requirements:_
```
pip3 install -r requirements.txt
```

_Create tables:_
```
python3 db/create_tables.py
```


## Run 🚀
```
python3 coin_data_download_and_store.py --date 2017-12-30 bitcoin 
python3 coin_data_download_and_store.py --start_date 2017-12-28 --end_date 2017-12-30 bitcoin
```

You can also use --storage as another parameter to choose between locally or database
```
python3 coin_data_download_and_store.py --start_date 2017-01-28 --end_date 2017-02-03 --storage database bitcoin
python3 coin_data_download_and_store.py --date 2017-12-30  --storage database bitcoin
```

To run the tests:
```
pytest
```

To run the lint:
```
flake8
```

If you want to see the data using a client, you can use for example DBeaver and connect to the local database with this credentials:
```
host: localhost
database: postgres
username: airflow
password: airflow
```

In order to run the ETL in Airflow, you have to follow these steps:
- Create a new database in your postgres called 'airflow_db'
- Open your browser and go to 'http://localhost:8080/'. In the top bar, go to Admin->Connections and configure the postgres connection with this parameters:
```
Connection Id: postgres_connection
Connection Type: Postgres
Host: postgres
Schema: airflow_db
Login: airflow
Password: airflow
Port: 5432
```
- In the top bar, go to Admin->Variables and create the next variables:
```
coin_in with value bitcon
end_date with value 15-01-2017
start_date with value 13-01-2017
```
Take into account that you can choose other values. In the top bar select DAGs, you can find the created DAG with the name 'crypto_data_download'. The table does not have a restriction, so you can insert the same row multiple times by running the DAG with the same coin and date range.


## Documentation (and comments) 📋
First and second exercises:
The entry point of the code is 'coin_data_download_and_store.py'. This file is where the validation of the input arguments is done and where the download and store methods are called. The others methods are self explained by the file/class name.

- The script only accepts dates in the format YYYY-MM-DD. The standard also accepts YYYYMMDD, so this could be a possible improvement of the code.
- I didn't do create the cron job, but this could be done using Celery or creating a cron job in the operating system.
- I avoid adding extra comments in the code, most of the methods are pretty simple (no tricky logic/algorithms), but another possible improvement of the code could be adding comments in the code (for example for the method that bulk download the files)
- For the database, I use the same as used in airflow, this is the reason why it is created from the airflow folder.
- The table created should have primary key, in this version it will allow replicated rows, which is not correct (I forgot to add this restriction).
- One possible improvement is to refactor the download class to has only one method which downloads one or more files without calling differents methods.

Third exercise:
The queries are in the 'db/queries/exercise3_queries.py' file. Both queries are done using the naming of the provided script to create and populate the databases. I want to remark that I did use another names for the tables, but because of the requests restriction of the endpoint, I prefer to use the provided data. For the second query I had to do a lot of reasearch and ask some things to chatGPT. I am not an expert using window functions

Fourth exercise:
In order to be fast, I used this [docker-compose](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml) as template for the creation of Airflow with Celery executor and Postgresql in Docker.
