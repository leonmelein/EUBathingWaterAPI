from fastapi import FastAPI
from datetime import datetime
import os

from Sources.Marineterrein import MarineTerrein
from Sources.ZwemwaterNL import ZwemwaterNL

version = os.getenv("version") if os.getenv("version") else 1.0
app = FastAPI()


@app.get("/")
async def main():
    data = []
    data.append(MarineTerrein.retrieve())
    data.append(ZwemwaterNL.retrieve())

    return {
        "Version": version,
        "LastUpdated": datetime.now().isoformat(),
        "Areas": data
    }


if __name__ == '__main__':
    main()
