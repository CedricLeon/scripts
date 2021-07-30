#!/bin/bash

echo "This script can be used to train and store 5 binary TPGs in the VVCPartdatabase environment. It's a variation of launch_NP-Train_diff-Actions.sh, the specific action can be specified and is not necessarily 0, 1, 2, 3, 4 or 5 (CARE : Up-to-date only the TPGVVCPartDatabase_binaryFeaturesEnv executable offers such feature);"

# Check the good use of the script
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_NP-Train_diff-Actions_personnalized.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR EXECUTABLE_NAME"
    echo "Example: /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_NP-Train_diff-Actions_personnalized.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ TPGVVCPartDatabase_binaryFeaturesEnv"
    exit
fi

# Extract and initialize parameters
pathExec=$1
pathRes=$2
execName=$3

#   SPLITS ?
#     |
#  |------|
# NP    OTHER
#         |
#      |------|
#     QT     OTHER
#              |
#          |--------|
#        HORI     VERTI
#         |         |
#     |-----|    |-----|
#    BTH   TTH  BTV   TTV

actionsName=( "NP" "QT" "DIREC" "HORI" "VERTI" )
actions0=( "{0}" "{1}" "{2,4}" "{2}" "{3}" )
actions1=( "{1,2,3,4,5}" "{2,3,4,5}" "{3,5}" "{4}" "{5}" )

# Training number (to store results)
let "i = 1"

# Script duration
start=$SECONDS

# Create a file storing the final scores
resultFile="$pathRes"recapScore.logs
echo " "
echo "Final results are stored in \"$resultFile\""
echo "Final scores of each training :" > "$resultFile"
echo " " >> "$resultFile"
echo "Action0 Actions1 Time BestGeneration Score" >> "$resultFile"

# Storing trainings parameters
echo "Copy trainings parameters \"params.json\" in $pathRes"
cp "$pathExec"params.json "$pathRes"params.json

# Build and compile the executable
echo "Build and compile TPGVVCPartDatabase_binary"

# Since last cmake update (3.19.8) bash doesn't find cmake in /usr/bin/, so I call the default cmake (included in $PATH)
/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release -DTESTING=1
/usr/local/bin/cmake --build "$pathExec"build/ --target $execName -- -j 38

# Create the global repertory
mkdir "$pathRes"all
cp "$pathRes"params.json "$pathRes"all/params.json

# Main loop
for train in 0 1 2 3 4; do
    echo " "
    echo "Training N°$i"

    # Time this training
    startTime=$SECONDS

    # Update paths
    nameAct="${actionsName[train]}"
    fileName=_ent"$i"_b"$nameAct"
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Start the training
    echo "Execute and redirect logs in "$logsFile".txt"
    echo "Call "$pathExec"build/$execName "\"${actions0[train]}\"" "\"${actions1[train]}\"" "0" "32" "32" "112" "100000" $nameAct > "$pathExec"build/"$logsFile".txt"
    "$pathExec"build/"$execName" "\"${actions0[train]}\"" "\"${actions1[train]}\"" "0" "32" "32" "112" "100000" $nameAct > "$pathExec"build/"$logsFile".txt

    # Compute the duration of this training
    time=$(( SECONDS - $startTime ))

    # Storing best generation score (and the corresponding policy .md)
    everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
    bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'`
    genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
    printf 'Best Score: %s at generation number %d in %dh:%dm:%ds\n' $bestScore $genBestScore $(($time/3600)) $(($time%3600/60)) $(($time%60))
    bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)

    echo "Best Score: $bestScore at generation number $genBestScore in "$min"min"$sec"s or "$time"s"
    echo ""\"${actions0[train]}\"" "\"${actions1[train]}\"" $time $genBestScore $bestScore" >> "$resultFile"

    # Store whole files (logs.txt + best_root.dot + best_stats.md + confMat.txt + bestPolicyStats.md)
    echo "Store results in "$pathRes""$nameAct"/"
    mkdir "$pathRes""$nameAct"
    mv "$pathExec"build/"$logsFile".txt "$pathRes""$nameAct"/"$logsFile"_"$bestScore".txt
    mv "$pathExec"build/out_best.dot "$pathRes""$nameAct"/out_best_last_ent"$i"_b"$nameAct"_"$bestScore".dot
    mv "$pathExec"build/out_best_stats.md "$pathRes""$nameAct"/out_best_stats_ent"$i"_b"$nameAct"_"$bestScore".md
    mv "$pathExec"build/bestPolicyStats.md "$pathRes""$nameAct"/bestPolicyStats_ent"$i"_b"$nameAct"_"$bestScore".md
    mv "$pathExec"fileClassificationTable.txt "$pathRes""$nameAct"/"$confMatFile"_"$bestScore".txt

    # For all/ directory
    cp "$pathRes""$nameAct"/out_best_last_ent"$i"_b"$nameAct"_"$bestScore".dot "$pathRes"all/"$nameAct".dot

    # Update training number
    let "i += 1"
done

# Complete all/ directory with the final scores file
cp "$resultFile" "$pathRes"all/recapScore.logs

time=$(( SECONDS - $start ))
printf 'Total training time: %dh:%dm:%ds\n' $(($time/3600)) $(($time%3600/60)) $(($time%60))
