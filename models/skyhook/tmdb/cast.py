from dataclasses import dataclass
from typing import List, Any

from models.skyhook.tmdb.image import Image
from utils import TMDB_IMAGE_BASE_URL


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