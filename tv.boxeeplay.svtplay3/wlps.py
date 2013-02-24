#encoding:utf-8
#author:Andreas Pehrson
#project:boxeeplay.tv

import simplejson as json
from utilities import get_data, handleException, Url
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
        self.endpoints = self.get_json(self.url("/v1/"))
        self.categories = self.get_iterable(self.get_list_endpoint("category"))

    def url(self, location):
        if location is None:
            return None
        url = Url(BASE_URL + location)
        url.add_param("format", "json")
        return url

    def get_list_endpoint(self, key):
        return self.url(self.endpoints[key]["list_endpoint"])

    def get_json(self, url):
        return convert(json.loads(get_data(url)))

    def get_iterable(self, endpoint):
        return WlpsIterable(self, endpoint)

    def get_shows(self, category):
        endpoint = self.get_list_endpoint("show")
        endpoint.add_param("category", category["id"])
        return self.get_iterable(endpoint)

    def get_episodes(self, show):
        endpoint = self.get_list_endpoint("episode")
        endpoint.add_param("show", show["id"])
        return self.get_iterable(endpoint)

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
        self.next_endpoint = self.client.url(meta["next"])

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

