from fastapi import APIRouter

from env import ArrServer

v0_4Router = APIRouter(prefix="/api/v0.4")

if ArrServer.is_activated(ArrServer.LIDARR):
    from routers.v0_4.musicbrainz import musicrainzsRouter

    print("Lidarr metadata server is activated.")

    v0_4Router.include_router(router=musicrainzsRouter)