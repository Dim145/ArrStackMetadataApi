from fastapi import APIRouter

from routers.v1 import v1Router

routers = APIRouter()

routers.include_router(v1Router)