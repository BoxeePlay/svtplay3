import base64
import simplejson
import urllib2
import mc

def track(event, properties=None):
    """
    A simple function for asynchronously logging to the mixpanel.com API.
    This function requires `curl` and Python version 2.4 or higher.

    @param event: The overall event/category you would like to log this data under
    @param properties: A dictionary of key-value pairs that describe the event
                       See http://mixpanel.com/api/ for further detail.
    @return Instance of L{subprocess.Popen}
    """
    if properties == None:
        properties = {}
    token = "45e300366f57752c6a7e30bcb0e24f0c"
    if "token" not in properties:
        properties["token"] = token

    properties["distinct_id"] = mc.GetUniqueId()

    params = {"event": event, "properties": properties}
    data = base64.b64encode(simplejson.dumps(params))
    request = "http://api.mixpanel.com/track/?data=" + data
    url_request = urllib2.Request(request)
    response = urllib2.urlopen(url_request)
    data = response.read()
    response.close()
    return data
