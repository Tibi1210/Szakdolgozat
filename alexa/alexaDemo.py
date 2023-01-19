import requests
import json
import datetime

findOneUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/findOne"
findUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/find"



find = json.dumps({
    "collection": "plant1",
    "database": "plants",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 0,
        "Light": 1,
        "Temperature": 1,
        "Humidity": 1,
        "SoilMoisture": 1,
        "Timestamp": 1
    },
    "sort": { "Timestamp": -1 },
    "limit": 1
})


headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': "",
}

response = requests.request("POST", findUrl, headers=headers, data=find)
y = json.loads(response.text)

print(y["documents"][0]["Light"])
print(datetime.datetime.fromtimestamp(y["documents"][0]["Timestamp"]))