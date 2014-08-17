#!/bin/bash
clear

echo "Hello, $USER!"
echo "Start collecting data."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_RESULTS="$DIR/script_results"
mkdir -p $SCRIPT_RESULTS

collect_models_data()
{
    local file="$SCRIPT_RESULTS/$(date +"%Y-%m-%d").dat"
    if [ ! -f "$file" ] ; then
         touch "$file"
     fi

    ./manage.py models_info 2>"$file"
}

collect_models_data