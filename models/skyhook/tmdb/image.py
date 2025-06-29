from dataclasses import dataclass
from typing import Any


@dataclass
class Image:
    CoverType: str
    Url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        _CoverType = str(obj.get("CoverType"))
        _Url = str(obj.get("Url"))
        return Image(_CoverType, _Url)