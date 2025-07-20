import musicbrainzngs
from fastapi import APIRouter

from env import MUSICBRAINZ_API_DOMAIN, MUSICBRAINZ_API_APP_NAME, MUSICBRAINZ_API_VERSION, MUSICBRAINZ_API_CONTACT
from routers.v0_4.musicbrainz.albums import albumsRouter

musicrainzsRouter = APIRouter()

musicrainzsRouter.include_router(router=albumsRouter)
musicbrainzngs.set_hostname(MUSICBRAINZ_API_DOMAIN, use_https=True)
musicbrainzngs.set_useragent(MUSICBRAINZ_API_APP_NAME, MUSICBRAINZ_API_VERSION, MUSICBRAINZ_API_CONTACT)


musicbrainzngs.set_rate_limit(limit_or_interval=1.5, new_requests=1)