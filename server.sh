#!/bin/bash

sleep 1

PYTHONPATH=/app alembic upgrade head
#PYTHONPATH=/app pytest
uvicorn main:app --host 0.0.0.0 --port 8000
