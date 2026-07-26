import sqlalchemy

from src.config.config import ConfigWork

CONFIG = ConfigWork()


class LocalDb:
    """Small SQLite helper for storing and reading long term content"""

    def __init__(self):
        """Initialise the database engine and create the required tables.

        The configured SQLite path and initialization SQL file are read from
        the application configuration before the schema is built.
        """
        self.sqlite_path = CONFIG.LOCAL_DB_PATH
        self.init_path = CONFIG.LOCAL_DB_INIT_SQL_PATH
        self._engine = sqlalchemy.create_engine(f"sqlite:///{self.sqlite_path}")

        self.setup_db()

    def setup_db(self):
        """Create the local database tables from the SQL init script.

        The SQL content is loaded from the configured initialization file and
        executed against the SQLite engine.
        """
        with open(file=self.init_path) as file:
            raw_content = file.read()
            content = sqlalchemy.text(raw_content)

        with self._engine.connect() as conn:
            conn.execute(content)

    def _insert(self, query, params):
        """Insert rows into the database and return any returned records.

        :param query: SQL statement to execute.
        :param params: Bound parameters for the insert statement.
        :returns: A list of row mappings returned by the database.
        :rtype: list[dict]
        """
        with self._engine.connect() as conn:
            result = conn.execute(statement=sqlalchemy.text(query), parameters=params)

            rows = result.mappings().all()
            conn.commit()

        return rows

    def _update(self, query, params):
        """Update rows in the database and return any returned records.

        :param query: SQL statement to execute.
        :param params: Bound parameters for the insert statement.
        :returns: A list of row mappings returned by the database.
        :rtype: list[dict]
        """
        with self._engine.connect() as conn:
            result = conn.execute(statement=sqlalchemy.text(query), parameters=params)

            rows = result.mappings().all()
            conn.commit()

        return rows

    def _select(self, query: str, params: str = None):
        """Run a read query and return the result rows as dictionaries.

        :param query: SQL query to execute.
        :param params: Params that will be parsed into the query.
        :returns: A list of row dictionaries produced by the query.
        :rtype: list[dict]
        """
        with self._engine.connect() as conn:
            result = conn.execute(statement=sqlalchemy.text(query), parameters=params)

        rows = [dict(row) for row in result.mappings().all()]

        return rows

    def _delete(self, query: str, params: dict = None):
        """Delete rows from the database and return the affected count.

        :param query: SQL delete statement to execute.
        :param params: Bound parameters for the delete statement.
        :returns: The number of rows deleted.
        :rtype: int
        """
        with self._engine.connect() as conn:
            result = conn.execute(statement=sqlalchemy.text(query), parameters=params)

            conn.commit()

        return result.rowcount
