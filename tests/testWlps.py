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
shows = []
shows.extend(client.get_shows(categories[2]))
BPLog(str(shows))
BPLog("Shows fetched for category nr 2: " + categories[2]["title"])
episodes = []
episodes.extend(client.get_episodes(shows[5]))
BPLog(str(episodes))
BPLog("Episodes fetched for episode nr 5: " + shows[5]["title"])
#episodes = []
#episodes.extend(client.get_iterable(client.get_list_endpoint("episode")))
#BPLog("_All_ episodes fetched. API haz bugz!")


# TODO
#
# Implement:
# * Latest episodes as WlpsIterable
# * Recommended episodes as WlpsIterable
# * Sort shows and episodes by title
