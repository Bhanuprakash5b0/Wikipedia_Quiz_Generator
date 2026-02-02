import psycopg2
from config import DATABASE_URL


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Create a .env file from .env.example and set DATABASE_URL to a valid PostgreSQL URI."
        )

    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.OperationalError as e:
        # Provide a clearer error message for common connection issues
        raise RuntimeError(
            f"Unable to connect to the database. Original error: {e}.\n"
            "Check that PostgreSQL is running and that DATABASE_URL in backend/.env is correct."
        ) from e

