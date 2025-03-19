#!/bin/bash

# Ensure pip is up-to-date
pip install --upgrade pip  

# Force reinstall Gunicorn
pip install --no-cache-dir --force-reinstall gunicorn  

# Force reinstall PyMuPDF
pip install --no-cache-dir --force-reinstall PyMuPDF==1.24.0  
