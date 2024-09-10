# database/connect_db.py

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class ConnectDataBase:
    def __init__(self):
        self.__dbname = os.getenv('DB_NAME')
        self.__postgres_user = os.getenv('DB_USER')
        self.__postgres_password = os.getenv('DB_PASSWORD')
        self.__postgres_host = os.getenv('DB_HOST')
        self.__postgres_port = os.getenv('DB_PORT')

    def get_connection(self):
        conn = psycopg2.connect(
            dbname=self.__dbname,
            user=self.__postgres_user,
            password=self.__postgres_password,
            host=self.__postgres_host,
            port=self.__postgres_port
        )
        return conn

    def close_connection(self, conn):
        if conn:
            conn.close()