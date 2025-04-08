#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# Pull latest changes before starting work
git pull

# Run data processing steps
bash download.sh
python3 process.py

# Push the changes to remote repository
git add data/output/*.csv
git commit -m "Weekly update"
git push
