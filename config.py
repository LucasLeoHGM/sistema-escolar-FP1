import os
from dotenv import load_dotenv, find_dotenv
import urllib.parse

# SQLAlchemy configuration helpers
"""Configuration helpers.

This module exposes `SQLALCHEMY_DATABASE_URL` as the canonical DB URL
to be used by `database.py`. Prefer setting a full `DATABASE_URL` in
production; individual `DB_*` variables are supported as a development
convenience fallback.
"""

# Load environment variables from .env if present (searches common locations)
load_dotenv(find_dotenv())

# Prefer a single `DATABASE_URL` (12-factor). If not provided, build one from
# individual `DB_*` variables for convenience in development.
def _build_from_env():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "sistema_escolar")
    user = os.getenv("DB_USER", "postgres")
    pwd = os.getenv("DB_PASSWORD", "")
    user_q = urllib.parse.quote_plus(str(user)) if user is not None else ""
    pwd_q = urllib.parse.quote_plus(str(pwd)) if pwd is not None else ""
    return f"postgresql+psycopg2://{user_q}:{pwd_q}@{host}:{port}/{db}"

# Allow full `DATABASE_URL` to override the granular settings
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or _build_from_env()


try:
    import psycopg2
    import psycopg2.extras

    def get_connection():
        # If a full DATABASE_URL is configured, pass it as DSN to psycopg2.
        dsn = os.getenv("DATABASE_URL")
        if dsn:
            return psycopg2.connect(dsn)
        # Fallback: parse individual env vars (convenience for dev)
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "sistema_escolar"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=os.getenv("DB_PORT", "5432")
        )

    def dict_cursor(conn):
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
except Exception:
    # psycopg2 may not be available in certain environments; keep SQLAlchemy as primary path
    def get_connection():
        raise RuntimeError("psycopg2 not available")

    def dict_cursor(conn):
        raise RuntimeError("psycopg2 not available")

