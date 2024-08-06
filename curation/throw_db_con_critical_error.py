import logging

import sqlalchemy


def throw_db_con_critical_error(engine: sqlalchemy.Engine):
    logging.critical(
        f"Connection to server '{engine.url.database}' failed. Ensure the server is running locally and accepting "
        f"connections on the selected socket.")

    exit(1)
