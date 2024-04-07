# Импортируйте библиотеку для кодирования в Base64
import base64
import json
import requests
from settings import settings


# Создайте функцию, которая кодирует файл и возвращает результат.
def create_data_request(input_image_file):
    with open(input_image_file, "rb") as f:
        file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
    # return encoded_content
    data = {
        "mimeType": "JPEG",
        "languageCodes": ["*"],
        "model": "passport",
        "content": encoded_content
    }
    return json.dumps(data, indent=4)

# def create_json(imag_path):
#     encode_content = encode_image_to_base64(imag_path)

#     data = {
#         "mimeType": "JPEG",
#         "languageCodes": ["*"],
#         "model": "passport",
#         "content": encode_content
#     }

#     return json.dumps(data, indent=4)


def main(image_path):
    json_data = create_data_request(image_path)

    # with open("output.json", "w") as json_file:
    #     json_file.write(json_data)

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers = {
        "Authorization": "Bearer t1.9euelZrGkZidloqNjZ6XicjKxp3OkO3rnpWax8qMyZCeyJfJlc3Hms-cjM7l8_dMOTVP-e82LUJG_N3z9wxoMk_57zYtQkb8zef1656VmonNlpKXm8yYyZael8zGlsmW7_zF656VmonNlpKXm8yYyZael8zGlsmW.ZoVtNTU0aY2vqggAOyEmXx6C4tU2q-aHSzqPsXF3M4QNVFplyQ9cOKWBamK9vxiHO8By8Sk6n6MEgLWxIXe1AA",
        "Content-Type": "application/json",
        "x-folder-id": settings.privacy.x_folder_id,
        "x-data-logging-enabled": "true"
    }

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
         data_json = response.json()
         file_name = "C:\\DEV_python\\YandexVision\\result_files_json\\file.json"
         with open(file_name, "w") as json_file:
            json.dump(data_json, json_file, indent=4)
        # print(response.json())
    else:
        print("Ошибка", response.status_code)
        

if __name__ == '__main__':
    input_image_file = "C:\\DEV_python\\YandexVision\\input_image\\1.jpg"
    main(input_image_file)
