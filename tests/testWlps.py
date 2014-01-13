#encoding:utf-8
# Must be run from same folder for relative import path to work!
import sys
sys.path.append("../tv.boxeeplay.svtplay3")
from wlps import WlpsClient
from wlps_mc import category_to_list_item, show_to_list_item, episode_to_list_item, has_episodes
from logger import Level, BPLog, SetEnabledPlus
import simplejson
import itertools
import ip_info

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

mc_categories = itertools.imap(category_to_list_item, categories)
mc_cat_list = []
mc_cat_list.extend(mc_categories)
BPLog("mc items for categories are " + str(len(mc_cat_list)))

shows = []
shows.extend(client.get_shows(categories[2]))
#BPLog(simplejson.dumps(shows, indent=2))
BPLog("Fetched " + str(len(shows)) + " shows for category nr 2: " + categories[2]["title"])

filtered_shows = []
filtered_shows.extend(itertools.ifilter(has_episodes, shows))
BPLog("Fetched " + str(len(filtered_shows)) + " shows with episodes for category nr 2: " + categories[2]["title"])

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
BPLog("Transformed category:")
BPLog(simplejson.dumps(category_item.to_object(), indent=2))

show = {
        "category": "/v1/category/5/",
        "episodes": [
            "/v1/episode/4306/",
            "/v1/episode/4307/"
        ],
        "id": "300",
        "resource_uri": "/v1/show/300/",
        "thumbnail": "shows/image_5_6.jpg",
        "thumbnail_url": "http://www.svt.se/cachable_image/1356099963000/svts/article927529.svt/ALTERNATES/large/rapport_affisch_ny.jpg",
        "title": "Rapport",
        "url": "http://www.svtplay.se/rapport"
    }
show_item = show_to_list_item(show)
BPLog("Transformed show:")
BPLog(simplejson.dumps(show_item.to_object(), indent=2))

episode = {
        "date_available_until": "2013-03-13T22:04:28.295345+00:00",
        "date_broadcasted": "2013-03-07T08:00:00+00:00",
        "date_created": "2013-03-07T23:04:28.298583+00:00",
        "date_downloaded": None,
        "description": "SVT Rapport är Sveriges största nyhetsprogram med nyheter dygnet runt i SVT1, SVT Forum och SVT Play.",
        "http_status": 200,
        "http_status_checked_date": "2013-03-09T22:10:15.070459+00:00",
        "id": "4307",
        "kind_of": 1,
        "length": "5 min",
        "recommended": False,
        "resource_uri": "/v1/episode/4307/",
        "show": "/v1/show/300/",
        "state": 0,
        "thumbnail_url": "http://www.svt.se/cachable_image/1362644099000/svts/article1079534.svt/ALTERNATES/extralarge/default_title",
        "title": "Rapport - 7/3 09:00 ",
        "title_slug": "Rapport - 7-3 09:00",
        "url": "http://www.svtplay.se/video/1079535/7-3-09-00",
        "viewable_in": 1,
        "viewable_on_device": 1
    }
episode_item = episode_to_list_item(episode)
BPLog("Transformed episode:")
BPLog(simplejson.dumps(episode_item.to_object(), indent=2))

try:
    BPLog("Is in sweden: " + str(ip_info.get_country_code() == "SE"))
    BPLog("Country: " + ip_info.get_country_name() + ", Code: " + ip_info.get_country_code())
except Exception, e:
    BPLog(str(e))
