from fastapi import APIRouter

from env import ArrServer

v1Router = APIRouter(prefix="/v1")

@v1Router.get("/")
async def root():
    return {"message": "Welcome to the v1 API"}

if ArrServer.is_activated(ArrServer.SONARR):
    from routers.v1.tvdb import tvdbRouter

    v1Router.include_router(router=tvdbRouter)

    print("Sonarr metadata server is activated.")