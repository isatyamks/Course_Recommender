
# linkedin = 'isatyamks'
# def scrap(linkedin):
#     print(linkedin)
#     api_key = "67c0bc870d3f4be461184ef7"
#     url = "https://api.scrapingdog.com/linkedin"
#     params = {
#         "api_key": api_key,
#         "type": "profile",
#         "linkId": linkedin,
#         "private": "false"
#     }
    
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()[0] if isinstance(response.json(), list) else response.json()
#     else:
#         print(f"Request failed with status code: {response.status_code}")
#         data = {}
#     return data


# json_input = scrap(linkedin)
# print(json_input)
