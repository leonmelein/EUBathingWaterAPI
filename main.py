import os
from databases import Database

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json
import uvicorn

origins = ["*"]

version = os.getenv("version") if os.getenv("version") else "1.0"
app = FastAPI(
    title="Zwemwater API",
    description="Toegang tot de actuele metingen van zwemplekken in Nederland",
    version= version
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database('sqlite+aiosqlite:///data/dataset.sqlite3')

@app.on_event("startup")
async def on_boot():
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

@app.get("/", summary="Get all Locations", description="Get all locations", tags=["GetLocations"])
async def main():
    with open("locs.geojson", "r") as input:
        data = json.load(input)
    
    return data

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
