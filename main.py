import psycopg2
import argparse

GLUCOSE_REPOSITORY_DIRECTORY = ('../curated-data-for-describing-blood-glucose-management-in-the-intensive-care-unit-1'
                                '.0.1')


def connect():
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


if __name__ == '__main__':
    # Define the command line arguments.
    parser = argparse.ArgumentParser(
        prog="Glucose homeostasis algorithm data curation",
        description="Leverages the MIMIC-III dataset to generate data a glucose homeostasis algorithm.",
        epilog="Link to GitHub repository: https://github.com/tahmidazam/glucose-homeostasis."
    )

    parser.add_argument('-d', '--dbname', type=str, default="mimic", help='Name of the Postgres database.',
                        required=False)
    parser.add_argument('-u', '--user', type=str, default="mimicuser", help='Username for the Postgres database.',
                        required=False)
    parser.add_argument('-p', '--password', type=str, default="", help='Username for the Postgres database.',
                        required=False)
    parser.add_argument('--host', type=str, default="localhost", help='The host of the Postgres database.',
                        required=False)
    parser.add_argument('--port', type=str, default="5432", help='The port used by the Postgres database.',
                        required=False)

    args: argparse.Namespace = parser.parse_args()

    # Attempt connection to the MIMIC-III Postgres database.
    mimic = connect()
