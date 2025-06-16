from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class TimeOfDay:
    hours: int
    minutes: int

    @staticmethod
    def from_dict(obj: Any) -> 'TimeOfDay':
        _hours = int(obj.get("hours"))
        _minutes = int(obj.get("minutes"))
        return TimeOfDay(_hours, _minutes)


@dataclass
class Image:
    coverType: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        _coverType = str(obj.get("coverType"))
        _url = str(obj.get("url"))
        return Image(_coverType, _url)


@dataclass
class Rating:
    count: int
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'Rating':
        _count = int(obj.get("count"))
        _value = str(obj.get("value"))
        return Rating(_count, _value)


@dataclass
class Season:
    seasonNumber: int
    images: List[Image]

    @staticmethod
    def from_dict(obj: Any) -> 'Season':
        _seasonNumber = int(obj.get("seasonNumber"))
        _images = [Image.from_dict(y) for y in obj.get("images")]
        return Season(_seasonNumber, _images)

@dataclass
class Actor:
    name: str
    character: str
    image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Actor':
        _name = str(obj.get("name"))
        _character = str(obj.get("character"))
        _image = str(obj.get("image"))
        return Actor(_name, _character, _image)

@dataclass
class Episode:
    tvdbShowId: int
    tvdbId: int
    seasonNumber: int
    episodeNumber: int
    airedBeforeSeasonNumber: int
    airedBeforeEpisodeNumber: int
    title: str
    airDate: str
    airDateUtc: str
    runtime: int
    overview: str
    image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Episode':
        _tvdbShowId = int(obj.get("tvdbShowId"))
        _tvdbId = int(obj.get("tvdbId"))
        _seasonNumber = int(obj.get("seasonNumber"))
        _episodeNumber = int(obj.get("episodeNumber"))
        _airedBeforeSeasonNumber = int(obj.get("airedBeforeSeasonNumber"))
        _airedBeforeEpisodeNumber = int(obj.get("airedBeforeEpisodeNumber"))
        _title = str(obj.get("title"))
        _airDate = str(obj.get("airDate"))
        _airDateUtc = str(obj.get("airDateUtc"))
        _runtime = int(obj.get("runtime"))
        _overview = str(obj.get("overview"))
        _image = str(obj.get("image"))
        return Episode(_tvdbShowId, _tvdbId, _seasonNumber, _episodeNumber, _airedBeforeSeasonNumber, _airedBeforeEpisodeNumber, _title, _airDate, _airDateUtc, _runtime, _overview, _image)

@dataclass
class Show:
    tvdbId: int
    title: str
    overview: str
    slug: str
    originalCountry: str
    originalLanguage: str
    language: str
    firstAired: str
    lastAired: str
    tvRageId: int
    tvMazeId: int
    tmdbId: int
    imdbId: str
    malIds: List[object]
    aniListIds: List[object]
    lastUpdated: str
    status: str
    runtime: int
    timeOfDay: TimeOfDay
    originalNetwork: str
    network: str
    genres: List[str]
    contentRating: str
    rating: Rating
    actors: List[Actor]
    images: List[Image]
    seasons: List[Season]
    episodes: List[Episode]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _tvdbId = int(obj.get("tvdbId"))
        _title = str(obj.get("title"))
        _overview = str(obj.get("overview"))
        _slug = str(obj.get("slug"))
        _originalCountry = str(obj.get("originalCountry"))
        _originalLanguage = str(obj.get("originalLanguage"))
        _language = str(obj.get("language"))
        _firstAired = str(obj.get("firstAired"))
        _lastAired = str(obj.get("lastAired"))
        _tvRageId = int(obj.get("tvRageId"))
        _tvMazeId = int(obj.get("tvMazeId"))
        _tmdbId = int(obj.get("tmdbId"))
        _imdbId = str(obj.get("imdbId"))
        _malIds = obj.get("malIds")
        _aniListIds = obj.get("aniListIds")
        _lastUpdated = str(obj.get("lastUpdated"))
        _status = str(obj.get("status"))
        _runtime = int(obj.get("runtime"))
        _timeOfDay = TimeOfDay.from_dict(obj.get("timeOfDay"))
        _originalNetwork = str(obj.get("originalNetwork"))
        _network = str(obj.get("network"))
        _genres = obj.get("genres")
        _contentRating = str(obj.get("contentRating"))
        _rating = Rating.from_dict(obj.get("rating"))
        _actors = [Actor.from_dict(y) for y in obj.get("actors")]
        _images = [Image.from_dict(y) for y in obj.get("images")]
        _seasons = [Season.from_dict(y) for y in obj.get("seasons")]
        _episodes = [Episode.from_dict(y) for y in obj.get("episodes")]
        return Show(_tvdbId, _title, _overview, _slug, _originalCountry, _originalLanguage, _language, _firstAired, _lastAired, _tvRageId, _tvMazeId, _tmdbId, _imdbId, _malIds, _aniListIds, _lastUpdated, _status, _runtime, _timeOfDay, _originalNetwork, _network, _genres, _contentRating, _rating, _actors, _images, _seasons, _episodes)


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
