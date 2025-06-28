from typing import List
from typing import Any
from dataclasses import dataclass

from tmdbsimple import Movies
from env import LANGS_FALLBACK
from utils import TMDB_IMAGE_BASE_URL


class TmdbReleaseDateTypes:
    Premiere = 1
    TheatricalLimited = 2
    Theatrical = 3
    Digital = 4
    Physical = 5
    TV = 6

@dataclass
class Tmdb:
    Count: int
    Value: float
    Type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tmdb':
        _Count = int(obj.get("Count"))
        _Value = float(obj.get("Value"))
        _Type = str(obj.get("Type"))
        return Tmdb(_Count, _Value, _Type)

@dataclass
class Trakt:
    Count: int
    Value: float
    Type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Trakt':
        _Count = int(obj.get("Count"))
        _Value = float(obj.get("Value"))
        _Type = str(obj.get("Type"))
        return Trakt(_Count, _Value, _Type)


class TmdbRealeaseDateTypes:
    Premiere = 1
    Theatrical_limited = 2
    Theatrical = 3
    Digital = 4
    Physical = 5
    TV = 6


@dataclass
class Translation:
    Title: str
    Overview: str
    Language: str

    @staticmethod
    def from_dict(obj: Any) -> 'Translation':
        _Title = str(obj.get("Title"))
        _Overview = str(obj.get("Overview"))
        _Language = str(obj.get("Language"))
        return Translation(_Title, _Overview, _Language)

    @staticmethod
    def from_tmdb_obj(obj: Any) -> 'Translation':
        return Translation(
            obj.get("data").get("title"),
            obj.get("data").get("overview"),
            obj.get("iso_639_1") + "-" + obj.get("iso_3166_1")
        )

@dataclass
class Image:
    CoverType: str
    Url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        _CoverType = str(obj.get("CoverType"))
        _Url = str(obj.get("Url"))
        return Image(_CoverType, _Url)

@dataclass
class AlternativeTitle:
    Title: str
    Type: str
    Language: str

    @staticmethod
    def from_dict(obj: Any) -> 'AlternativeTitle':
        _Title = str(obj.get("Title"))
        _Type = str(obj.get("Type"))
        _Language = str(obj.get("Language"))
        return AlternativeTitle(_Title, _Type, _Language)

    @staticmethod
    def from_tmdb_obj(obj: Any) -> 'AlternativeTitle':
        return AlternativeTitle(
            obj.get("title"),
            obj.get("type"),
            obj.get("iso_3166_1")
        )

@dataclass
class Cast:
    Name: str
    Order: int
    Character: str
    TmdbId: int
    CreditId: str
    Images: List[Image]

    @staticmethod
    def from_dict(obj: Any) -> 'Cast':
        _Name = str(obj.get("Name"))
        _Order = int(obj.get("Order"))
        _Character = str(obj.get("Character"))
        _TmdbId = int(obj.get("TmdbId"))
        _CreditId = str(obj.get("CreditId"))
        _Images = [Image.from_dict(y) for y in obj.get("Images")]
        return Cast(_Name, _Order, _Character, _TmdbId, _CreditId, _Images)


    @staticmethod
    def from_tmdb_obj(obj: Any) -> 'Cast':
        return Cast(
            obj.get("name"),
            obj.get("order"),
            obj.get("character"),
            obj.get("id"),
            obj.get("credit_id"),
            [Image(
                "Headshot",
                TMDB_IMAGE_BASE_URL + obj.get("profile_path", "") if obj.get("profile_path") else None
            )]
        )

@dataclass
class Certification:
    Country: str
    Certification: str

    @staticmethod
    def from_dict(obj: Any) -> 'Certification':
        _Country = str(obj.get("Country"))
        _Certification = str(obj.get("Certification"))
        return Certification(_Country, _Certification)

@dataclass
class Crew:
    Name: str
    Order: int
    Job: str
    Department: str
    TmdbId: int
    CreditId: str
    Images: List[Image]

    @staticmethod
    def from_dict(obj: Any) -> 'Crew':
        _Name = str(obj.get("Name"))
        _Order = int(obj.get("Order"))
        _Job = str(obj.get("Job"))
        _Department = str(obj.get("Department"))
        _TmdbId = int(obj.get("TmdbId"))
        _CreditId = str(obj.get("CreditId"))
        _Images = [Image.from_dict(y) for y in obj.get("Images")]
        return Crew(_Name, _Order, _Job, _Department, _TmdbId, _CreditId, _Images)

    @staticmethod
    def from_tmdb_obj(obj: Any, order: int) -> 'Crew':
        return Crew(
            obj.get("name"),
            order,
            obj.get("job"),
            obj.get("department"),
            obj.get("id"),
            obj.get("credit_id"),
            [Image(
                "Headshot",
                TMDB_IMAGE_BASE_URL + obj.get("profile_path", "") if obj.get("profile_path") else None
            )]
        )

