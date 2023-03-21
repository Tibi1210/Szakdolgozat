import requests
import json
import datetime

findOneUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/findOne"
findUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/find"
deleteUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/deleteMany"
insertUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/insertOne"
updateUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/updateOne"

api=""
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': api, 
}

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
                "Timestamp": 1,
            },
            "sort": { "Timestamp": -1 },
            "limit": 1
        })

response = requests.request("POST", findUrl, headers=headers, data=find)
r = json.loads(response.text)

print(r)
