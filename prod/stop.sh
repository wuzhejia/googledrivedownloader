#!/bin/bash

# Find and kill the Gunicorn process
pkill -f 'gunicorn -w 4 -b 0.0.0.0:5000 -D gd:app'

# Display a message
echo "Gunicorn process terminated."
