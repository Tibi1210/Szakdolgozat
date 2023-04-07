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

insertJson = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "document": {
                "Timestamp": 1, 
                "Light": 1,
                "Temperature": 1,
                "Humidity": 1,
                "SoilMoisture": 1,
                "delete": 1
            }
        })



try:
  dataResponse = json.loads(requests.request("POST", insertUrl, headers=headers, data=insertJson).text)
except Exception as e:
  print(str(e))
