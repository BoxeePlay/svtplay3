#encoding:utf-8
#author:Andreas Pehrson
#project:boxeeplay.tv

from urllib import quote_plus, urlencode
from utilities import Url
from logger import BPLog

class NoSuitableStreamError(Exception):
    pass

class NoStreamsError(Exception):
    pass

def get_streams(path):
    url = Url("http://pirateplay.se/api/get_streams.js")
    url.add_param('url', path)
    print url.get_url()
    return url.load_json()

def filter_path_matching(streams, matcher):
    for stream in streams:
        if matcher in stream["url"]: yield stream

def filter_max_bitrate(streams, limit=-1):
    for stream in streams:
        if limit <= 0 or bandwidth_from_stream(stream) <= limit: yield stream

def bandwidth_from_stream(stream):
    try: return int(stream["meta"]["quality"].split(' ', 1)[0])
    except: return -1

def cmp_bandwidth(a, b):
    return cmp(bandwidth_from_stream(a), bandwidth_from_stream(b))

def boxeespecific_quality_from_stream(stream):
    if bandwidth_from_stream(stream) < 0: return 'A'
    if bandwidth_from_stream(stream) < 1000: return '0'
    else: return '1'

def pirateplayable_item(item, bitrate_limit):
    streams = get_streams(item.GetPath())

    print str(streams)
    if len(streams) == 0:
        raise NoStreamsError()

    streams_generator = filter_path_matching(streams, "m3u8")
    streams_generator = filter_max_bitrate(streams, bitrate_limit)

    streams = []
    streams.extend(streams_generator)
    streams.sort(cmp_bandwidth, reverse=True)

    BPLog("Available streams are:")
    for stream in streams:
        BPLog("%d" %bandwidth_from_stream(stream))

    if len(streams) == 0:
        raise NoSuitableStreamError()

    stream = streams[0]
    params = { "quality": boxeespecific_quality_from_stream(stream) }
    item.SetPath("playlist://%s?%s" %(quote_plus(stream["url"]), urlencode(params)))
    item.SetContentType("application/vnd.apple.mpegurl")
    return item

