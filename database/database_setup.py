import mysql.connector
from database_connection import cursor
from mysql.connector import errorcode
DB_NAME = 'leafsroster'

def create_database():
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    print(f"Database {DB_NAME} created!")


create_database()
