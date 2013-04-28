#encoding:utf-8
#author:Andreas Pehrson
#project:boxeeplay.tv

import mc, time, ip_info
from wlps import WlpsClient
from wlps_mc import category_to_list_item, show_to_list_item, episode_to_list_item, set_outside_sweden, episode_list_item_to_playable
from logger import BPLog,BPTraceEnter,BPTraceExit,Level
from itertools import islice
from urllib import quote_plus
import mixpanel_client as tracker

VERSION = "SVTPlay 3.0.0"
NO_SHOWS_TEXT = "Inga program laddade"
NO_EPISODES_TEXT = "Inga avsnitt för det här programmet"
BX_JSACTIONS_URL = "http://boxeeplay.tv/bx-jsactions/svtplay3.js"

initiated = False
category_list_index = -1
show_list_index = -1
episode_list_index = -1
focused_list = 1000
labelPrograms = ""
labelEpisodes = ""
client = None
country_code = "unknown"
is_sweden = True

def initiate():
    global category_list_index
    global show_list_index
    global episode_list_index
    global labelPrograms
    global labelEpisodes
    global country_code
    global is_sweden
    global client
    global initiated

    BPTraceEnter()
    mc.ShowDialogWait()

    if not initiated:
        try:
            client = WlpsClient()
        except Exception, e:
            BPLog("Could not set up API client: " + str(e))
            show_error_and_exit(message="Kunde inte kontakta API-servern. Appen stängs ner...")

        # TODO Do geo lookup in background..
        # TODO Do tracking in background..
        try:
            country_code = ip_info.get_country_code()
            is_sweden = country_code == "SE"
        except Exception, e:
            BPLog("Could not retreive physical location of client: " + str(e))

        BPLog("We are in sweden: " + str(is_sweden))
        if not is_sweden:
            set_outside_sweden(True)
            mc.GetWindow(14000).GetLabel(14002).SetLabel("Du är inte i Sverige\nAllt material kan inte visas")
        else:
            set_outside_sweden(False)
            mc.GetWindow(14000).GetLabel(14002).SetLabel("")

        initiated = True

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

        mc.GetWindow(14000).GetList(focused_list).SetFocus()
        mc.GetWindow(14000).GetList(1000).SetFocusedItem(category_list_index)
        mc.GetWindow(14000).GetList(2000).SetFocusedItem(show_list_index)
        mc.GetWindow(14000).GetList(3001).SetFocusedItem(episode_list_index)
        mc.HideDialogWait()

    BPLog("Initiate complete.")
    BPTraceExit()

def loadCategories():
    BPTraceEnter()
    mc.ShowDialogWait()
    win = mc.GetWindow(14000)
    target = win.GetList(1000)
    win.GetLabel(2003).SetLabel(NO_SHOWS_TEXT)
    win.GetLabel(3003).SetLabel(NO_EPISODES_TEXT)
    items = mc.ListItems()
    for cat in client.categories:
        items.append(category_to_list_item(cat))
    target.SetItems(items)
    mc.HideDialogWait()
    BPLog("Successfully loaded all categories.", Level.DEBUG)
    BPTraceExit()

def load_shows_from_category():
    global focused_list

    cList = mc.GetWindow(14000).GetList(1000)
    focused_list = 1000
    cItem = cList.GetItem(cList.GetFocusedItem())
    shows = client.get_shows_from_id(cItem.GetProperty("id"))
    load_shows(shows, cItem)

    latest_episodes_item = mc.ListItem()
    latest_episodes_item.SetLabel("Senaste " + cItem.GetLabel())
    set_episodes(latest_for_category, latest_episodes_item)

def load_shows(shows, category_item):
    BPTraceEnter()
    mc.ShowDialogWait()
    set_episodes([], mc.ListItem())
    try:
        set_shows(islice(shows, 0, 20), category_item)
        mc.HideDialogWait()
        add_shows(islice(shows, 20, None), category_item)
    except Exception, e:
        mc.HideDialogWait()
        show_error_and_continue(message="Laddning av program misslyckades. Kollat internetanslutningen?\n\n" + str(e))
    tracker.track("Load Category", { "title": category_item.GetLabel(),
                                     "Id": mc.GetUniqueId()
                                   })
    BPLog("Finished loading programs in category %s." %category_item.GetLabel(), Level.DEBUG)
    BPTraceExit()

def load_recommended_episodes():
    recommended_item = mc.ListItem()
    recommended_item.SetLabel("Rekommenderade program")
    recommended_item.SetProperty("category", "preset-category")
    set_shows([], mc.ListItem())
    load_episodes(client.get_recommended_episodes(), recommended_item)

def load_live():
    live_item = mc.ListItem()
    live_item.SetLabel("Kanaler")
    live_item.SetProperty("category", "preset-category")
    set_shows([], mc.ListItem())
    load_shows(client.get_channels(), live_item)

