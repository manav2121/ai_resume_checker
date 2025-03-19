#!/bin/bash

# Ensure pip is up-to-date
pip install --upgrade pip  

# Install dependencies (force reinstall to avoid issues)
pip install --no-cache-dir --force-reinstall flask gunicorn PyMuPDF
