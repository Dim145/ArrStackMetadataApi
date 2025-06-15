from fastapi import APIRouter

from routers.v1.tvdb import tvdbRouter

v1Router = APIRouter(prefix="/v1")

@v1Router.get("/")
async def root():
    return {"message": "Welcome to the v1 API"}

v1Router.include_router(router=tvdbRouter)