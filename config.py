import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host": "dpg-d45qihchg0os73e5b2i0-a.oregon-postgres.render.com",
    "database": "test1_v02p",
    "user": "test1_v02p_user",
    "password": "gv5WuvRUhGrvLnDVfiEeaEEOe0QDGgPv",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )

def dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
