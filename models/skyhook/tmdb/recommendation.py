from dataclasses import dataclass
from typing import Any


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