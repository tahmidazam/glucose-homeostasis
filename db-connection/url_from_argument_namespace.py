import argparse


def url_from_argument_namespace(argument_namespace: argparse.Namespace) -> str:
    return f"postgresql+psycopg2://{argument_namespace.user}:{argument_namespace.password}@{argument_namespace.host}:{argument_namespace.port}/{argument_namespace.dbname}"
