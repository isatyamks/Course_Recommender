
  import requests
  
  api_key = "67c03d3d33734d79746429d7"
  url = "https://api.scrapingdog.com/linkedin"
  
  params = {
      "api_key": api_key,
      "type": "profile",
      "linkId": "https://www.linkedin.com/in/isatyamks/",
      "private": "false"
  }
  
  response = requests.get(url, params=params)
  
  if response.status_code == 200:
      data = response.json()
      print(data)
  else:
      print(f"Request failed with status code: {response.status_code}")