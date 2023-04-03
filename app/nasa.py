import requests, requests_cache
from typing import List
from dataclasses import dataclass


@dataclass
class SpaceObject:
    """Python dataclass for individually tracked objects in space."""

    des: str
    jd: str
    cd: str
    orbit_id: str
    t_sigma_f: str
    h: float
    dist: float
    dist_min: float
    dist_max: float
    v_rel: float
    v_inf: float

    def __post_init__(self):
        AU_TO_KM_CONVERSION = 1.49e8
        self.dist = float(self.dist) * AU_TO_KM_CONVERSION
        self.dist_min = round(float(self.dist_min), 2)
        self.dist_max = float(self.dist_max)
        self.dist_min = float(self.dist_min)
        self.v_rel = float(self.v_rel)
        self.v_inf = round(float(self.v_inf), 2)
        self.h = float(self.h)


def _fetch():
    """Raw response from the NASA API"""
    base_url = f"https://ssd-api.jpl.nasa.gov/cad.api"
    payload = {"dist-min": "2LD", "date-min": "now", "date-max": "+14"}
    nasa_response = requests.get(base_url, params=payload)
    requests_cache.install_cache("astro", backend="sqlite", expire_after=10)
    return nasa_response


def _format_to_dict() -> List[dict]:
    response = _fetch()
    r_data = response.json()["data"]
    r_fields = response.json()["fields"]
    readable = [dict(zip(r_fields, data)) for data in r_data]
    return readable


def format_space_object(
    response_dict: List[dict] = _format_to_dict(),
) -> List[SpaceObject]:
    space = [SpaceObject(**item) for item in response_dict]
    return space
