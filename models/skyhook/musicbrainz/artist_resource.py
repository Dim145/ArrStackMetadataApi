from dataclasses import dataclass, field
from typing import List, Optional

from models.skyhook.musicbrainz.image_resource import ImageResource
from models.skyhook.musicbrainz.link_resource import LinkResource
from models.skyhook.musicbrainz.rating_resource import RatingResource

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.skyhook.musicbrainz.album_resource import AlbumResource

@dataclass
class ArtistResource:
    Albums: List['AlbumResource'] = field(default_factory=list)
    Genres: List[str] = field(default_factory=list)
    ArtistName: Optional[str] = None
    AristUrl: Optional[str] = None
    Overview: Optional[str] = None
    Type: Optional[str] = None
    Disambiguation: Optional[str] = None
    Id: Optional[str] = None
    OldIds: Optional[List[str]] = None
    Images: Optional[List[ImageResource]] = None
    Links: Optional[List[LinkResource]] = None
    ArtistAliases: Optional[List[str]] = None
    Status: Optional[str] = None
    Rating: Optional[RatingResource] = None

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'ArtistResource':

        artist_dict = obj.get('artist', {})

        return ArtistResource(
            Id=obj.get('target'),
            ArtistName=artist_dict.get('name'),
            Type=artist_dict.get('type'),
            Disambiguation=artist_dict.get('disambiguation'),
        )