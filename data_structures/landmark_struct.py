from dataclasses import dataclass

@dataclass
class Landmark:
    lat: float
    lon: float
    name: str