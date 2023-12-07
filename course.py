import requests
import json

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
        params.update({
            "owner_id" : self.user_id, 
            "album_id" : "profile",
            "extended" : 1,
        })
        response = requests.get(self.API_BASE_URL + "photos.get", params=params)
        return response.json()
    
    def download_photo(self, url):
        response = requests.get(url)
        return response.content
    
class YandexAPIClient:
    API_BASE_URL = "https://cloud-api.yandex.net/"
    
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"OAuth {self.token}"}
    
    def create_folder(self,folder):
        url = self.API_BASE_URL + "v1/disk/resources"
        params = {"path": folder}
        response = requests.put(url, params=params, headers=self.headers)

        print (f'Created folder /{folder}')
    
    def upload_file(self, file, folder, name):
        url = self.API_BASE_URL + "v1/disk/resources/upload"
        params = {"path": f"{folder}/{name}.jpg", "overwrite" : "true"}
        response = requests.get(url, params=params, headers=self.headers)
        upload_url = response.json()["href"]
        response = requests.put(upload_url, files={"file": file})

        print (f'Uploaded file {name}.jpg')

def good_name(name):
    for entry in log:
        if entry["file_name"] == name:
            return False
    
    return True

with open("tokens.json", "r") as f:
    tokens = json.load(f)

log = []
backup_id = int(input("Enter VK user ID: ")) 
backup_folder = "backup" 
vk_client = VKAPIClient(tokens["vk"], backup_id)
yadi_client = YandexAPIClient(tokens["yadi"])

photos_info = vk_client.get_profile_photos()
photos_amount = photos_info["response"]["count"]
wished_amount = input(f"Found {photos_amount} photos, how many should I backup? ")

if wished_amount == "":
    wished_amount = 5
elif wished_amount.isdigit() and int(wished_amount) <= photos_amount:
    photos_amount = int(wished_amount)
else:
    print ("Wrong input, backing up all photos")

yadi_client.create_folder(backup_folder)

for i in range (photos_amount):
    photo_url = photos_info["response"]["items"][i]["sizes"][-1]["url"]
    name = photos_info["response"]["items"][i]["likes"]["count"]

    if not good_name(f"{name}.jpg"):
        name = f'{name} - {photos_info["response"]["items"][i]["date"]}'

    photo = vk_client.download_photo(photo_url)

    yadi_client.upload_file(photo, backup_folder, name)

    log.append({
        "file_name": f"{name}.jpg", 
        "size": photos_info["response"]["items"][i]["sizes"][-1]["type"]
    })

print ("Done!")

with open("log.json", "w") as f:
    json.dump(log, f, indent=4)