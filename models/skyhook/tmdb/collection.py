from dataclasses import dataclass
from typing import List, Any

from models.skyhook.tmdb.image import Image
from models.skyhook.tmdb.translation import Translation


@dataclass
class Collection:
    TmdbId: int
    Name: str
    Overview: str
    Images: List[Image]
    Translations: List[Translation]
    Parts: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        _TmdbId = int(obj.get("TmdbId"))
        _Name = str(obj.get("Name"))
        _Overview = str(obj.get("Overview"))
        _Images = [Image.from_dict(y) for y in obj.get("Images")]
        _Translations = [Translation.from_dict(y) for y in obj.get("Translations")]
        _Parts = obj.get("Parts")
        return Collection(_TmdbId, _Name, _Overview, _Images, _Translations, _Parts)