from dataclasses import dataclass
from typing import Any

from models.skyhook.tmdb.ratings.tmdb import Tmdb
from models.skyhook.tmdb.ratings.trakt import Trakt


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