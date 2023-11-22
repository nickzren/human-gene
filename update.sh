#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

bash download.sh
python3 process.py

# push the changes to remote repository
git add data/output/protein_coding_gene.csv
git commit -m "Weekly update"
git push
