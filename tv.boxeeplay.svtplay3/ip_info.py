import utilities

REQUEST_URL = "http://api.ipinfodb.com/v3/ip-country/?key=a4610f4c5d9c206aa4e94637d50f5db4967d0ba5c482cdb8c75dfbe3583b78c0&format=json"
response = None

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
