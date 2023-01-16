import os

from fastapi import FastAPI
import uvicorn

from Models.Response import Response
from Sources.Marineterrein import MarineTerrein
from Sources.ZwemwaterNL import ZwemwaterNL

version = os.getenv("version") if os.getenv("version") else "1.0"
app = FastAPI(
    title="Zwemwater API",
    description="Toegang tot de actuele metingen van zwemplekken in Nederland",
    version= version
)


@app.get("/", summary="Get all Locations", description="Get all locations", tags=["GetLocations"])
async def main():
    data = []
    data.append(MarineTerrein().retrieve())
    data.append(ZwemwaterNL().retrieve(location="6102791"))
    return Response(version, data)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
