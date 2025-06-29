from dataclasses import dataclass
from typing import List, Any

from models.skyhook.tmdb.image import Image
from utils import TMDB_IMAGE_BASE_URL


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