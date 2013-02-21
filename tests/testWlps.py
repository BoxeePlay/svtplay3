# Must be run from same folder for relative import path to work!
import sys
sys.path.append("../tv.boxeeplay.svtplay3")
from wlps import WlpsClient
from logger import Level, BPLog, SetEnabledPlus

SetEnabledPlus(Level.DEBUG, True)
client = WlpsClient()
BPLog("START")
categories = []
categories.extend(client.categories)
BPLog("Categories fetched first time.")
categories = []
categories.extend(client.categories)
BPLog(str(categories))
BPLog("Categories fetched second time. Should be cached!")
#episodes = []
#episodes.extend(client.get_iterable(client.get_list_endpoint("episode")))
#BPLog("_All_ episodes fetched. API haz bugz!")


# TODO
#
# Implement:
# * Latest episodes as WlpsIterable
# * Get shows from category
# * Get episodes from show
