#!/bin/bash
source /app/.venv/bin/activate
pip install webdriver-manager
playwright install chromium --with-deps  # Fallback if needed, but Selenium uses webdriver-manager
uvicorn main:app --host 0.0.0.0 --port $PORT
