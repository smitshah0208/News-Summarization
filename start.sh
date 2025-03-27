#!/bin/bash
# Exit script if any command fails
set -e

# Start uvicorn in background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in foreground
streamlit run app.py --server.port 7860 --server.address 0.0.0.0