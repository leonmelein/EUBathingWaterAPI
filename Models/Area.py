from Models.WaterQuality import WaterQuality


class Area:
    def __init__(self, name: str, quality: WaterQuality, temperature: float = None):
        self.name = name
        self.quality = quality
        self.temperature = temperature
