import urllib2
from logger import BPLog, BPTraceEnter, BPTraceExit, Level

class Url:
    def __init__(self, url):
        if url is None:
            return
        urlSplit = url.split("?")
        self.url = urlSplit[0]
        self.params = {}
        if len(urlSplit) > 1:
            self.params = dict(key_val.split("=", 1) for key_val in urlSplit[1].split("&"))

    def add_param(self, key, value):
        self.params[key] = value

    def get_url(self):
        params = ("=".join(tup) for tup in self.params.items())
        url = self.url + "?" + "&".join(params)
        return url

    def __repr__(self):
        return self.get_url()

def get_data(url):
    BPTraceEnter(str(url))
    BPLog("Getting data from: " + str(url))
    request = urllib2.Request(str(url))
    request.add_header = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
    response = urllib2.urlopen(request)
    data = response.read()
    response.close();
    BPTraceExit("Returning %s" % data)
    return data

def handleException(func, e):
    BPLog("In " + str(func) + ", " + str(e), Level.ERROR)
