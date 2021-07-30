#!/bin/bash

echo "This script is used to launch print_TPGAcesses.py many times. It calls it for each action in [NP, QT, BTH, BTV, TTH, TTV]."
echo "This script doesn't need arguments (please check it to modify paths and variables)."

# Paths
pathExec="/home/cleonard/dev/stage/scripts/python/"
pathRes="/home/cleonard/dev/stage/results/scripts_results/Binary/Actions_bal_dataset1/"

# Auto access virtual python environment and activate it
cd $pathExec
source envVirDTB/bin/activate

# Browse and launch print_TPGAcesses.py for every action
actionsName=( "NP" "QT" "BTH" "BTV" "TTH" "TTV" )
for action in 0 1 2 3 5; do
    fileName=`ls "$pathRes""${actionsName[action]}"/ | grep 'out_best_stats' | grep -o 'out_best_stats.*$'`
    python3.6 print_TPGAcesses.py "$pathRes""${actionsName[action]}"/"$fileName" &
done
