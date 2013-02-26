import mc, time
from wlps import WlpsClient
from wlps_mc import category_to_list_item, show_to_list_item, episode_to_list_item
from logger import BPLog,BPTraceEnter,BPTraceExit,Level
from itertools import imap, islice

focusedCategoryNo = -1
focusedTitleNo = -1
focusedEpisodeNo = -1
labelPrograms = ""
labelEpisodes = ""
selectedTitleId = 0
client = None

def initiate():
    global focusedCategoryNo
    global focusedTitleNo
    global focusedEpisodeNo
    global labelPrograms
    global labelEpisodes
    global client

    BPTraceEnter()

    client = WlpsClient()

    if len(mc.GetWindow(14000).GetList(1000).GetItems()) == 0:
        BPLog("No programs in program listing. Loading defaults.", Level.DEBUG)
        loadCategories()
        time.sleep(0.001) #Äckelfulhack
        load_recommended_episodes()
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
    title = cItem.GetLabel()
    load_shows(shows, title)

def load_shows(shows, title):
    BPTraceEnter()
    mc.ShowDialogWait()
    set_shows([] ,"")
    set_episodes([],"")
    try:
        set_shows(islice(shows, 0, 20), title)
        mc.HideDialogWait()
        add_shows(islice(shows, 20, None), title)
    except Exception, e:
        BPLog("Laddning av program misslyckades: %s" %e, Level.ERROR)
        mc.HideDialogWait()
    BPLog("Finished loading programs in category %s." %title, Level.DEBUG)
    BPTraceExit()

def load_recommended_episodes():
    load_episodes(client.get_recommended_episodes(), "Rekommenderade program")

def load_recent_episodes():
    load_episodes(islice(client.get_latest_episodes(), 0, 100), "Nya program")

def load_episodes_from_show():
    cList = mc.GetWindow(14000).GetList(2000)
    cItem = cList.GetItem(cList.GetFocusedItem())
    episodes = client.get_episodes_from_id(cItem.GetProperty("id"))
    title = cItem.GetLabel()
    load_episodes(episodes, title)

def load_episodes(episodes, title):
    global selectedTitleId

    BPTraceEnter()
    mc.ShowDialogWait()
    set_episodes([],"")
    try:
        set_episodes(islice(episodes, 0, 20), title)
        mc.HideDialogWait()
        add_episodes(islice(episodes, 20, None), title)
    except Exception, e:
        BPLog("Laddning av avsnitt misslyckades: %s" %e, Level.ERROR)
        mc.HideDialogWait()
    BPLog("Finished loading episodes in category %s." %title, Level.DEBUG)
    BPTraceExit()

def set_shows(items, title):
    global labelPrograms

    BPTraceEnter()
    win = mc.GetWindow(14000)

    labelPrograms = title
    win.GetLabel(2001).SetLabel(title)

    target = win.GetList(2000)
    mc_list = mc.ListItems()
    for item in imap(show_to_list_item, items):
        mc_list.append(item)
    target.SetItems(mc_list)
    if len(mc_list) > 0:
        target.SetFocus()
    BPTraceExit()

def add_shows(items, title):
    BPTraceEnter()
    win = mc.GetWindow(14000)
    target = win.GetList(2000)
    mc_list = target.GetItems()
    for item in items:
        mc_list.append(show_to_list_item(item))
    focusedIndex = target.GetFocusedItem()
    target.SetItems(mc_list)
    target.SetFocusedItem(focusedIndex)
    BPTraceExit()

def set_episodes(items, title):
    global labelEpisodes

    BPTraceEnter()
    win = mc.GetWindow(14000)

    win.GetLabel(3002).SetLabel(title)
    labelEpisodes = title

    target = win.GetList(3001)
    mc_list = mc.ListItems()
    for item in imap(episode_to_list_item, items):
        mc_list.append(item)
    target.SetItems(mc_list)

    if len(mc_list) > 0:
        target.SetFocus()
    BPTraceExit()

