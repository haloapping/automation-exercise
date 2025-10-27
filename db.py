from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
import configvar


DB_DSN = f"host={configvar.HOST} dbname={configvar.DBNAME} user={configvar.USER} password={configvar.PASSWORD}"

pool = ConnectionPool(
    open=True,
    conninfo=DB_DSN,
    min_size=1,
    max_size=10,
    kwargs={
        "row_factory": dict_row,
    },
)
