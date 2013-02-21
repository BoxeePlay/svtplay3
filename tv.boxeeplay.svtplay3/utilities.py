import urllib2
from logger import BPLog, BPTraceEnter, BPTraceExit, Level

def getData(url):
    BPTraceEnter(url)
    request = urllib2.Request(url)
    request.add_header = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
    response = urllib2.urlopen(request)
    data = response.read()
    response.close();
    BPTraceExit("Returning %s" % data)
    #BPLog("read: " + data)
    #BPLog("encode utf8: " + data.encode("utf-8"))
    #BPLog("str convert: " + str(data))
    #BPLog("encode 8859: " + data.encode("iso-8859-1"))
    return data

def handleException(func, e):
    BPLog("In " + str(func) + ", " + str(e), Level.ERROR)
