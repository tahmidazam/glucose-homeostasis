from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Config:
    mimic_database_name: str
    mimic_database_username: str
    mimic_database_password: str
    mimic_database_host: str
    mimic_database_port: int

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        mimic_database_name = from_str(obj.get("MIMIC_DATABASE_NAME"))
        mimic_database_username = from_str(obj.get("MIMIC_DATABASE_USERNAME"))
        mimic_database_password = from_str(obj.get("MIMIC_DATABASE_PASSWORD"))
        mimic_database_host = from_str(obj.get("MIMIC_DATABASE_HOST"))
        mimic_database_port = int(from_str(obj.get("MIMIC_DATABASE_PORT")))
        return Config(mimic_database_name, mimic_database_username, mimic_database_password, mimic_database_host,
                      mimic_database_port)

    def to_dict(self) -> dict:
        result: dict = {
            "MIMIC_DATABASE_NAME": from_str(self.mimic_database_name),
            "MIMIC_DATABASE_USERNAME": from_str(self.mimic_database_username),
            "MIMIC_DATABASE_PASSWORD": from_str(self.mimic_database_password),
            "MIMIC_DATABASE_HOST": from_str(self.mimic_database_host),
            "MIMIC_DATABASE_PORT": from_str(str(self.mimic_database_port))
        }
        return result


def config_from_dict(s: Any) -> Config:
    return Config.from_dict(s)


def config_to_dict(x: Config) -> Any:
    return to_class(Config, x)
