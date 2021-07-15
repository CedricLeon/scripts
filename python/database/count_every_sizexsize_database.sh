#!/bin/bash

pathExec="/home/cleonard/dev/stage/scripts/python/"
scriptName="database/balance-count_10CSV-dtb_from_unbalanced.py"

pathResult="/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/"

pathDTB="/media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/"
fileRecapName="AllDtbCompo.txt"
fileRecap="$pathDTB""$fileRecapName"

cd $pathExec
source envVirDTB/bin/activate

#echo "DTB [NP,QT,BTH,BTV,TTH,TTV] TOTAL" > "$fileRecap"

database=( "4x8" "4x16" "4x32" "4x64" "8x4" "8x8" "8x16" "8x32" "8x64" "16x4" "16x8" "16x16" "16x32" "16x64" "32x4" "32x8" "32x16" "32x32" "32x64" "64x4" "64x8" "64x16" "64x32" "64x64" )

for i in $(seq 0 1 23); do

    dtbOrigin="$pathDTB""${database[i]}"/
    dtbArrival="$pathResult""${database[i]}""_balanced"
    mkdir "$dtbArrival"

    echo "Call balance script for $dtbOrigin database and store in $dtbArrival"
    python3.6 "$pathExec""$scriptName" "$dtbOrigin" "$dtbArrival" "$fileRecap"
done
