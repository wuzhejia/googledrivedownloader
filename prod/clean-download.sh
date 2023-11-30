#!/bin/bash

# Directory to clean
directory="/root/prod/download"

# Find files older than 7 days and remove them
find "$directory" -type f -mtime +7 -exec rm {} \;

echo "Cleanup completed."
