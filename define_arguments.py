import argparse


def define_arguments() -> argparse.ArgumentParser:
    """
    Define the command-line arguments for the main script.
    :return: The parser for the command-line arguments.
    """
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="Glucose homeostasis algorithm data curation",
        description="Leverages the MIMIC-III dataset to generate data a glucose homeostasis algorithm.",
        epilog="Link to GitHub repository: https://github.com/tahmidazam/glucose-homeostasis."
    )

    argument_parser.add_argument('-d', '--dbname', type=str, default="mimic", help='Name of the Postgres database.',
                                 required=False)
    argument_parser.add_argument('-u', '--user', type=str, default="mimicuser",
                                 help='Username for the Postgres database.',
                                 required=False)
    argument_parser.add_argument('-p', '--password', type=str, default="", help='Username for the Postgres database.',
                                 required=False)
    argument_parser.add_argument('--host', type=str, default="localhost", help='The host of the Postgres database.',
                                 required=False)
    argument_parser.add_argument('--port', type=str, default="5432", help='The port used by the Postgres database.',
                                 required=False)

    return argument_parser
