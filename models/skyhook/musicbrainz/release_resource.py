from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from models.skyhook.musicbrainz.medium_resource import MediumResource
from models.skyhook.musicbrainz.track_resource import TrackResource


@dataclass
class ReleaseResource:
    Disambiguation: Optional[str] = None
    Country: Optional[List[str]] = None
    ReleaseDate: Optional[datetime] = None
    Id: Optional[str] = None
    OldIds: Optional[List[str]] = None
    Label: Optional[List[str]] = None
    Media: Optional[List[MediumResource]] = None
    Title: Optional[str] = None
    Status: Optional[str] = None
    TrackCount: int = 0
    Tracks: Optional[List[TrackResource]] = None

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'ReleaseResource':
        return ReleaseResource(
            Id=obj.get('id'),
            Country=obj.get('country'),
            ReleaseDate=datetime.strptime(obj.get('date'), '%Y-%m-%d') if obj.get('date') else None,
            Label=obj.get('label-info', [{}])[0].get('label', {}).get('name') if obj.get('label-info') else None,
            Title=obj.get('title'),
            Status=obj.get('status'),
            Disambiguation=obj.get('disambiguation'),
        )