import mysql.connector
from configparser import ConfigParser


def read_db_config(filename='config/config.ini', section='mysql'):
    # Create a parser object
    parser = ConfigParser()
    # Read the configuration file
    parser.read(filename)
    # Get the section from the configuration file
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    return db


host = "localhost"
database = "postgraduate"
user = "root"
password = "root"


import mysql.connector

def connect_to_database():
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print('Connected to the MySQL database')
            return conn
    except Exception as e:
        print(f'Error connecting to the database: {e}')
        return None

