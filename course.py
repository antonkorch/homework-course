import requests
import json
from pprint import pprint

class VKAPIClient:
    API_BASE_URL = "https://api.vk.com/method/"

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = int(user_id)

    def get_common_params(self):
        return {
            "access_token": self.token,
            "v": "5.131"
        }
    
    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({"owner_id" : self.user_id, "album_id" : "profile"})
        response = requests.get(self.API_BASE_URL + "photos.get", params=params)
        return response.json()
    
    def download_photo(self, url):
        response = requests.get(url)
        return response.content
    
class YandexAPIClient:
    API_BASE_URL = "https://cloud-api.yandex.net/"
    
    def __init__(self, token):
        self.token = token
    
    def create_folder(self,folder):
        url = self.API_BASE_URL + "v1/disk/resources"
        params = {"path": folder}
        headers = {"Authorization": f"OAuth {self.token}"}
        response = requests.put(url, params=params, headers=headers)
        print (f'Created folder /{folder} with response code {response.status_code}')

with open("tokens.json", "r") as f:
    tokens = json.load(f)

backup_id = "2493073" 
backup_folder = "backup" 
vk_client = VKAPIClient(tokens["vk"], backup_id)
yadi_client = YandexAPIClient(tokens["yadi"])

photos_info = vk_client.get_profile_photos()

yadi_client.create_folder(backup_folder)

