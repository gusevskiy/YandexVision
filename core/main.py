import os, glob
import json
from datetime import datetime, timedelta
import response_IAM_token as response_IAM_token
from settings import settings


def iam_token(path_file_iamtoken):
    # По умолчанию считаем что обновление требуется
    token_update = False
    for file in os.listdir(path_file_iamtoken):
        if file.startswith("iam_token"):
            # открывает json file iam_token запрошенный ранее.
            with open(f"{path_file_iamtoken}{file}", "r") as file:
                iam_token = json.load(file)
            # дата и время окончания токена
            expiresAt = iam_token["expiresAt"]
            # переводим в формат "2024-04-07 03:55:09.855960"
            token_run_out_this_time = datetime.strptime(
                expiresAt[:26]+'Z', '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            # если до окончания токена осталось меньше 2х часов.
            if token_run_out_this_time - datetime.today() < timedelta(hours=2):
                token_update = response_IAM_token.response_iam_token()
                break
    else:
        token_update = response_IAM_token.response_iam_token()
    return token_update


def main():
    
    iam_token()
    ...




if __name__ == '__main__':
    path_file_iamtoken = (os.path.join(os.getcwd(), "iam_token\\"))
    # print(path_file_iamtoken)
    # print(os.path.isfile(path_file_iamtoken))
    print(iam_token(path_file_iamtoken))
    # print(path_file_iamtoken)