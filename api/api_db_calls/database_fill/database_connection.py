import mysql.connector
from database_fill.confidential import *

config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME
}

TABLES = {}

db = mysql.connector.connect(**config)
cursor = db.cursor()

def create_database():
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    print(f"Database {DB_NAME} created!")


create_database()
