import mc

def category_to_list_item(item):
    list_item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    return list_item

def show_to_list_item(item):
    list_item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    return list_item

def episode_to_list_item(item):
    list_item = mc.ListItem(mc.ListItem.MEDIA_VIDEO_EPISODE)
    list_item.SetProperty("id", item["id"])
    list_item.SetTitle(item["title"])
    list_item.SetLabel(item["title"])
    list_item.SetPath(item["url"])
    list_item.SetDescription(item["description"], False)
    list_item.SetProperty("date_available_until", item["date_available_until"])
    list_item.SetProperty("date_broadcasted", item["date_broadcasted"])
    date_array = item["date_broadcasted"].split("T")[0].split("-")
    list_item.SetDate(int(date_array[0]),
                      int(date_array[1]),
                      int(date_array[2]))
    list_item.SetProperty("length", item["length"])
    duration_array = item["length"].split()
    duration = sum(map(parse_duration, zip(duration_array[1::2], duration_array[::2])))
    list_item.SetDuration(duration)

    list_item.SetThumbnail(get_image_size(item["thumbnail_url"], "small"))
    list_item.SetIcon(get_image_size(item["thumbnail_url"], "medium"))
    return list_item

def get_image_size(url, size):
    parts = url.split("/")
    if "ALTERNATES" in parts:
        size_position = parts.index("ALTERNATES") + 1
        parts[size_position] = size
    return "/".join(parts)

def parse_duration((identifier, value)):
    if identifier == "h":
        return int(value) * 3600
    if identifier == "min":
        return int(value) * 60
    if identifier == "sek":
        return int(value)