def add_episodes(items, title):
    BPTraceEnter()
    win = mc.GetWindow(14000)
    target = win.GetList(3001)
    mc_list = target.GetItems()
    for item in items:
        mc_list.append(episode_to_list_item(item))
    focusedIndex = target.GetFocusedItem()
    target.SetItems(mc_list)
    target.SetFocusedItem(focusedIndex)
    BPTraceExit()

def showLive():
    global selectedTitleId

    BPTraceEnter()
    mc.ShowDialogWait()
    selectedTitleId = str("")
    set_shows(mc.ListItems(), "")
    set_episodes(mc.ListItems(), "")
    try:
            set_episodes(playmc.GetLiveEpisodes(), "Livesändningar")
    except Exception, e:
        BPLog("Could not show live episodes: %s" %e, Level.ERROR)
    mc.HideDialogWait()
    BPTraceExit()

def showRecent():
    global selectedTitleId

    BPTraceEnter()
    mc.ShowDialogWait()
    selectedTitleId = str("")
    set_shows(mc.ListItems(),"")
    set_episodes(mc.ListItems(),"")
    try:
            set_episodes(playmc.GetRecentEpisodes(), "Senaste avsnitt")
    except Exception, e:
        BPLog("Could not show recent episodes: %s" %e, Level.ERROR)
    mc.HideDialogWait()
    BPTraceExit()

def search():
    global selectedTitleId

    BPTraceEnter()
    mc.ShowDialogWait()
    selectedTitleId = str("")
    set_shows(mc.ListItems(),"")
    set_episodes(mc.ListItems(),"")
    try:
        searchTerm = mc.GetWindow(14000).GetEdit(110).GetText()
        try:
            searchTerm = searchTerm.decode("utf-8")
            result = playmc.SearchEpisodesAndSamples(searchTerm.encode("latin-1"))
            set_episodes(result, str(len(result)) + " träffar på \"" + searchTerm.encode("utf-8") + "\"")
        except Exception, e:
            BPLog("Could not search for %s: %s" %(searchTerm.encode("utf-8"), e), Level.ERROR)
    except Exception, e:
        BPLog("Could not search: %s" %e, Level.ERROR)
    mc.HideDialogWait()
    BPTraceExit()

def appendSearch(str):
    BPTraceEnter()
    try:
        searchBar = mc.GetWindow(14000).GetEdit(110)
        searchBar.SetText(searchBar.GetText()+str)
    except Exception, e:
        BPLog("Could not append searchbar with %s. Exception: %s" %(str,e), Level.ERROR)
    BPTraceExit()

def playVideo():
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
    BPTraceExit()

def populateNextSamplesPage():
    BPTraceEnter()
    mc.ShowDialogWait()

    try:
        if len(selectedTitleId) > 0:
            sampleList = mc.GetWindow(14000).GetList(3001)
            # Remember the item that was focused when the action was initiated
            originallyFocusedItemNo = sampleList.GetFocusedItem()
            list = sampleList.GetItems()
            # This check prevents loading of next page
            # before the page to be loaded is loaded
            # due to ondown triggered twice on the same item (ondown, up, ondown)
            if originallyFocusedItemNo + 1 == len(list):
                # There appears to be a bug in the SVT XML load routine so that
                # the same item is loaded as both the last on page 2 (101-200) and
                # the first on page 3 (201-300)
                newItems = playmc.GetNextSamplesPage(selectedTitleId, sampleList)
                if len(newItems) > 0:
                    for newItem in newItems:
                        list.append(newItem)
                    # If the focused item is still the same (the last)
                    # advance to the first newly loaded item
                    # otherwise keep the focused item
                    # if for example the user scrolled up during the load
                    focusedItemNo = sampleList.GetFocusedItem()
                    if focusedItemNo == originallyFocusedItemNo:
                        focusedItemNo = focusedItemNo + 1
                    sampleList.SetItems(list)
                    sampleList.SetFocusedItem(focusedItemNo)
    except Exception, e:
        BPLog("Could not load next sample page. Exception: %s" %(e), Level.ERROR)
    mc.HideDialogWait()
    BPTraceExit()
