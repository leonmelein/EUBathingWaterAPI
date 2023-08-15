from datetime import datetime
from typing import List
from Models.Area import Area


class Response():

    def __init__(self, version: str, data: List[Area]):
        self.Version = version
        self.LastUpdated = datetime.now().isoformat()
        self.Data = data
