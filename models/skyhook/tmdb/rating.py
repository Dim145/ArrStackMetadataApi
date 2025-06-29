from dataclasses import dataclass
from typing import Any


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