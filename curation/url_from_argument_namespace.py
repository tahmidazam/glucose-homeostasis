from config import Config


def config_to_db_url(config: Config) -> str:
    return f"postgresql+psycopg2://{config.mimic_database_username}:{config.mimic_database_password}@" \
           f"{config.mimic_database_host}:{config.mimic_database_port}/{config.mimic_database_name}"
