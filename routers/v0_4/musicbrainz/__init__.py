import musicbrainzngs
from fastapi import APIRouter

from routers.v0_4.musicbrainz.albums import albumsRouter

musicrainzsRouter = APIRouter()

musicrainzsRouter.include_router(router=albumsRouter)

musicbrainzngs.set_rate_limit(limit_or_interval=1.5, new_requests=1)