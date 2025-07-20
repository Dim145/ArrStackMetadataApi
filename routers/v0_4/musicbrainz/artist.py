import json

import musicbrainzngs
from fastapi import APIRouter
from musicbrainzngs import RELATION_INCLUDES

from models.skyhook.musicbrainz.artist_resource import ArtistResource
from routers.v0_4.musicbrainz.album import get_albums
from utils import CACHE_MUSICBRAINZ_ARTIST_PREFIX, cache_or_exec, exec_and_wait

artistRouter = APIRouter(prefix="/artist")

@artistRouter.get("/{artist_id}")
async def get_artist(artist_id: str):
    """
    Placeholder for artist retrieval logic.
    This function should be implemented to fetch artist details from MusicBrainz.
    """

    cache_id = CACHE_MUSICBRAINZ_ARTIST_PREFIX + artist_id
    data = cache_or_exec(cache_id, lambda: exec_and_wait(lambda: musicbrainzngs.get_artist_by_id(artist_id, includes=[
     "recordings", "releases", "release-groups",
     "works", "various-artists", "discids", "tags",
     "media", "isrcs", "aliases", "annotation", "ratings"
    ] + RELATION_INCLUDES), seconds=1))

    artist = ArtistResource.from_musicbrainz(data)

    for album in data['artist'].get('release-group-list', []):
        # await because of rate limiting, we need to fetch albums separately
        artist.Albums.append(await get_albums(album.get('id')))


    return artist