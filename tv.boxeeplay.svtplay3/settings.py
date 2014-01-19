#encoding:utf-8
#author:Andreas Pehrson
#project:boxeeplay.tv

import mc
from logger import BPLog, Level

USE_PIRATEPLAY_KEY = "use_pirateplay"
BITRATE_LIMIT_KEY = "bitrate_limit"

def conf():
    return mc.GetApp().GetLocalConfig()

def activate():
    decision = mc.ShowDialogSelect("Jag vill ändra...", [get_option_stream_source(), get_option_bitrate_limit()])
    if decision == 0:
        activate_stream_source_selection()
    if decision == 1:
        activate_bitrate_limit_selection()

def activate_stream_source_selection():
    cont = mc.ShowDialogConfirm("Ändra Uppspelningskälla", "Traditionellt öppnas videor i den inbyggda webbläsaren. Med pirateplay kan vi istället öppna videoströmmarna direkt i Boxee. Då startar de snabbare men med låst bitrate/kvalitet.", "Avbryt", "Fortsätt")
    if not cont:
        return

    opt_pirateplay = "Pirateplay om möjligt"
    opt_webonly = "Endast webbläsaren"
    if get_use_pirateplay(): opt_pirateplay = "[valt] " + opt_pirateplay
    else: opt_webonly = "[valt] " + opt_webonly
    decision = mc.ShowDialogSelect("Ändra Uppspelningskälla", [opt_pirateplay, opt_webonly])

    if decision == 0:
        set_use_pirateplay(True)
    elif decision == 1:
        set_use_pirateplay(False)
    else:
        BPLog("Stream source dialog cancelled")
        return


def activate_bitrate_limit_selection():
    cont = mc.ShowDialogConfirm("Ändra bandbreddsbegränsning", "När Pirateplay används spelar vi normalt upp strömmarna med högsta möjliga kvalitet. Har du då problem med hackig och buffrande uppspelning kan du här ställa in en gräns för hur hög bitrate vi får välja.", "Avbryt", "Fortsätt")
    if not cont:
        return

    options = [ "Obegränsat", "2500 Kbps", "2000 Kbps", "1500 Kbps", "1000 Kbps", "500 Kbps" ]
    option_values = [ -1, 2500, 2000, 1500, 1000, 500 ]
    limit = get_bitrate_limit()
    active_value_index = 0
    try: active_value_index = option_values.index(limit)
    except: BPLog("Value %d not found in list of bitrate limit options" %limit, Level.WARNING)
    options[active_value_index] = "[valt] " + options[active_value_index]
    decision = mc.ShowDialogSelect("Begränsa bandbredd", options)

    if decision == -1:
        BPLog("Bitrate limit dialog cancelled")
        return

    chosen_limit = option_values[decision]
    set_bitrate_limit(chosen_limit)
    BPLog("Bitrate limit set to %d kbps (%s)" %(chosen_limit, options[decision]))

def get_use_pirateplay():
    return conf().GetValue(USE_PIRATEPLAY_KEY) == "True"

def set_use_pirateplay(use_pirateplay):
    conf().SetValue(USE_PIRATEPLAY_KEY, str(use_pirateplay))

def get_bitrate_limit():
    limit = conf().GetValue(BITRATE_LIMIT_KEY)
    if limit == "": return -1
    else: return int(limit)

def set_bitrate_limit(limit):
    conf().SetValue(BITRATE_LIMIT_KEY, str(limit))

def get_option_stream_source():
    opt = "Uppspelningskälla: "
    if get_use_pirateplay():
        opt += "Pirateplay"
    else:
        opt += "Web"
    return opt

def get_option_bitrate_limit():
    opt = "Bandbreddsbegränsning: "
    limit = get_bitrate_limit()
    if limit == -1:
        opt += "Obegränsat"
    else:
        opt += "%d kbps" %limit
    return opt
