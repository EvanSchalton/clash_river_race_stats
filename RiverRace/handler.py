import boto3
import json

import requests
import datetime
import os


def getAPIKey():
    # I use a function because in my deployment I have multiple api keys and randomly choose one
    # this helps w/ rate limiting
    return os.environ['CR_API_KEY']

def getClanTags()
    # splits & strips the csv of clantags and reurns a list
    return [i.strip() for i in os.environ['CLAN_TAGS'].split(",")]

def tag23(tag):
    if "#" in tag:
        return tag.replace("#", "%23")
    if tag[:3] == "%23":
        return tag
    else:
        return "%23" + tag

def riverRaceAPI(clanID):
    # Use the royalapi proxy service to hit the clash server
    # Set this: 128.128.128.128 as your IP to use the proxy service
    clanID = tag23(clanID)
    req = requests.get(
        'https://proxy.royaleapi.dev/v1/clans/{}/currentriverrace'.format(clanID),
        headers={
            'Accept': 'application/json',
            'authorization': f"Bearer {getAPIKey()}"
        }
    ).json()
    try:
        return req
    except Exception as e:
        # Not really handling the error here -- probably should retry w/ backoff, but....
        print("clanAPI error:", e)
        print("request:", req)


def riverrace(event, context):
    # Loops through the clan tags and saves them to your dynamodb table
    # Also need error handling here.....
    print(event, context)
    client = boto3.resource('dynamodb')
    table = client.Table("RiverRace")

    pullTime = datetime.datetime.now().isoformat()

    for clanTag in getClanTags():
        results = riverRaceAPI(clanTag)

        table.put_item(Item= {
            'clanTag': clanTag,
            'pullTime': pullTime,
            'data': results
        })

    response = {
        "statusCode": 200
    }

    return response
