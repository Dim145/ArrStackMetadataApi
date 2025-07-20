from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Any

from models.skyhook.musicbrainz.artist_resource import ArtistResource
from models.skyhook.musicbrainz.image_resource import ImageResource
from models.skyhook.musicbrainz.link_resource import LinkResource
from models.skyhook.musicbrainz.rating_resource import RatingResource
from models.skyhook.musicbrainz.release_resource import ReleaseResource


@dataclass
class AlbumResource:
    ArtistId: Optional[str] = None
    Artists: Optional[List[ArtistResource]] = None
    Disambiguation: Optional[str] = None
    Overview: Optional[str] = None
    Id: Optional[str] = None
    OldIds: Optional[List[str]] = None
    Images: Optional[List[ImageResource]] = None
    Links: Optional[List[LinkResource]] = None
    Genres: Optional[List[str]] = None
    Rating: Optional[RatingResource] = None
    ReleaseDate: Optional[datetime] = None
    Releases: Optional[List[ReleaseResource]] = None
    SecondaryTypes: Optional[List[str]] = None
    Title: Optional[str] = None
    Type: Optional[str] = None
    ReleaseStatuses: Optional[List[str]] = None

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'AlbumResource':

        artists = obj.get('artist-credit', [])
        tags = obj.get('tag-list', [])

        return AlbumResource(
            Id=obj.get('id'),
            ReleaseDate=obj.get('first-release-date'),
            SecondaryTypes=[obj.get('type')],
            Disambiguation=obj.get('disambiguation'),
            Title=obj.get('title'),
            Type=obj.get('primary-type'),
            Rating=RatingResource.from_musicbrainz(obj.get('rating')) if obj.get('rating') else None,
            Links=[LinkResource.from_musicbrainz(link) for link in obj.get('url-relation-list', [])],
            Artists=[ArtistResource.from_musicbrainz(artist) for artist in artists],
            Releases=[ReleaseResource.from_musicbrainz(release) for release in obj.get('release-list', [])],
            Images=[ImageResource.from_musicbrainz(image) for image in obj.get('images', [])],
            Genres= [tag.get('name') for tag in tags],
            ArtistId=artists[0].get('artist', {}).get('id') if len(artists) > 0 else None,

        )