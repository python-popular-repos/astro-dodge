import requests, requests_cache
from dataclasses import dataclass

AU_TO_KM_CONVERSION = 1.49e8


@dataclass
class SpaceObject:
    des: str
    orbit_id: str
    jd: str
    cd: str
    dist: float
    dist_min: float
    dist_max: float
    v_rel: float
    v_inf: float
    t_sigma_f: str
    h: float

    def __post_init__(self):
        self.dist = float(self.dist) * AU_TO_KM_CONVERSION
        self.dist_min = round(float(self.dist_min), 2)
        self.dist_max = float(self.dist_max)
        self.dist_min = float(self.dist_min)
        self.v_rel = float(self.v_rel)
        self.v_inf = round(float(self.v_inf), 2)
        self.h = float(self.h)


def fetch():
    base_url = f"https://ssd-api.jpl.nasa.gov/cad.api"
    payload = {"dist-min": "2LD", "date-min": "now", "date-max": "+14"}
    r = requests.get(base_url, params=payload)
    r_data = r.json()["data"]
    r_fields = r.json()["fields"]
    readable = [dict(zip(r_fields, data)) for data in r_data]
    return readable


def format():
    requests_cache.install_cache("astro", backend="sqlite", expire_after=10)
    space_response = fetch()
    space = [SpaceObject(**item) for item in space_response]
    return space
