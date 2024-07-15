import argparse
import psycopg2


def connect_to_local_mimic(argument_namespace: argparse.Namespace):
    """
    Connects to the local MIMIC-III Postgres database.
    :param argument_namespace: The argument parser from which to source server hosting information and credentials.
    :return: The connection to the MIMIC-III Postgres database.
    """
    try:
        connection = psycopg2.connect(
            f"dbname={argument_namespace.dbname} user={argument_namespace.user} password={argument_namespace.password} host={argument_namespace.host} port={argument_namespace.port}")

        print(f"Connected to {connection.info.dbname} as {connection.info.user}.")

        return connection
    except psycopg2.Error:
        print(
            "Connection to server failed. Ensure the server is running locally and accepting connections on the "
            "selected socket.")
        exit(1)
