from fastapi import APIRouter

from routers.v0_4 import v0_4Router
from routers.v1 import v1Router

routers = APIRouter()

routers.include_router(v1Router)
routers.include_router(v0_4Router)