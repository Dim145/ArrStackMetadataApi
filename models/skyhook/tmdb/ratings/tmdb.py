from dataclasses import dataclass
from typing import Any


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