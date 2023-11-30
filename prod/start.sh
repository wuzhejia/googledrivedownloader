#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:5000 -D gd:app --error-logfile gunicorn-error.log --access-logfile gunicorn-access.log