def load_episodes_from_show():
    global focused_list

    cList = mc.GetWindow(14000).GetList(2000)
    focused_list = 2000
    cItem = cList.GetItem(cList.GetFocusedItem())
    if cItem.GetProperty("playable"):
        play_item(cItem)
    else:
        episodes = client.get_episodes_from_id(cItem.GetProperty("id"))
        store_show_list()
        load_episodes(episodes, cItem)

def load_episodes(episodes, show_item):
    BPTraceEnter()
    mc.ShowDialogWait()
    try:
        set_episodes(islice(episodes, 0, 20), show_item)
        mc.HideDialogWait()
        add_episodes(islice(episodes, 20, None), show_item)
    except Exception, e:
        mc.HideDialogWait()
        show_error_and_continue(message="Laddning av avsnitt misslyckades. Kollat internetanslutningen?\n\n" + str(e))
    tracker.track("Load Show", { "title": show_item.GetLabel(),
                                 "Id": mc.GetUniqueId(),
                                 "category": show_item.GetProperty("category")
                               })
    BPLog("Finished loading episodes in category %s." %show_item.GetLabel(), Level.DEBUG)
    BPTraceExit()

def set_shows(items, category_item):
    global labelPrograms
    global show_list_index

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
    show_list_index = 0
    if len(mc_list) > 0:
        win.GetLabel(2003).SetLabel("")
        target.SetFocus()
    else:
        win.GetLabel(2003).SetLabel(NO_SHOWS_TEXT)
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
    global episode_list_index

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
    episode_list_index = 0

    if len(mc_list) > 0:
        win.GetLabel(3003).SetLabel("")
        target.SetFocus()
    else:
        win.GetLabel(3003).SetLabel(NO_EPISODES_TEXT)

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

def click_episode():
    global focused_list

    focused_list = 3001
    item_list = mc.GetWindow(14000).GetList(focused_list)
    item = item_list.GetItem(item_list.GetFocusedItem())
    play_item(item)

def play_item(item):
    global category_list_index
    global show_list_index
    global episode_list_index
    BPTraceEnter()

    # Remember the selections in the lists
    store_category_list()
    store_show_list()
    store_episode_list()

    play_item = episode_list_item_to_playable(item)
    play_item.SetPath("flash://boxeeplay.tv/src=%s&bx-jsactions=%s" %
                      (quote_plus(play_item.GetPath()),quote_plus(BX_JSACTIONS_URL)))
    BPLog("Playing clip \"%s\" with path \"%s\" and bitrate %s." %(item.GetLabel(), item.GetPath(), item.GetProperty("bitrate")))
    mc.GetPlayer().Play(play_item)

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

def move_left_from_episode_list():
    store_episode_list()
    win = mc.GetWindow(14000)
    menu = win.GetControl(100)
    shows = win.GetList(2000)
    if shows.GetItems():
        restore_show_list()
    else:
        menu.SetFocus()

def move_right_from_menu():
    win = mc.GetWindow(14000)
    shows = win.GetList(2000)
    episodes = win.GetList(3001)
    if shows.GetItems():
        restore_show_list()
    elif episodes.GetItems():
        restore_episode_list()

def move_left_from_show_list():
    store_show_list()
    mc.GetWindow(14000).GetControl(100).SetFocus()

def move_right_from_show_list():
    store_show_list()
    win = mc.GetWindow(14000)
    episodes = win.GetList(3001)
    if episodes.GetItems():
        restore_episode_list()

def store_show_list():
    global show_list_index
    show_list_index = mc.GetWindow(14000).GetList(2000).GetFocusedItem()

def restore_show_list():
    win = mc.GetWindow(14000)
    win.GetControl(2000).SetFocus()
    win.GetList(2000).SetFocusedItem(show_list_index)

def store_episode_list():
    global episode_list_index
    episode_list_index = mc.GetWindow(14000).GetList(3001).GetFocusedItem()

def restore_episode_list():
    win = mc.GetWindow(14000)
    win.GetControl(3001).SetFocus()
    win.GetList(3001).SetFocusedItem(episode_list_index)

def store_category_list():
    global category_list_index
    category_list_index = mc.GetWindow(14000).GetList(1000).GetFocusedItem()

def restore_category_list():
    win = mc.GetWindow(14000)
    win.GetControl(100).SetFocus()
    win.GetList(1000).SetFocusedItem(category_list_index)

def show_error_and_exit(title = "Tyvärr", message = "Ett oväntat fel har inträffat. Appen stängs..."):
    show_error_and_continue(title, message)
    mc.CloseWindow()

def show_error_and_continue(title = "Tyvärr", message = "Ett oväntat fel har inträffat. Appen stängs..."):
    mc.ShowDialogOk(title, message)
