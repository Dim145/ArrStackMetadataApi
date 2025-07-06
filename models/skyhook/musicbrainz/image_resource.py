from dataclasses import dataclass
from typing import Optional


@dataclass
class ImageResource:
    CoverType: Optional[str] = None
    Url: Optional[str] = None
    Height: int = 0
    Width: int = 0

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'ImageResource':
        return ImageResource(
            CoverType=obj.get('types', {})[0] if obj.get('types') else None,
            Url=obj.get('image'),
        )