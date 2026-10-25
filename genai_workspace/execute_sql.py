import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "my_dbt_db"),
    "user": os.getenv("DB_USER", "dbt_user"),
    "password": os.getenv("DB_PASSWORD"),
}


def execute_sql(sql: str) -> list[dict]:
    """
    Execute the query in a read-only transaction.
    Args:
        sql: str -> llm generated query
    Returns:
        list[dict] -> list of resultant records"""

    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.set_session(readonly=True)

        with connection.cursor() as cursor:
            cursor.execute("SET LOCAL statement_timeout = '15000'")
            cursor.execute(sql)

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            if len(rows) > 100:
                raise ValueError(
                    "The query returned more than 100 rows. "
                    "Please narrow your question."
                )

            return [
                dict(zip(columns, row))
                for row in rows
            ]
