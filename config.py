import os
from dotenv import load_dotenv, find_dotenv
import urllib.parse

# SQLAlchemy
"""Configuration helpers.

This module exposes `DB_CONFIG` and `SQLALCHEMY_DATABASE_URL`.
Engine/session creation was intentionally removed from here to avoid
duplicate SQLAlchemy engines when importing both `config` and `database`.
Use `database.engine` / `database.SessionLocal` for DB access.
"""

# Load environment variables from .env if present (searches common locations)
load_dotenv(find_dotenv())

# Configuration read from environment variables. Do not store secrets in source.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "sistema_escolar"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432")
}


# SQLAlchemy engine and session
def _build_sqlalchemy_url():
    user = DB_CONFIG.get("user")
    pwd = DB_CONFIG.get("password")
    host = DB_CONFIG.get("host")
    port = DB_CONFIG.get("port")
    db = DB_CONFIG.get("database")
    # quote user/password to handle special characters safely
    user_q = urllib.parse.quote_plus(str(user)) if user is not None else ""
    pwd_q = urllib.parse.quote_plus(str(pwd)) if pwd is not None else ""
    return f"postgresql+psycopg2://{user_q}:{pwd_q}@{host}:{port}/{db}"

# Allow a full DATABASE_URL env var to override granular settings (12-factor)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or _build_sqlalchemy_url()


try:
    import psycopg2
    import psycopg2.extras

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
except Exception:
    # psycopg2 may not be available in certain environments; keep SQLAlchemy as primary path
    def get_connection():
        raise RuntimeError("psycopg2 not available")

    def dict_cursor(conn):
        raise RuntimeError("psycopg2 not available")

