from datetime import datetime
from datetime import timedelta

def LogError(msg):
    print str(datetime.now()) + ", " + str(msg)

def ShowDialogNotification(msg, icon):
    print("notification")

def ActivateWindow(nr):
    LogError("Activating window " + str(nr))

class ListItem:
    MEDIA_UNKNOWN = "unknown"
    MEDIA_AUDIO_MUSIC = "audio-music"
    MEDIA_AUDIO_SPEECH = "audio-speech"
    MEDIA_AUDIO_RADIO = "audio-radio"
    MEDIA_AUDIO_OTHER = "audio-other"
    MEDIA_VIDEO_MUSIC_VIDEO = "video-music-video"
    MEDIA_VIDEO_FEATURE_FILM = "video-feature-film"
    MEDIA_VIDEO_TRAILER = "video-trailer"
    MEDIA_VIDEO_EPISODE = "video-episode"
    MEDIA_VIDEO_CLIP = "video-clip"
    MEDIA_VIDEO_OTHER = "video-other"
    MEDIA_PICTURE = "picture"
    MEDIA_FILE = "file"

    def __init__(self, type=MEDIA_UNKNOWN):
        self.type = type
        self.alternative_paths = []
        self.cast = []
        self.properties = {}

    def AddAlternativePathPath(self, label, path, media_type, thumbnail):
        self.alternative_paths.append({ "label" : label,
                                        "path" : path,
                                        "media_type" : media_type,
                                        "thumbnail" : thumbnail })

    def AddCast(self, name):
        self.AddCastAndRole(name, "unknown")

    def AddCastAndRole(self, name, role):
        self.cast.append({ "name" : name, "role" : role})

    def Dump(self):
        LogError(str(self))

    def GetAlbum(self):
        return self.album

    def SetAlbum(self, album):
        self.album = album

    def GetArtist(self):
        return self.artist

    def SetArtist(self, artist):
        self.artist = artist

    def GetAuthor(self):
        return self.author

    def SetAuthor(self, author):
        self.author = author

    def GetCast(self):
        return self.cast

    def GetCastAndRole(self):
        return self.cast

    def GetComment(self):
        return self.comment

    def SetComment(self, comment):
        self.comment = comment

    def GetContentRating(self):
        return self.content_rating

    def SetContentRating(self, content_rating):
        self.content_rating = content_rating

    def GetContentType(self):
        return self.content_type

    def SetContentType(self, content_type):
        self.content_type = content_type

    def GetDate(self):
        return str(self.date)

    def SetDate(self, year, month, day):
        self.date = {"year" : year, "month" : month, "day" : day}

    def GetDescription(self):
        return self.description

    def SetDescription(self, description, isHtml=False):
        self.description = description

    def GetDirector(self):
        return self.director

    def SetDirector(self, director):
        self.director = director

    def GetDuration(self):
        return self.duration

    def GetDurationFormatted(self):
        return str(timedelta(seconds=self.duration))

    def SetDuration(self, duration):
        self.duration = duration

    def GetEpisode(self):
        return self.episode

    def SetEpisode(self, episode):
        self.episode = episode

    def SetExternalItem(self, externalItem):
        self.external_item = externalItem

    def GetGenre(self):
        return self.genre

    def SetGenre(self, genre):
        self.genre = genre

    def GetIcon(self):
        return self.icon

    def SetIcon(self, icon):
        self.icon = icon

    def GetImage(self):
        return self.image

    def SetImage(self, image):
        self.image = image

    def GetKeywords(self):
        return self.keywords

    def SetKeywords(self, keywords):
        self.keywords = keywords

    def GetLabel(self):
        return self.label

    def SetLabel(self, label):
        self.label = label

    def GetMediaType(self):
        return self.type

    def GetPath(self):
        return self.path

    def SetPath(self, path):
        self.path = path

    def GetProperty(self, key):
        return self.properties[key]

    def SetProperty(self, key, value):
        self.properties[key] = value

    def GetProviderSource(self):
        return self.provider_source

    def SetProviderSource(self, provider_source):
        self.provider_source = provider_source

    def GetReportToServer(self):
        return self.report_to_server

    def SetReportToServer(self, report_to_server):
        self.report_to_server = report_to_server

    def GetSeason(self):
        return self.season

    def SetSeason(self, season):
        self.season = season

    def GetSize(self):
        return self.size

    def GetSizeFormatted(self):
        return str(self.size)

    def SetSize(self, size):
        self.size = size

    def GetStarRating(self):
        return self.star_rating

    def SetStarRating(self, star_rating):
        self.star_rating = star_rating

    def GetStudio(self):
        return self.studio

    def SetStudio(self, studio):
        self.studio = studio

    def GetTagLine(self):
        return self.tag_line

    def SetTagLine(self, tag_line):
        self.tag_line = tag_line

    def GetThumbnail(self):
        return self.thumbnail

    def SetThumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def GetTitle(self):
        return self.title

    def SetTitle(self, title):
        self.title = title

    def GetTrackNumber(self):
        return self.track_number

    def SetTrackNumber(self, track_number):
        self.track_number = track_number

    def GetTVShowTitle(self):
        return self.tv_show_title

    def SetTVShowTitle(self, tv_show_title):
        self.tv_show_title = tv_show_title

    def GetViewCount(self):
        return self.view_count

    def GetViewCountFormatted(self):
        return (str(self.view_count))

    def SetViewCount(self, view_count):
        self.view_count = view_count

    def GetWriter(self):
        return self.writer

    def SetWriter(self, writer):
        self.writer = writer

    def GetYear(self):
        return self.year

    def SetYear(self, year):
        self.year = year

    def SetAddToHistory(self, add_to_history):
        self.add_to_history = add_to_history

    def to_object(self):
        result = {}
        if hasattr(self, "type"): result["type"] = self.type
        if self.alternative_paths: result["alternative_paths"] = self.alternative_paths
        if self.cast: result["cast"] = self.cast
        if hasattr(self, "album"): result["album"] = self.album
        if hasattr(self, "artist"): result["artist"] = self.artist
        if hasattr(self, "author"): result["author"] = self.author
        if hasattr(self, "comment"): result["comment"] = self.comment
        if hasattr(self, "content_rating"): result["content_rating"] = self.content_rating
        if hasattr(self, "content_type"): result["content_type"] = self.content_type
        if hasattr(self, "date"): result["date"] = self.date
        if hasattr(self, "description"): result["description"] = self.description
        if hasattr(self, "director"): result["director"] = self.director
        if hasattr(self, "duration"): result["duration"] = self.duration
        if hasattr(self, "episode"): result["episode"] = self.episode
        if hasattr(self, "external_item"): result["external_item"] = self.external_item
        if hasattr(self, "genre"): result["genre"] = self.genre
        if hasattr(self, "icon"): result["icon"] = self.icon
        if hasattr(self, "image"): result["image"] = self.image
        if hasattr(self, "keywords"): result["keywords"] = self.keywords
        if hasattr(self, "label"): result["label"] = self.label
        if hasattr(self, "path"): result["path"] = self.path
        if self.properties: result["properties"] = self.properties
        if hasattr(self, "provider_source"): result["provider_source"] = self.provider_source
        if hasattr(self, "report_to_server"): result["report_to_server"] = self.report_to_server
        if hasattr(self, "season"): result["season"] = self.season
        if hasattr(self, "star_rating"): result["star_rating"] = self.star_rating
        if hasattr(self, "studio"): result["studio"] = self.studio
        if hasattr(self, "tag_line"): result["tag_line"] = self.tag_line
        if hasattr(self, "thumbnail"): result["thumbnail"] = self.thumbnail
        if hasattr(self, "title"): result["title"] = self.title
        if hasattr(self, "track_number"): result["track_number"] = self.track_number
        if hasattr(self, "tv_show_title"): result["tv_show_title"] = self.tv_show_title
        if hasattr(self, "view_count"): result["view_count"] = self.view_count
        if hasattr(self, "writer"): result["writer"] = self.writer
        if hasattr(self, "year"): result["year"] = self.year
        return result

    def __str__(self):
        return str(self.to_object())
