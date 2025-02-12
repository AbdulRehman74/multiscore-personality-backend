#!/bin/bash
poetry install
exec uvicorn app.main:app --host=0.0.0.0 --port=${PORT}
