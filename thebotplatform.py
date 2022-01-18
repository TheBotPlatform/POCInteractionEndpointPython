import requests
import re
import json

from decouple import config

#Creating and getting my bearer token

def BearerTokenGrab():

    clientID = config("TBP_CLIENT_ID")
    clientSecret = config("TBP_CLIENT_SECRET")
    url = "https://api.thebotplatform.com/oauth2/token"
    payload = "client_id="+clientID+"&client_secret="+clientSecret+"&grant_type=client_credentials"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    jsonResponse = response.json()
    return jsonResponse['access_token']

#Creates a User ID for the current user
def CreateUserID(Token):
    url = "https://api.thebotplatform.com/v1.0/interaction/user"
    payload = []
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer "+Token
        }
    response = requests.post(url, data=payload, headers=headers)
    jsonResponse = response.json()   
    return jsonResponse['data']['attributes']['user']['id']

def getBotResponse(UserID, input):
    url = "https://api.thebotplatform.com/v1.0/interaction"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+BearerTokenGrab() # TODO: this shouldn't be done on every request, it lasts 60 minutes
        }
    payloaddict = { "data": { "type": "interaction", "attributes": { "user": { "id": UserID }, "input": input } } }

    response = requests.post(url, headers=headers, json=payloaddict)
    jsonResponse = response.json()
    formatJsonresp = json.dumps(jsonResponse, indent=4, sort_keys=True)
    return formatJsonresp

testToken = BearerTokenGrab()
print("Token is: "+testToken)
userId = CreateUserID(testToken);

print("Userid is: "+userId)