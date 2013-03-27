import mc, time, ip_info
from wlps import WlpsClient
from wlps_mc import category_to_list_item, show_to_list_item, episode_to_list_item, set_outside_sweden
from logger import BPLog,BPTraceEnter,BPTraceExit,Level
from itertools import islice
import mixpanel_client as tracker

VERSION = "SVTPlay 3.0.0"

focusedCategoryNo = -1
focusedTitleNo = -1
focusedEpisodeNo = -1
labelPrograms = ""
labelEpisodes = ""
selectedTitleId = 0
client = WlpsClient()

# TODO Do geo lookup in background..
# TODO Do tracking in background..
try:
    country_code = ip_info.get_country_code()
    is_sweden = country_code == "SE"
except Exception, e:
    country_code = "unknown"
    is_sweden = True
    BPLog("Could not retreive physical location of client: " + str(e))

def initiate():
    global focusedCategoryNo
    global focusedTitleNo
    global focusedEpisodeNo
    global labelPrograms
    global labelEpisodes

    BPTraceEnter()

    BPLog("We are in sweden: " + str(is_sweden))
    if not is_sweden:
        set_outside_sweden(True)
        mc.GetWindow(14000).GetLabel(14002).SetLabel("Du är inte i Sverige")
    else:
        set_outside_sweden(False)
        mc.GetWindow(14000).GetLabel(14002).SetLabel("")

    if len(mc.GetWindow(14000).GetList(1000).GetItems()) == 0:
        BPLog("No programs in program listing. Loading defaults.", Level.DEBUG)
        loadCategories()
        time.sleep(0.001) #Äckelfulhack
        load_recommended_episodes()
        tracker.track("Initated", {"Locale": mc.GetGeoLocation(),
                                   "Platform": mc.GetPlatform(),
                                   "Country Code": country_code,
                                   "In Sweden": str(is_sweden)
                                   })
    else:
        #Restore last focus
        mc.GetWindow(14000).GetLabel(2001).SetLabel(labelPrograms)
        mc.GetWindow(14000).GetLabel(3002).SetLabel(labelEpisodes)
        if focusedCategoryNo >= 0:
            categoryList = mc.GetWindow(14000).GetList(1000)
            categoryList.SetFocusedItem(focusedCategoryNo)
        if focusedTitleNo >= 0:
            titleList = mc.GetWindow(14000).GetList(2000)
            titleList.SetFocusedItem(focusedTitleNo)
        if focusedEpisodeNo >= 0:
            episodeList = mc.GetWindow(14000).GetList(3001)
            episodeList.SetFocusedItem(focusedEpisodeNo)

    BPLog("Initiate complete.")
    BPTraceExit()

def loadCategories():
    BPTraceEnter()
    mc.ShowDialogWait()
    win = mc.GetWindow(14000)
    target = win.GetList(1000)
    items = mc.ListItems()
    for cat in client.categories:
        items.append(category_to_list_item(cat))
    target.SetItems(items)
    mc.HideDialogWait()
    BPLog("Successfully loaded all categories.", Level.DEBUG)
    BPTraceExit()

def load_shows_from_category():
    cList = mc.GetWindow(14000).GetList(1000)
    cItem = cList.GetItem(cList.GetFocusedItem())
    shows = client.get_shows_from_id(cItem.GetProperty("id"))
    load_shows(shows, cItem)

def load_shows(shows, category_item):
    BPTraceEnter()
    mc.ShowDialogWait()
    set_shows([] , mc.ListItem())
    set_episodes([], mc.ListItem())
    try:
        set_shows(islice(shows, 0, 20), category_item)
        mc.HideDialogWait()
        add_shows(islice(shows, 20, None), category_item)
    except Exception, e:
        BPLog("Laddning av program misslyckades: %s" %e, Level.ERROR)
        mc.HideDialogWait()
    tracker.track("Load Category", { "title": category_item.GetLabel(),
                                     "Id": mc.GetUniqueId()
                                   })
    BPLog("Finished loading programs in category %s." %category_item.GetLabel(), Level.DEBUG)
    BPTraceExit()

def load_recommended_episodes():
    recommended_item = mc.ListItem()
    recommended_item.SetLabel("Rekommenderade program")
    recommended_item.SetProperty("category", "preset-category")
    load_episodes(client.get_recommended_episodes(), recommended_item)

def load_recent_episodes():
    recent_item = mc.ListItem()
    recent_item.SetLabel("Nya program")
    recent_item.SetProperty("category", "preset-category")
    load_episodes(islice(client.get_latest_episodes(), 0, 40), recent_item)

