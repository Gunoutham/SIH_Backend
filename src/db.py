import psycopg2 as pg


HOST = "localhost"
PORT = "5432"
PASSWORD = "1234"
USERNAME = "postgres"
DATABASE = "postgres"

def get_db_connection():
    return pg.connect(host=HOST, port=PORT, password=PASSWORD, user=USERNAME, database=DATABASE)