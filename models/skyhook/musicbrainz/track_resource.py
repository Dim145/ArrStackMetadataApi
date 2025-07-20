from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TrackResource:
    ArtistId: Optional[str] = None
    DurationMs: int = 0
    Id: Optional[str] = None
    OldIds: Optional[List[str]] = None
    RecordingId: Optional[str] = None
    OldRecordingIds: Optional[List[str]] = None
    TrackName: Optional[str] = None
    TrackNumber: Optional[str] = None
    TrackPosition: int = 0
    Explicit: bool = False
    MediumNumber: int = 0

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'TrackResource':
        """
        Creates a TrackResource instance from a MusicBrainz track object.

        Parameters:
        - obj: A dictionary representing the track data from MusicBrainz.

        Returns:
        - An instance of TrackResource populated with the track data.
        """
        recording = obj.get('recording', {})

        return TrackResource(
            Id=obj.get('id'),
            RecordingId=recording.get('id'),
            TrackName=recording.get('title'),
            DurationMs=obj.get('length', 0),
            TrackNumber=obj.get('number'),
            TrackPosition=obj.get('position', 0),
            ArtistId=obj.get('artist-credit', [{}])[0].get('artist', {}).get('id'),
            Explicit=obj.get('is-explicit', False)
        )