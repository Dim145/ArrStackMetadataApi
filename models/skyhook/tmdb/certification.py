from dataclasses import dataclass
from typing import Any


@dataclass
class Certification:
    Country: str
    Certification: str

    @staticmethod
    def from_dict(obj: Any) -> 'Certification':
        _Country = str(obj.get("Country"))
        _Certification = str(obj.get("Certification"))
        return Certification(_Country, _Certification)