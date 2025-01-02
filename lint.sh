#!/usr/bin/env bash

uv run isort plot.py
uv run black -l 120 plot.py
uv run flake8 --max-line-length 120 plot.py
uv run mypy --ignore-missing-import plot.py