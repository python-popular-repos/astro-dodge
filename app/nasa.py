import requests
from typing import List
from app import db
from app.models import SpaceObject, SpaceRecord


def _fetch():
    """Raw response from the NASA API"""
    base_url = f"https://ssd-api.jpl.nasa.gov/cad.api"
    payload = {"dist-min": "2LD", "date-min": "now", "date-max": "+14"}
    nasa_response = requests.get(base_url, params=payload)
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


def seed_db():
    data = format_space_object()
    for item in data:
        data_base = SpaceRecord(item)
        db.session.add(data_base)
    db.session.commit()
