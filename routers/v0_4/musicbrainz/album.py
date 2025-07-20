import json

import musicbrainzngs
from fastapi import APIRouter
from musicbrainzngs import RELATION_INCLUDES, TAG_INCLUDES

from env import MUSICBRAINZ_API_CONTACT, MUSICBRAINZ_API_VERSION, MUSICBRAINZ_API_APP_NAME, MUSICBRAINZ_API_DOMAIN
from models.skyhook.musicbrainz.album_resource import AlbumResource
from utils import CACHE_MUSICBRAINZ_ALBUM_PREFIX, cache_or_exec, CACHE_IMAGES_SUFFIX, exec_and_wait, \
    CACHE_MUSICBRAINZ_RELEASE_PREFIX

albumsRouter = APIRouter(prefix="/album")

@albumsRouter.get("/{album_id}")
async def get_albums(album_id: str):

    cache_id = CACHE_MUSICBRAINZ_ALBUM_PREFIX + album_id
    data = cache_or_exec(cache_id, lambda: exec_and_wait(lambda: musicbrainzngs.get_release_group_by_id(album_id, includes=[
        "artists", "releases", "discids", "media", "ratings",
        "artist-credits", "annotation", "aliases", "tags"
    ] + RELATION_INCLUDES), 1))

    cache_id = cache_id + CACHE_IMAGES_SUFFIX
    images = cache_or_exec(cache_id, lambda: musicbrainzngs.get_release_group_image_list(album_id))

    release_group = data.get('release-group')

    release_group['images'] = images.get('images')

    # because of rate limiting, we need to fetch releases separately
    for i in range(release_group['release-count']):
        rid = release_group["release-list"][i].get('id')
        cache_id = CACHE_MUSICBRAINZ_RELEASE_PREFIX + rid
        release_data = cache_or_exec(cache_id, lambda: exec_and_wait( lambda: musicbrainzngs.get_release_by_id(rid, includes=[
             "artists", "labels", "recordings", "aliases",
             "tags", "media", "annotation",
             "artist-credits", "discids", "isrcs",
             "recording-level-rels", "work-level-rels"
         ] + RELATION_INCLUDES), 1))

        release_group["release-list"][i] = release_data.get('release')


    return AlbumResource.from_musicbrainz(release_group)