import requests
import os, glob 
import json
from datetime import datetime
from log_config import setup_logger
from loguru import logger
from settings import settings


# настройки loggers
setup_logger()


def delete_file_iam_token():
    """
    Удаляет файл iam_token*.json
    """
    try:
        file_iam_token = glob.glob(os.getcwd()+'/iam_token*')[0]
        if file_iam_token:
            os.remove(file_iam_token)
            logger.info(f'Deleted old file: file_iam_token {file_iam_token}')
        else:
            logger.warning('No file iam_token')
    except Exception as e:
        logger.error(f'Error deleting file_iam_token: {e}')

# 
def response_iam_token():
    """
    Запрашивает iam_token для Authorization в HTTP запросе.
    """
    try:
        # сначало удаляем файл если он есть
        delete_file_iam_token()

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
        with open(file_name, "w") as json_file:
            json.dump(iam_token, json_file, indent=4)
            logger.info(f"Created new file: {file_name}")
        return True
            
    except requests.exceptions.RequestException as e:
        logger.error(f'Error fetching iam_token {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    return False


if __name__ == '__main__':
    response_iam_token()
    # delete_file_iam_token()