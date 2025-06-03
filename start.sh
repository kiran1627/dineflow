#!/bin/bash
uvicorn fastapi-app.main:app --host 0.0.0.0 --port 8000
