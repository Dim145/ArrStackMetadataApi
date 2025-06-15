from fastapi import FastAPI

from env import TVDB_API_KEY, METADATA_SERVER_FOR
from routers import routers

app = FastAPI()

@app.get("/")
async def root():
    return f"Running metadata server for {METADATA_SERVER_FOR}"

app.include_router(routers)