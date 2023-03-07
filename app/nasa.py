import requests, requests_cache
from dataclasses import dataclass

AU_TO_KM_CONVERSION = 1.495979e8


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
        self.dist_min = float(self.dist_min)
        self.dist_max = float(self.dist_max)
        self.dist_min = float(self.dist_min)
        self.v_rel = float(self.v_rel)
        self.v_inf = float(self.v_inf)
        self.h = float(self.h)


def fetch():
    base_url = f"https://ssd-api.jpl.nasa.gov/cad.api"
    payload = {"dist-min": "1LD", "date-min": "now", "date-max": "+7", "limit": 10}
    r = requests.get(base_url, params=payload)
    r_data = r.json()["data"]
    r_fields = r.json()["fields"]
    readable = [dict(zip(r_fields, data)) for data in r_data]
    return readable


def format():
    requests_cache.install_cache("astro", backend="sqlite", expire_after=180)
    space_response = fetch()
    space = []

    for item in space_response:
        obj = SpaceObject(**item)
        space.append(obj)

    return space


if __name__ == "__main__":
    test1 = [
        {
            "des": "2023 DX",
            "orbit_id": "1",
            "jd": "2460006.565377386",
            "cd": "2023-Mar-03 01:34",
            "dist": "0.0133404519543656",
            "dist_min": "0.0132927026501745",
            "dist_max": "0.0133882006487615",
            "v_rel": "13.0512222235651",
            "v_inf": "13.0359097456893",
            "t_sigma_f": "00:03",
            "h": "25.87",
        },
        {
            "des": "faker",
            "orbit_id": "1",
            "jd": "2460006.565377386",
            "cd": "2023-Mar-03 01:34",
            "dist": "0.0133404519543656",
            "dist_min": "0.0132927026501745",
            "dist_max": "0.0133882006487615",
            "v_rel": "13.0512222235651",
            "v_inf": "13.0359097456893",
            "t_sigma_f": "00:03",
            "h": "25.87",
        },
    ]
