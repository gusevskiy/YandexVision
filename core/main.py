# Импортируйте библиотеку для кодирования в Base64
import base64
import os
import json
import requests
from settings import settings
from response_IAM_token import check_iam_token


def get_iam_token(iam_token_dir):
    if check_iam_token(iam_token_dir):
        file_iam_token = f"{iam_token_dir}\\{os.listdir(iam_token_dir)[0]}"
        with open(f"{file_iam_token}", "r", encoding="utf8") as file:
                iam_token = json.load(file)["iamToken"]
        return iam_token


def create_image_in_base64(input_image_file):
    with open(input_image_file, "rb") as f:
        file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
    data = {
        "mimeType": "JPEG",
        "languageCodes": ["ru"],
        "model": "passport",
        "content": encoded_content
    }
    return json.dumps(data, indent=4)


def main(image_path, iam_token_dir):
    iam_token = get_iam_token(iam_token_dir)
    json_data = create_image_in_base64(image_path)

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers = {
        "Authorization": f"Bearer {iam_token}",
        "Content-Type": "application/json",
        "x-folder-id": settings.privacy.x_folder_id,
        "x-data-logging-enabled": "true"
    }

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
         data_json = response.json()
         print(data_json)
         # Define the directory path
         directory = settings.privacy.result_json_folder

         # Create the directory if it doesn't exist
         if not os.path.exists(directory):
             os.makedirs(directory)

         # Define the file path
         file_path = directory + "file.json"

         with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)
    else:
        print("Ошибка", response.status_code)
        

if __name__ == '__main__':
    iam_token_dir = os.path.join(os.getcwd(), "iam_token")
    image_path = "C:\\RPA\\python\\YandexVision\\incoming\\photo_2024-04-16_10-50-14.jpg"
    main(image_path, iam_token_dir)
    # print(iam_token_dir)
