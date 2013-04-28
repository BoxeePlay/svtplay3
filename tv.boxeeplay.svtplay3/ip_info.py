import utilities, threading

REQUEST_URL = "http://api.ipinfodb.com/v3/ip-country/?key=a4610f4c5d9c206aa4e94637d50f5db4967d0ba5c482cdb8c75dfbe3583b78c0&format=json"
response = None

class IpGetter(threading.Thread):

    def __init__(self):
        self.response = None
        self.error = None
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        try:
            self.response = get_response()
        except Exception, e:
            self.error = e

    def get_response(self):
        if self.isAlive():
            raise RuntimeError("Not finished yet")
        elif self.error != None:
            raise self.error
        else:
            return self.response

    def get_country_code(self):
        return self.get_response()["countryCode"]

    def get_country_name(self):
        return self.get_response()["countryName"]

def get_response():
    global response

    if response == None:
        response = utilities.load_json(REQUEST_URL)
    if response["statusCode"] != "OK":
        raise Exception("Code: " + response["statusCode"] +
                        "Message: " + response["statusMessage"])
    return response

def get_country_code():
    return get_response()["countryCode"]

def get_country_name():
    return get_response()["countryName"]
