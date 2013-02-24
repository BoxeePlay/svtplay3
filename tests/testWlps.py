# Must be run from same folder for relative import path to work!
import sys
sys.path.append("../tv.boxeeplay.svtplay3")
from wlps import WlpsClient
from logger import Level, BPLog, SetEnabledPlus
import simplejson
import itertools

SetEnabledPlus(Level.DEBUG, True)
client = WlpsClient()
BPLog("START")
categories = []
categories.extend(client.categories)
BPLog("Categories fetched first time.")
categories = []
categories.extend(client.categories)
BPLog(simplejson.dumps(categories, indent=2))
BPLog("Categories fetched second time. Should be cached!")
shows = []
shows.extend(client.get_shows(categories[2]))
BPLog(simplejson.dumps(shows, indent=2))
BPLog("Shows fetched for category nr 2: " + categories[2]["title"])
episodes = []
episodes.extend(client.get_episodes(shows[7]))
BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Episodes fetched for episode nr 7: " + shows[7]["title"])
episodes = []
episodes.extend(client.get_recommended_episodes())
BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Recommended episodes fetched. All " + str(len(episodes)) + " of them!")
episodes = []
episodes.extend(itertools.islice(client.get_latest_episodes(), 40))
BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Latest episodes fetched. All " + str(len(episodes)) + " of them!")
#episodes = []
#episodes.extend(client.get_iterable(client.get_list_endpoint("episode")))
#BPLog("_All_ episodes fetched. API haz bugz!")


# TODO
#
# Implement:
# * Sort shows by title
