"""
This file (test_nasa.py) contains the unit tests for the nasa.py file.
Examples:
* Focus on testing small units of code in isolation 
  (ie database models, utility functions)
"""
from app.nasa import SpaceObject, _fetch, _format_to_dict, format_space_object


def test_api():
    test = _fetch()
    assert test.status_code == 200
    assert test.encoding == "utf-8"
    assert test.ok == True
    assert test.headers["content-type"] == "application/json"


def test_format_to_dict():
    test = _format_to_dict()
    assert type(test) is list
    assert type(test[0]) is dict


def test_formatting():
    test = format_space_object()
    assert type(test) is list
    assert type(test[0]) is SpaceObject


def test_space_object(mock_space_object):
    mock = mock_space_object
    assert mock["des"] == "pytest"
    assert mock["orbit_id"] == "0"
    assert mock["jd"] == "100.1"
    assert mock["cd"] == "2023-Apr-01 00:00"
    assert mock["dist"] == "0.1001"
    assert mock["dist_min"] == "0.0"
    assert mock["dist_max"] == "0.1"
    assert mock["v_rel"] == "10.0"
    assert mock["v_inf"] == "10.1"
    assert mock["t_sigma_f"] == "00:00"
    assert mock["h"] == "100.101"


def test_format_space_object(mock_space_object):
    mock = mock_space_object
    space_mock = SpaceObject(**mock)
    assert type(space_mock) is SpaceObject
    assert type(space_mock.dist) is float
    assert space_mock.des == "pytest"
