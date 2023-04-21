#!/bin/bash
python3 -m pytest -v
python3 -m pytest --cov=app/ tests/ --cov-report html
poetry export -f requirements.txt --without-hashes > app/requirements.txt