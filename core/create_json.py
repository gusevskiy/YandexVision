# Импортируйте библиотеку для кодирования в Base64
import base64
import json
import requests
from core.settings import settings


# Создайте функцию, которая кодирует файл и возвращает результат.
def encode_image_to_base64(input_image_file):
    with open(input_image_file, "rb") as f:
        file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
    return encoded_content

def create_json(imag_path):
    encode_content = encode_image_to_base64(imag_path)

    data = {
        "mimeType": "JPEG",
        "languageCodes": ["*"],
        "model": "passport",
        "content": encode_content
    }

    return json.dumps(data, indent=4)


def main(input_image_path):
    json_data = create_json(input_image_path)

    # with open("output.json", "w") as json_file:
    #     json_file.write(json_data)

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers = {
        "Authorization": "Bearer t1.9euelZrNy8fNjpONj8-Yi5CWx5yUlu3rnpWax8qMyZCeyJfJlc3Hms-cjM7l8_dWNTpP-e8GayFF_d3z9xZkN0_57wZrIUX9zef1656VmpGbmY_HmpmPm8qUnc2axo-J7_zF656VmpGbmY_HmpmPm8qUnc2axo-J.YUd87jDN2xSIaDNAO-BNVQjBcLsVdvDeDWvTGD0hAqVWkuI62T0iApTELDvTsPju9rFUXyGLtHn_lT2F4vLfBQ",
        "Content-Type": "application/json",
        "x-folder-id": settings.privacy.x_folder_id,
        "x-data-logging-enabled": "true"
    }

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Ошибка", response.status_code)
        

if __name__ == '__main__':
    input_image_file = "C:\\DEV_python\\YandexVision\\1.jpg"
    main(input_image_file)
