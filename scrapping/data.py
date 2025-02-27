
import requests
linkedin = 'isatyamks'
api_key = "67c0b380bd375d7bb8171f90"
url = "https://api.scrapingdog.com/linkedin"

params = {
    "api_key": api_key,
    "type": "profile",
    "linkId": f'{linkedin}',
    "private": "false"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")