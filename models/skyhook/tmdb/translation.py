from dataclasses import dataclass
from typing import Any


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