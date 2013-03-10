import urllib2
import simplejson as json
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
        params = ["=".join(tup) for tup in self.params.items()]
        params_str = ""
        if params: params_str = "?" + "&".join(params)
        return self.url + params_str

    def __repr__(self):
        return self.get_url()

def get_data(url):
    BPTraceEnter(str(url))
    BPLog("Getting data from: " + str(url))
    request = urllib2.Request(str(url))
    response = urllib2.urlopen(request)
    data = response.read()
    response.close();
    BPTraceExit("Returning %s" % data)
    return data

def handleException(func, e):
    BPLog("In " + str(func) + ", " + str(e), Level.ERROR)

def convert(input):
    if isinstance(input, dict):
        return dict((convert(key), convert(value)) for (key, value) in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def load_json(url):
    return convert(json.loads(get_data(str(url))))

