from environs import Env
from dataclasses import dataclass


@dataclass
class Privacy:
    OAuth_token: str
    x_folder_id: str
    incoming_files: str
    result_json_folder: str


@dataclass
class Settings:
    privacy: Privacy


# ф-я формирования объекта настроеК
def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        privacy=Privacy(
            OAuth_token=env.str("OAuth"),
            x_folder_id=env.str("X_folder_id"),
            incoming_files=env.str("incoming_files"),
            result_json_folder=env.str("result_json_folder")
        )
    )


# Считавем настройки из файла input
settings = get_settings('./.env')
print(settings)  # test print