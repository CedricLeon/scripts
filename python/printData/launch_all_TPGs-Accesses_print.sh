#!/bin/bash

pathExec="/home/cleonard/dev/stage/scripts/python/"
pathRes="/home/cleonard/dev/stage/results/scripts_results/Actions_bal_dataset1/"

cd $pathExec
source envVirDTB/bin/activate

actionsName=( "NP" "QT" "BTH" "BTV" "TTH" "TTV" )

for action in 0 1 2 3 5; do
    fileName=`ls "$pathRes""${actionsName[action]}"/ | grep 'out_best_stats' | grep -o 'out_best_stats.*$'`
    python3.6 print_TPGAcesses.py "$pathRes""${actionsName[action]}"/"$fileName" &
done
