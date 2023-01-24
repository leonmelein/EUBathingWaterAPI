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
    
    data = [
        MarineTerrein().retrieve()           
    ]

    ZwClient = ZwemwaterNL()
    for location in locations:
        print(location)
        try:
            data.append(ZwClient.retrieve(location=location))
        except:
            print(location, "failed")
        
    data = sorted(data, key=lambda x: x.name)
    return Response(version, data)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
