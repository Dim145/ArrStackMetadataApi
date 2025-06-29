from dataclasses import dataclass
from typing import Any


@dataclass
class Trakt:
    Count: int
    Value: float
    Type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Trakt':
        _Count = int(obj.get("Count"))
        _Value = float(obj.get("Value"))
        _Type = str(obj.get("Type"))
        return Trakt(_Count, _Value, _Type)