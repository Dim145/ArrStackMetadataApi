from dataclasses import dataclass
from typing import List, Any

from models.skyhook.tmdb.cast import Cast
from models.skyhook.tmdb.crew import Crew


@dataclass
class Credits:
    Cast: List[Cast]
    Crew: List[Crew]

    @staticmethod
    def from_dict(obj: Any) -> 'Credits':
        _Cast = [Cast.from_dict(y) for y in obj.get("Cast")]
        _Crew = [Crew.from_dict(y) for y in obj.get("Crew")]
        return Credits(_Cast, _Crew)