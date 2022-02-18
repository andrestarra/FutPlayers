import requests
import json

# CONNECTION VARIABLES
API = 'https://www.easports.com/fifa/ultimate-team/api/fut/item'
API_SAVE = 'http://localhost:8000/api/v1'

# GENERALS VARIALES
HEADERS = {'content-type': 'application/json'}

def send(url, data):
    return requests.post(url, data=json.dumps(data), headers=HEADERS)

def get(url, params):
    return requests.get(url, params=params)

def savePlayers(data):
    return send(API_SAVE + '/players/import', data)

def getPlayers(page=None):
    params = {}
    if page:
        params['page'] = page
    return get(API, params)