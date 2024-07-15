import argparse
import psycopg2


def connect_to_local_mimic(argument_parser: argparse.ArgumentParser):
    """
    Connects to the local MIMIC-III Postgres database.
    :param argument_parser: The argument parser from which to source server hosting information and credentials.
    :return: The connection to the MIMIC-III Postgres database.
    """
    args: argparse.Namespace = argument_parser.parse_args()

    try:
        connection = psycopg2.connect(
            f"dbname={args.dbname} user={args.user} password={args.password} host={args.host} port={args.port}")

        print(f"Connected to {connection.info.dbname} as {connection.info.user}.")

        return connection
    except psycopg2.Error:
        print(
            "Connection to server failed. Ensure the server is running locally and accepting connections on the "
            "selected socket.")
        exit(1)
