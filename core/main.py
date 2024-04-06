import os, glob
import json
from datetime import datetime, timedelta
import core.response_IAM_token as response_IAM_token
from core.settings import settings


path_file_iamtoken = (os.path.join(os.getcwd()))


def iam_token():
        
    for file in os.listdir(path_file_iamtoken):
        if file.startswith("iam_token"):
            # открывает json file iam_token запрошенный ранее.
            with open(path_file_iamtoken, "r") as file:
                iam_token = json.load(file)
            # дата и время окончания токена
            expiresAt = iam_token["expiresAt"]
            # переводим в формат "2024-04-07 03:55:09.855960"
            token_run_out_this_time = datetime.strptime(
                expiresAt[:26]+'Z', '%Y-%m-%dT%H:%M:%S.%fZ'
            )
            # если до окончания токена осталось меньше 2х часов.
            if token_run_out_this_time - datetime.today() < timedelta(hours=10):
                response_IAM_token.response_iam_token()
                break
        else:
            response_IAM_token.response_iam_token()
            break

if __name__ == '__main__':
    # iam_token()
    print(path_file_iamtoken)