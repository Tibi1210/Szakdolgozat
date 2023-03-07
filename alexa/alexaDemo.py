import requests
import json
import datetime

findOneUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/findOne"
findUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/find"
deleteUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/deleteMany"




find = json.dumps({
    "collection": "plant1",
    "database": "plants",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 1,
        "Light": 1,
        "Temperature": 1,
        "Humidity": 1,
        "SoilMoisture": 1,
        "Timestamp": 1
    },
    "sort": { "Timestamp": -1 }
})

response = requests.request("POST", findUrl, headers=headers, data=find)
toDelete = json.loads(response.text)

for item in toDelete["documents"]:
    print(datetime.datetime.fromtimestamp(item["Timestamp"]))


#for item in toDelete["documents"]:
#    delete=json.dumps({
#        "collection": "plant1",
#        "database": "plants",
#        "dataSource": "Cluster0",
#        "filter": { "Timestamp": item["Timestamp"] }
#        })
#    response = requests.request("POST", deleteUrl, headers=headers, data=delete)



