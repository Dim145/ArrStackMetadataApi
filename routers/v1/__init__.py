import requests
from fastapi import APIRouter

from env import ArrServer, TMDB_API_KEY

v1Router = APIRouter(prefix="/v1")

@v1Router.get("/")
async def root():
    return {"message": "Welcome to the v1 API"}

if ArrServer.is_activated(ArrServer.SONARR):
    from routers.v1.tvdb import tvdbRouter

    v1Router.include_router(router=tvdbRouter)

    print("Sonarr metadata server is activated.")

if ArrServer.is_activated(ArrServer.RADARR):
    import tmdbsimple as tmdb_client

    from routers.v1.tmdb import moviesRouter

    tmdb_client.API_KEY = TMDB_API_KEY
    tmdb_client.REQUESTS_SESSION = requests.Session()
    tmdb_client.REQUESTS_SESSION.headers.update({"Authorization": "Bearer " + TMDB_API_KEY})

    v1Router.include_router(router=moviesRouter)

    print("Radarr metadata server is activated.")