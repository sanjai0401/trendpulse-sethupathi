import requests

url = "https://api.sampleapis.com/futurama/episodes"
response = requests.get(url)

data = response.json()

import json
with open("data.json", "w") as f:
    json.dump(data, f)