def load_episodes_from_show():
    cList = mc.GetWindow(14000).GetList(2000)
    cItem = cList.GetItem(cList.GetFocusedItem())
    episodes = client.get_episodes_from_id(cItem.GetProperty("id"))
    load_episodes(episodes, cItem)

def load_episodes(episodes, show_item):
    global selectedTitleId

    BPTraceEnter()
    mc.ShowDialogWait()
    set_episodes([], mc.ListItem())
    try:
        set_episodes(islice(episodes, 0, 20), show_item)
        mc.HideDialogWait()
        add_episodes(islice(episodes, 20, None), show_item)
    except Exception, e:
        BPLog("Laddning av avsnitt misslyckades: %s" %e, Level.ERROR)
        mc.HideDialogWait()
    tracker.track("Load Show", { "title": show_item.GetLabel(),
                                 "Id": mc.GetUniqueId(),
                                 "category": show_item.GetProperty("category")
                               })
    BPLog("Finished loading episodes in category %s." %show_item.GetLabel(), Level.DEBUG)
    BPTraceExit()

def set_shows(items, category_item):
    global labelPrograms

    BPTraceEnter()
    win = mc.GetWindow(14000)

    title = category_item.GetLabel()
    labelPrograms = title
    win.GetLabel(2001).SetLabel(title)

    target = win.GetList(2000)
    mc_list = mc.ListItems()
    for item in items:
        mc_list.append(show_to_list_item(item, title))
    target.SetItems(mc_list)
    if len(mc_list) > 0:
        target.SetFocus()
    BPTraceExit()

def add_shows(items, category_item):
    BPTraceEnter()
    win = mc.GetWindow(14000)
    target = win.GetList(2000)
    mc_list = target.GetItems()
    for item in items:
        mc_list.append(show_to_list_item(item, category_item.GetLabel()))
    focusedIndex = target.GetFocusedItem()
    target.SetItems(mc_list)
    target.SetFocusedItem(focusedIndex)
    BPTraceExit()

def set_episodes(items, show_item):
    global labelEpisodes

    BPTraceEnter()
    win = mc.GetWindow(14000)

    title = show_item.GetLabel()
    win.GetLabel(3002).SetLabel(title)
    labelEpisodes = title

    target = win.GetList(3001)
    mc_list = mc.ListItems()
    for item in items:
        mc_list.append(episode_to_list_item( item
                                           , show_item.GetProperty("category")
                                           , title
                                           ))
    target.SetItems(mc_list)

    if len(mc_list) > 0:
        target.SetFocus()
    BPTraceExit()

def add_episodes(items, show_item):
    BPTraceEnter()
    win = mc.GetWindow(14000)
    target = win.GetList(3001)
    mc_list = target.GetItems()
    for item in items:
        mc_list.append(episode_to_list_item( item
                                           , show_item.GetProperty("category")
                                           , show_item.GetLabel()
                                           ))
    focusedIndex = target.GetFocusedItem()
    target.SetItems(mc_list)
    target.SetFocusedItem(focusedIndex)
    BPTraceExit()

def play_video():
    global focusedCategoryNo
    global focusedTitleNo
    global focusedEpisodeNo
    BPTraceEnter()

    # Remember the selections in the lists
    categoryList = mc.GetWindow(14000).GetList(1000)
    if len(categoryList.GetItems()) > 0:
        focusedCategoryNo = categoryList.GetFocusedItem()
    else:
        focusedCategoryNo = -1

    titleList = mc.GetWindow(14000).GetList(2000)
    if len(titleList.GetItems()) > 0:
        focusedTitleNo = titleList.GetFocusedItem()
    else:
        focusedTitleNo = -1

    episodeList = mc.GetWindow(14000).GetList(3001)
    if len(episodeList.GetItems()) > 0:
        focusedEpisodeNo = episodeList.GetFocusedItem()
    else:
        focusedEpisodeNo = -1

    item = episodeList.GetItem(focusedEpisodeNo)
    BPLog("Playing clip \"%s\" with path \"%s\" and bitrate %s." %(item.GetLabel(), item.GetPath(), item.GetProperty("bitrate")))
    mc.GetPlayer().Play(item)

    if (item.GetProperty("episode")):
        item_type="Episode"
    else:
        item_type="Clip"
    tracker.track("Play", { "title": item.GetLabel(),
                            "url": item.GetPath(),
                            "Id": mc.GetUniqueId(),
                            "type": item_type,
                            "show": item.GetProperty("show"),
                            "category": item.GetProperty("category")
                            })
    BPTraceExit()

