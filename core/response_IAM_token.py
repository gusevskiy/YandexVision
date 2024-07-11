import requests
import os, glob 
import json
from datetime import datetime, timedelta
from log_config import setup_logger
from loguru import logger
from settings import settings


# настройки loggers
setup_logger()


def delete_file_iam_token(iam_token_dir):
    """
    Удаляет файл iam_token*.json
    """
    try:
        file_iam_token = f"{iam_token_dir}\\{os.listdir(iam_token_dir)[0]}"
        if file_iam_token:
            os.remove(file_iam_token)
            logger.info(f'Deleted old file: file_iam_token {file_iam_token}')
        else:
            logger.warning('No file iam_token')
    except Exception as e:
        logger.error(f'Error deleting file_iam_token: {e}')

# 
def response_iam_token(iam_token_dir) -> bool:
    """
    Запрашивает iam_token для Authorization в HTTP запросе.
    Сохраняет ответ в файл iam_token_date.json.
    """
    try:
        # сначало удаляем файл если он есть
        delete_file_iam_token(iam_token_dir)
        # запрашиваем IAM_token
        iam_token_response = requests.post(
            'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            json={"yandexPassportOauthToken": settings.privacy.OAuth_token}
            )
        # Генерирует исключение при ошибке HTTP
        iam_token_response.raise_for_status()
        # формируем json формат
        iam_token = iam_token_response.json()
        # сохраняем файл iam_token_текущая_дата.json
        file_name = f"iam_token {datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"
        with open(f"{iam_token_dir}\\{file_name}", "w") as json_file:
            json.dump(iam_token, json_file, indent=4)
            logger.info(f"Created new file: {file_name}")
        return True
            
    except requests.exceptions.RequestException as e:
        logger.error(f'Error fetching iam_token {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    return False


def check_iam_token(iam_token_dir) -> bool:
    """
    Ф-я Проверяет существующий iam_token.json метод expiresAt
    на предмент окнчания действия токена.
    Если до окончания жизни токена менее 2х часов,
    звпрашивается новый.
    Если все запросы прошли ф-я возвращает True
    """
    # По умолчанию считаем что обновление требуется
    token_update = False
    for file in os.listdir(iam_token_dir):
        if file.startswith("iam_token"):
            # открывает json file iam_token котрый в папке iam_token.
            with open(f"{iam_token_dir}\\{file}", "r") as file:
                iam_token = json.load(file)
            # дата и время окончания токена
            expiresAt = iam_token["expiresAt"]
            # переводим в формат "2024-04-07 03:55:09.855960"
            token_run_out_this_time = datetime.strptime(
                expiresAt[:26]+'Z', '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            # если до окончания токена осталось меньше 2х часов, запрашиваем новый.
            if token_run_out_this_time - datetime.today() < timedelta(hours=2):
                token_update = response_iam_token(iam_token_dir)
                logger.info(f"Update token {file}")
                break
            else:
            # если время еще позволяет используем существующий токен
                token_update = True
                logger.info("token is valid")
                break
    # Если файла с токеном ввобще нет, запрашиваем новый токен.
    else:
        token_update = response_iam_token(iam_token_dir)
        logger.warning("File iam_token.json не был обнаружен!!! Создали новый.")
    return token_update


if __name__ == '__main__':
    iam_token_dir = os.path.join(os.getcwd(), "iam_token")
    # print(iam_token_dir)
    # print(f"{iam_token_dir}\{os.listdir(iam_token_dir)[0]}")
    # print(check_iam_token(iam_token_dir))
    # delete_file_iam_token()
    # print(os.listdir(os.path.join(os.getcwd(), "iam_token\\"))[0]) 