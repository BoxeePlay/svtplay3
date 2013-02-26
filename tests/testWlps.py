# Must be run from same folder for relative import path to work!
import sys
sys.path.append("../tv.boxeeplay.svtplay3")
from wlps import WlpsClient
from wlps_mc import category_to_list_item, show_to_list_item, episode_to_list_item
from logger import Level, BPLog, SetEnabledPlus
import simplejson
import itertools

SetEnabledPlus(Level.DEBUG, True)
client = WlpsClient()
BPLog("START")
categories = []
categories.extend(client.categories)
BPLog("Categories fetched first time. All " + str(len(categories)) + " of them!")
categories = []
categories.extend(client.categories)
#BPLog(simplejson.dumps(categories, indent=2))
BPLog("Categories fetched second time. Should be cached! All " + str(len(categories)) + " of them!")
shows = []
shows.extend(client.get_shows(categories[2]))
#BPLog(simplejson.dumps(shows, indent=2))
BPLog("Fetched " + str(len(shows)) + " shows for category nr 2: " + categories[2]["title"])
episodes = []
episodes.extend(client.get_episodes(shows[7]))
#BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Fetched " + str(len(episodes)) + " episodes for shows nr 7: " + shows[7]["title"])
episodes = []
episodes.extend(client.get_recommended_episodes())
#BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Recommended episodes fetched. All " + str(len(episodes)) + " of them!")
episodes = []
episodes.extend(itertools.islice(client.get_latest_episodes(), 40))
#BPLog(simplejson.dumps(episodes, indent=2))
BPLog("Latest episodes fetched. All " + str(len(episodes)) + " of them!")
#episodes = []
#episodes.extend(client.get_iterable(client.get_list_endpoint("episode")))
#BPLog("_All_ episodes fetched. API haz bugz!")

BPLog("### Transform tests ###")
category = {"id": "6",
            "resource_uri": "/v1/category/6/",
            "shows": [
                "/v1/show/479/",
                "/v1/show/485/",
                "/v1/show/497/",
                "/v1/show/499/",
                "/v1/show/730/",
                "/v1/show/777/",
                "/v1/show/795/",
                "/v1/show/796/",
                "/v1/show/537/",
                "/v1/show/540/",
                "/v1/show/560/",
                "/v1/show/561/",
                "/v1/show/852/",
                "/v1/show/590/",
                "/v1/show/620/",
                "/v1/show/625/",
                "/v1/show/845/",
                "/v1/show/650/",
                "/v1/show/662/",
                "/v1/show/675/",
                "/v1/show/678/",
                "/v1/show/682/",
                "/v1/show/849/"
            ],
            "title": "Film & Drama"}
category_item = category_to_list_item(category)
BPLog("Transformed category: " + str(category_item))

show     = {"episodes": [
                "/v1/episode/9393/",
                "/v1/episode/9396/",
                "/v1/episode/9394/",
                "/v1/episode/9395/",
                "/v1/episode/13995/"
            ],
            "id": "463",
            "resource_uri": "/v1/show/463/",
            "title": "Akuten"}
show_item = show_to_list_item(show)
BPLog("Transformed show: " + str(show_item))

episode = {"date_available_until": "2013-03-22T19:34:57.081480+00:00",
           "date_broadcasted": "2012-03-22T14:10:00+00:00",
           "date_created": "2013-02-12T20:34:57.439902+00:00",
           "date_downloaded": None,
           "description": "",
           "http_status": 200,
           "http_status_checked_date": "2013-02-24T22:00:03.605942+00:00",
           "id": "9377",
           "length": "0 sek",
           "recommended": False,
           "resource_uri": "/v1/episode/9377/",
           "show": "/v1/show/462/",
           "state": 0,
           "thumbnail_url": None,
           "title": "SVT Nyheter Live",
           "url": "http://www.svtplay.se/video/116538/svt-nyheter-live-22-3"}
episode_item = episode_to_list_item(episode)
BPLog("Transformed episode: " + str(episode_item))



# TODO
#
# Implement:
# * Sort shows by title
