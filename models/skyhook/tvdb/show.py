from datetime import datetime
from typing import List
from typing import Any
from dataclasses import dataclass

from env import LANGS_FALLBACK

CONTENT_RATING_ORDER = ['fra', 'usa']

COVER_TYPES = [
    {'name': 'Banner', 'id': 1, 'includeText': None},
    {'name': 'Poster', 'id': 2, 'includeText': True},
    {'name': 'Poster', 'id': 7, 'includeText': True}, # Season Poster
    {'name': 'Fanart', 'id': 3, 'includeText': None},
    {'name': 'Clearlogo', 'id': 23, 'includeText': None}
]

@dataclass
class TimeOfDay:
    hours: int
    minutes: int

    @staticmethod
    def from_dict(obj: Any) -> 'TimeOfDay':
        _hours = int(obj.get("hours"))
        _minutes = int(obj.get("minutes"))
        return TimeOfDay(_hours, _minutes)

    @staticmethod
    def from_string(time_str: str) -> 'TimeOfDay':
        if not time_str:
            return None

        """Convert a time string in HH:MM format to a TimeOfDay instance."""
        hours, minutes = map(int, time_str.split(':'))
        return TimeOfDay(hours, minutes)


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
    absoluteEpisodeNumber: int | None
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
        _absoluteEpisodeNumber = int(obj.get("absoluteEpisodeNumber"))
        _airedBeforeSeasonNumber = int(obj.get("airedBeforeSeasonNumber"))
        _airedBeforeEpisodeNumber = int(obj.get("airedBeforeEpisodeNumber"))
        _title = str(obj.get("title"))
        _airDate = str(obj.get("airDate"))
        _airDateUtc = str(obj.get("airDateUtc"))
        _runtime = int(obj.get("runtime"))
        _overview = str(obj.get("overview"))
        _image = str(obj.get("image"))
        return Episode(_tvdbShowId, _tvdbId, _seasonNumber, _episodeNumber, _absoluteEpisodeNumber, _airedBeforeSeasonNumber, _airedBeforeEpisodeNumber, _title, _airDate, _airDateUtc, _runtime, _overview, _image)

    @staticmethod
    def from_tvdb_obj(tvdb_obj: dict) -> 'Episode':

        image_link = tvdb_obj.get('image', '')

        if image_link and not image_link.startswith('http') and len(image_link) > 0:
            image_link = 'https://artworks.thetvdb.com' + image_link

        absolute_episode_number = tvdb_obj.get('absoluteNumber', None)

        if absolute_episode_number == 0:
            absolute_episode_number = None

        return Episode(
            tvdb_obj.get('seriesId'),
            tvdb_obj.get('id'),
            tvdb_obj.get('seasonNumber', 0),
            tvdb_obj.get('number', 0),
            absolute_episode_number,
            tvdb_obj.get('airsBeforeSeason', 0),
            tvdb_obj.get('airsBeforeEpisode', 0),
            tvdb_obj.get('name', ''),
            tvdb_obj.get('aired', ''),
            datetime.strptime(tvdb_obj.get('aired', ''), '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ') if tvdb_obj.get('aired') else '',
            tvdb_obj.get('runtime', 0),
            tvdb_obj.get('overview', ''),
            image_link
        )

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
    alternativeTitles: List[dict]
    actors: List[Actor]
    images: List[Image]
    seasons: List[Season]
    episodes: List[Episode]

    @staticmethod
    def from_dict(obj: Any) -> 'Show':
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

    @staticmethod
    def from_tvdb_obj(tvdb_obj: dict) -> 'Show':

        lang_fallback_index = -1

        # Extract the name from translations if available
        translations = tvdb_obj.get('translations', {})
        name_translations = translations.get('nameTranslations') or []

        name = ""

        for index, lang in enumerate(LANGS_FALLBACK):
            for translation in name_translations:
                if translation.get('language') == lang.pt2t and not (translation.get('isAlias') or False):
                    name = translation.get('name')
                    break

            if name != "":
                lang_fallback_index = index
                break

        if name == "":
            name = tvdb_obj.get('name')

        alternative_titles = []

        for index, lang in enumerate(LANGS_FALLBACK):
            for translation in name_translations:
                if translation.get('language') == lang.pt2t and (translation.get('isAlias') or False):
                    alternative_titles.append({"title": translation.get('name')})

        # Extract overview from translations if available
        overview_translations = translations.get('overviewTranslations') or []

        overview = ""

        for lang in LANGS_FALLBACK:
            for translation in overview_translations:
                if translation.get('language') == lang.pt2t:
                    overview = translation.get('overview')
                    break
            if overview != "":
                break

        if overview == "":
            overview = tvdb_obj.get('overview', "")

        # get tvmaze id from remote_ids
        tvmaze_id = None
        remote_ids = tvdb_obj.get('remoteIds', [])

        if isinstance(remote_ids, list):
            tvmaze_id = next((item.get('id') for item in remote_ids if item.get('type') == 19), None)
            if tvmaze_id is not None:
                tvmaze_id = int(tvmaze_id)

        # get tmdb id from remote_ids
        tmdb_id = None

        if isinstance(remote_ids, list):
            tmdb_id = next((item.get('id') for item in remote_ids if item.get('type') == 12), None)
            if tmdb_id is not None:
                tmdb_id = int(tmdb_id)

        # get imdb id from remote_ids
        imdb_id = None

        if isinstance(remote_ids, list):
            imdb_id = next((item.get('id') for item in remote_ids if item.get('type') == 2), None)

        # get my animelist id from remote_ids
        # todo: implement my animelist id extraction
        mal_ids = []

        # get aniList id from remote_ids
        # todo: implement aniList id extraction
        ani_list_ids = []

        # get original network name
        original_network = tvdb_obj.get('originalNetwork', {}).get('name', 'Unknown')

        # get network name
        network = tvdb_obj.get('latestNetwork', {}).get('name', 'Unknown')

        # get genres name from genres list
        genres = [genre.get('name') for genre in tvdb_obj.get('genres', [])]
        genres.sort()

        # get content rating from contentRatings (fra or usa)
        content_ratings = tvdb_obj.get('contentRatings', [])
        content_rating = "Unknown"

        for rating in CONTENT_RATING_ORDER:
            for content_rating_obj in content_ratings:
                if content_rating_obj.get('country') == rating:
                    content_rating = content_rating_obj.get('name', 'Unknown')
                    break
            if content_rating != "Unknown":
                break


        # get actors from characters list
        actors = []

        for character in filter(lambda x: x.get('peopleType') == 'Actor', tvdb_obj.get('characters', [])):
            actors.append(Actor(
                name=character.get('personName'),
                character=character.get('name'),
                image=character.get('personImgURL')
            ))

        # get images from artworks
        images = []
        artworks = tvdb_obj.get('artworks')

        # sort artworks by id reversing the order
        artworks.sort(key=lambda x: x.get('id', 0), reverse=True)

        for cover_type in COVER_TYPES:
            artwork = None

            for art_obj in artworks:
                if art_obj.get('type') != cover_type.get('id'):
                    continue

                if cover_type.get('includeText') is True and (not map(lambda x: x.pt2t, LANGS_FALLBACK).__contains__(art_obj.get('language'))):
                    continue

                if cover_type.get('includeText') is None or cover_type.get('includeText') == art_obj.get('includesText'):
                    artwork = art_obj
                    break

            if artwork is None and cover_type.get('id') == 2:
                # if no poster found, use the first available image as a fallback for poster
                artwork = next((art for art in artworks if art.get('type') == cover_type.get('id')), None)

            if artwork:
                images.append(Image(
                    coverType=cover_type.get('name'),
                    url=artwork.get('image')
                ))

        # get seasons from seasons list
        seasons = []

        for season in filter(lambda x: x.get('type', {}).get('type') == 'official', tvdb_obj.get('seasons', [])):
            season_artworks = list(filter(lambda x: int(x.get('seasonId', 0)) == int(season.get('id')), artworks))

            season_images = []

            for cover_type in COVER_TYPES:
                season_artwork = None

                for art_obj in season_artworks:
                    if art_obj.get('type') == cover_type.get('id'):
                        season_artwork = art_obj
                        break

                if season_artwork:
                    season_images.append(Image(
                        coverType=cover_type.get('name'),
                        url=season_artwork.get('image')
                    ))

            seasons.append(Season(
                seasonNumber=season.get('number', 0),
                images=season_images
            ))

        # episodes not included in the Show object as per the original code
        # return empty list for episodes and handle it separately if needed
        episodes = []

        # get date string and set to None if empty
        first_aired = tvdb_obj.get('firstAired', "")
        if first_aired == "":
            first_aired = None

        last_aired = tvdb_obj.get('lastAired', "")
        if last_aired == "":
            last_aired = None

        return Show(
            tvdb_obj.get('id'),
            name,
            overview,
            tvdb_obj.get('slug'),
            tvdb_obj.get('originalCountry'),
            tvdb_obj.get('originalLanguage'),
            LANGS_FALLBACK[lang_fallback_index].pt2t if lang_fallback_index > -1 else tvdb_obj.get('originalLanguage'),
            first_aired,
            last_aired,
            None,  # tvRageId is not available in TVDB API
            tvmaze_id,
            tmdb_id,
            imdb_id,
            mal_ids,
            ani_list_ids,
            datetime.strptime(tvdb_obj.get('lastUpdated'), "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%dT%H:%M:%SZ'),
            tvdb_obj.get('status', {}).get('name', 'Unknown'),
            tvdb_obj.get('averageRuntime', 0),
            TimeOfDay.from_string(tvdb_obj.get('airsTime')),
            original_network,
            network,
            genres,
            content_rating,
            Rating(count=0, value=''),
            alternative_titles,
            actors,
            images,
            seasons,
            episodes
        )