@dataclass
class Credits:
    Cast: List[Cast]
    Crew: List[Crew]

    @staticmethod
    def from_dict(obj: Any) -> 'Credits':
        _Cast = [Cast.from_dict(y) for y in obj.get("Cast")]
        _Crew = [Crew.from_dict(y) for y in obj.get("Crew")]
        return Credits(_Cast, _Crew)

@dataclass
class MovieRatings:
    Tmdb: Tmdb
    Imdb: str
    Metacritic: str
    RottenTomatoes: str
    Trakt: Trakt

    @staticmethod
    def from_dict(obj: Any) -> 'MovieRatings':
        _Tmdb = Tmdb.from_dict(obj.get("Tmdb"))
        _Imdb = str(obj.get("Imdb"))
        _Metacritic = str(obj.get("Metacritic"))
        _RottenTomatoes = str(obj.get("RottenTomatoes"))
        _Trakt = Trakt.from_dict(obj.get("Trakt"))
        return MovieRatings(_Tmdb, _Imdb, _Metacritic, _RottenTomatoes, _Trakt)

@dataclass
class Rating:
    Count: int
    Value: float
    Origin: str
    Type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Rating':
        _Count = int(obj.get("Count"))
        _Value = float(obj.get("Value"))
        _Origin = str(obj.get("Origin"))
        _Type = str(obj.get("Type"))
        return Rating(_Count, _Value, _Origin, _Type)

@dataclass
class Recommendation:
    TmdbId: int
    Title: str

    @staticmethod
    def from_dict(obj: Any) -> 'Recommendation':
        _TmdbId = int(obj.get("TmdbId"))
        _Title = str(obj.get("Title"))
        return Recommendation(_TmdbId, _Title)

    @staticmethod
    def from_tmdb_obj(obj: Any) -> 'Recommendation':
        return Recommendation(
            obj.get("id"),
            obj.get("title")
        )

