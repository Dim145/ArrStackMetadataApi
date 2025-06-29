from dataclasses import dataclass
from typing import Any


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