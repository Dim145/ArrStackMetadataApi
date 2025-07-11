import json

import musicbrainzngs
from fastapi import APIRouter
from musicbrainzngs import RELATION_INCLUDES

from models.skyhook.musicbrainz.album_resource import AlbumResource
from utils import CACHE_MUSICBRAINZ_ALBUM_PREFIX, cache_or_exec, CACHE_IMAGES_SUFFIX, exec_and_wait

albumsRouter = APIRouter(prefix="/albums")

@albumsRouter.get("/{album_id}")
async def get_albums(album_id: str):
    musicbrainzngs.set_hostname("beta.musicbrainz.org", use_https=True)
    musicbrainzngs.set_useragent("Application lidarrMetadataProxyServerForDim", "0.4.0","dimitri.bleach@gmail.com")

    cache_id = CACHE_MUSICBRAINZ_ALBUM_PREFIX + album_id
    data = cache_or_exec(cache_id, lambda: exec_and_wait(lambda: musicbrainzngs.get_release_group_by_id(album_id, includes=[
        "artists", "releases", "discids", "media",
        "artist-credits", "annotation", "aliases"
    ] + RELATION_INCLUDES), 1))

    cache_id = cache_id + CACHE_IMAGES_SUFFIX
    images = cache_or_exec(cache_id, lambda: musicbrainzngs.get_release_group_image_list(album_id))

    release_group = data.get('release-group')

    release_group['images'] = images.get('images')

    print(json.dumps(data, indent=2))

    return AlbumResource.from_musicbrainz(release_group)