@dataclass
class Movie:
    TmdbId: int
    ImdbId: str
    Title: str
    Overview: str
    OriginalTitle: str
    OriginalLanguage: str
    TitleSlug: str
    Runtime: int
    Popularity: float
    Year: int
    Premier: str
    InCinema: str
    PhysicalRelease: str
    DigitalRelease: str
    Images: List[Image]
    Ratings: List[Rating]
    MovieRatings: MovieRatings
    Genres: List[str]
    Keywords: List[str]
    AlternativeTitles: List[AlternativeTitle]
    Translations: List[Translation]
    Recommendations: List[Recommendation]
    Credits: Credits
    Studio: str
    YoutubeTrailerId: str
    Certifications: List[Certification]
    Status: str
    Collection: str
    Homepage: str

    @staticmethod
    def from_dict(obj: Any) -> 'Movie':
        _TmdbId = int(obj.get("TmdbId"))
        _ImdbId = str(obj.get("ImdbId"))
        _Title = str(obj.get("Title"))
        _Overview = str(obj.get("Overview"))
        _OriginalTitle = str(obj.get("OriginalTitle"))
        _OriginalLanguage = str(obj.get("OriginalLanguage"))
        _TitleSlug = str(obj.get("TitleSlug"))
        _Runtime = int(obj.get("Runtime"))
        _Popularity = float(obj.get("Popularity"))
        _Year = int(obj.get("Year"))
        _Premier = str(obj.get("Premier"))
        _InCinema = str(obj.get("InCinema"))
        _PhysicalRelease = str(obj.get("PhysicalRelease"))
        _DigitalRelease = str(obj.get("DigitalRelease"))
        _Images = [Image.from_dict(y) for y in obj.get("Images")]
        _Ratings = [Rating.from_dict(y) for y in obj.get("Ratings")]
        _MovieRatings = MovieRatings.from_dict(obj.get("MovieRatings"))
        _Genres = [y for y in obj.get("Genres")]
        _Keywords = [y for y in obj.get("Keywords")]
        _AlternativeTitles = [AlternativeTitle.from_dict(y) for y in obj.get("AlternativeTitles")]
        _Translations = [Translation.from_dict(y) for y in obj.get("Translations")]
        _Recommendations = [Recommendation.from_dict(y) for y in obj.get("Recommendations")]
        _Credits = Credits.from_dict(obj.get("Credits"))
        _Studio = str(obj.get("Studio"))
        _YoutubeTrailerId = str(obj.get("YoutubeTrailerId"))
        _Certifications = [Certification.from_dict(y) for y in obj.get("Certifications")]
        _Status = str(obj.get("Status"))
        _Collection = str(obj.get("Collection"))
        _Homepage = str(obj.get("Homepage"))
        return Movie(_TmdbId, _ImdbId, _Title, _Overview, _OriginalTitle, _OriginalLanguage, _TitleSlug, _Runtime, _Popularity, _Year, _Premier, _InCinema, _PhysicalRelease, _DigitalRelease, _Images, _Ratings, _MovieRatings, _Genres, _Keywords, _AlternativeTitles, _Translations, _Recommendations, _Credits, _Studio, _YoutubeTrailerId, _Certifications, _Status, _Collection, _Homepage)

    @staticmethod
    def from_tmdb_obj(obj: Movies) -> 'Movie':

        # get the release dates
        premier = None
        in_cinema = None
        physical = None
        digital = None

        for lang in LANGS_FALLBACK:
            for release_date in obj.release_dates_by_country:
                if release_date.get("iso_3166_1") == lang.pt1.upper():
                    for date in release_date.get("release_dates", []):
                        if date.get("type") == TmdbReleaseDateTypes.Premiere:
                            premier = date.get("release_date", "")
                        if date.get("type") == TmdbReleaseDateTypes.Theatrical:
                            in_cinema = date.get("release_date", "")
                        if date.get("type") == TmdbReleaseDateTypes.Physical:
                            physical = date.get("release_date", "")
                        if date.get("type") == TmdbReleaseDateTypes.Digital:
                            digital = date.get("release_date", "")

        # get images
        images = []

        # add poster images
        if hasattr(obj, 'posters') and obj.posters:
            # get a poster with a filter
            posters = sorted(obj.posters, key=lambda x: x.get('vote_count', 0), reverse=True)

            images.append(Image(
                "Poster",
                TMDB_IMAGE_BASE_URL + posters[0].get("file_path"),
            ))

        if hasattr(obj, 'logos') and obj.logos:
            # get a logo with a filter
            logos = sorted(obj.logos, key=lambda x: x.get('vote_count', 0), reverse=True)

            images.append(Image(
                "Clearlogo",
                TMDB_IMAGE_BASE_URL + logos[0].get("file_path"),
            ))

        if hasattr(obj, 'backdrops') and obj.backdrops:
            # get a backdrop with a filter
            backdrops = sorted(obj.backdrops, key=lambda x: x.get('vote_count', 0), reverse=True)

            images.append(Image(
                "Banner",
                TMDB_IMAGE_BASE_URL + backdrops[0].get("file_path"),
            ))

        ratings = []

        ratings.append(Rating(
            obj.vote_count,
            obj.vote_average,
            "Tmdb",
            "User"
        ))

        # get movie ratings
        # todo : get ratings from other sources if available
        movie_ratings = MovieRatings(
            Tmdb(obj.vote_count, obj.vote_average, "User"),
            None,
            None,
            None,
            None
        )

        # build crédit object
        credit = Credits(
            [Cast.from_tmdb_obj(cast) for cast in obj.cast] if hasattr(obj, 'cast') else [],
            [Crew.from_tmdb_obj(crew, ind) for ind, crew in enumerate(obj.crew)] if hasattr(obj, 'crew') else []
        )

        # extract youtube trailer from videos if available
        youtube_trailer_id = ""

        if obj.videos:
            for video in list(obj.videos):
                if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                    youtube_trailer_id = video.get("key")
                    break

        return Movie(
            obj.id,
            obj.imdb_id,
            obj.title,
            obj.overview,
            obj.original_title,
            obj.original_language,
            str(obj.id), # use id as slug
            obj.runtime,
            obj.popularity,
            int(obj.release_date.split("-")[0]) if obj.release_date else 0,  # Year
            premier,
            in_cinema,
            physical,
            digital,
            images,
            ratings,
            movie_ratings,
            [genre.get("name") for genre in obj.genres] if hasattr(obj, 'genres') else [],
            [keyword.get("name") for keyword in obj.keywords] if hasattr(obj, 'keywords') else [],
            [AlternativeTitle.from_tmdb_obj(title) for title in obj.alternative_titles] if hasattr(obj, 'alternative_titles') else [],
            [Translation.from_tmdb_obj(translation) for translation in obj.translations] if hasattr(obj, 'translations') else [],
            [Recommendation.from_tmdb_obj(rec) for rec in obj.recommendations] if hasattr(obj, 'recommendations') else [],
            credit,
            obj.production_companies[0].get("name") if hasattr(obj, 'production_companies') and obj.production_companies and obj.production_companies[0] else "",
            youtube_trailer_id,
            [], # certifications
            obj.status,
            None, # collection
            obj.homepage
        )



