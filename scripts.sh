#!/bin/bash
python3 -m pytest -v
python3 -m pytest --cov=app/ tests/
poetry export -f requirements.txt --without-hashes > app/requirements.txt