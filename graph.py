# Pipeline
from requests_futures.sessions import FuturesSession
from collections import Counter
import requests
import json
import operator

MY_CLIENT_ID = "b45b1aa10f1ac2941910a7f0d10f8e28"
session = FuturesSession(max_workers=20) #empirically determined best on my machine

def submitRequest(songId, page):
    requestUrl = "http://api.soundcloud.com/tracks/" + songId + "/playlists?client_id=" + MY_CLIENT_ID + "&limit=5&linked_partitioning=1&offset=" + str(page * 5)
    print("Page" + str(page))
    return session.get(requestUrl)

def batchRequests(id, batchSize, batchNum):
    i = batchNum * batchSize
    limit = i + batchSize
    responseArray = []
    #submit async
    while(i < limit):
        responseArray.append(submitRequest(id, i))
        i += 1
    return responseArray

def batchProcess(responseArray, processedArray):
    for i, response in enumerate(responseArray):
        print("processing response: " + str(i))

        #soundcloud thinks im ddosing :)
        try:
            result = response.result()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            continue

        #sometimes connections drop
        if result.status_code != 200:
            print("failed")
            continue

        rJson = result.json()
        if 'collection' in rJson:
            processResponse(rJson, processedArray)
        if not "next_href" in rJson:
            return False

    return True

#adds processed response to processedArray
def processResponse(rJson, processedArray):
    collections = rJson["collection"]
    for collection in collections:
        tracks = collection["tracks"]
        for track in tracks:
            processedArray.append(track["id"])

def crawlAllPlaylists(id):
    next = True
    processedArray = []
    batchNum = 0
    while(next):
        responses = batchRequests(id, 50, batchNum)
        next = batchProcess(responses, processedArray)
        batchNum += 1
    return processedArray

def getRankings(id):
    results = crawlAllPlaylists(id)
    counted = Counter(results)
    sorted_counts = sorted(counted.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_counts
