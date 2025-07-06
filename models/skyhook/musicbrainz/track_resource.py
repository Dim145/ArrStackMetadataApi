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