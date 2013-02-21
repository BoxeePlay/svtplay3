#encoding:utf-8
#author:Andreas Pehrson
#project:boxeeplay.tv

import simplejson as json
from utilities import getData, handleException
from logger import BPLog, Level

BASE_URL = "http://api.welovepublicservice.se"

__all__ = [ "WlpsClient" ]

def convert(input):
    if isinstance(input, dict):
        return dict((convert(key), convert(value)) for (key, value) in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class WlpsClient:
    def __init__(self):
        self.endpoints = self.get_json("/v1/")
        self.categories = self.get_iterable(self.get_list_endpoint("category"))

    def get_list_endpoint(self, key):
        return self.endpoints[key]["list_endpoint"] + "?format=json"

    def get_json(self, location):
        url = BASE_URL + location
        return convert(json.loads(getData(url)))

    def get_iterable(self, endpoint):
        return WlpsIterable(self, endpoint)

# NOT thread safe
class WlpsIterable:
    def __init__(self, client, endpoint):
        self.client = client
        self.next_endpoint = endpoint
        self.objects = []
        self.current_limit = 0
        self.size = 1

    def __iter__(self):
        return WlpsIterator(self, self.client)

    def set_meta(self, meta):
        self.current_limit = meta["offset"] + meta["limit"]
        self.size = meta["total_count"]
        self.next_endpoint = meta["next"]

# NOT thread safe
class WlpsIterator:
    def __init__(self, iterable, client):
        self.iterable = iterable
        self.client = client
        self.current = -1

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        if self.current >= self.iterable.size:
            raise StopIteration
        if self.current >= self.iterable.current_limit:
            json = self.client.get_json(self.iterable.next_endpoint)
            self.iterable.set_meta(json["meta"])
            self.iterable.objects.extend(json["objects"])
        if self.current >= len(self.iterable.objects):
            BPLog("API reported length of " + str(self.iterable.size) +
                  " but I reached the end at " + str(self.current) +
                  " items. Stopping.", Level.ERROR)
            raise StopIteration # if we got more objects but the list was not filled as expected
        #BPLog("objects length: " + str(len(self.iterable.objects)) + ", current: " + str(self.current - 1) + ", size: " + str(self.iterable.size) + ", current_limit: " + str(self.iterable.current_limit))
        return self.iterable.objects[self.current]

