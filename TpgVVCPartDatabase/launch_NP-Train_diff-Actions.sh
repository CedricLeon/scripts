#!/bin/bash

echo "This script can be used to train and store 5 binary TPGs in the VVCPartdatabase environment."

# Check the good use of the script
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_NP-Train_diff-Actions.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR EXECUTABLE_NAME"
    echo "Example: /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_NP-Train_diff-Actions.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ TPGVVCPartDatabase_binaryFeaturesEnv"
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
#           |------|
#          BTH   OTHER
#                  |
#               |------|
#              BTV   OTHER
#                      |
#                   |------|
#                  TTH    TTV

actions0=( "NP" "QT" "BTH" "BTV" "TTH" "TTV" )
actions1=( "{1,2,3,4,5}" "{0,2,3,4,5}" "{0,1,3,4,5}" "{0,1,2,4,5}" "{0,1,2,3,5}" "{0,1,2,3,4}")

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
echo "N°Action Actions1 Time BestGeneration Score" >> "$resultFile"

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
for action in 0 1 2 3 4 5; do # NP QT BTH BTV TTH
    echo " "
    echo "Training N°$i"

    # Time this training
    startTime=$SECONDS

    # Update paths
    nameAct="${actions0[action]}"
    fileName=_ent"$i"_b"$nameAct"
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Start the training
    echo "Execute and redirect logs in "$logsFile".txt"
    echo "Call "$pathExec"build/$execName "\"{$action}\"" "\"${actions1[action]}\"" "1" "16" "16" "24" "50220" $nameAct "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/64x16_binary-50%/" "0" > "$pathExec"build/"$logsFile".txt"

    "$pathExec"build/$execName "\"{$action}\"" "\"${actions1[action]}\"" "1" "16" "16" "24" "50220" $nameAct "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/16x16_binary-50%/" "0" > "$pathExec"build/"$logsFile".txt
s
    # Compute the duration of this training
    time=$(( SECONDS - $startTime ))

    # Storing best generation score (and the corresponding policy .md)
    everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
    bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'`
    genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
    printf 'Best Score: %s at generation number %d in %dh:%dm:%ds\n' $bestScore $genBestScore $(($time/3600)) $(($time%3600/60)) $(($time%60))
    bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)
    echo "$action "\"${actions1[action]}\"" $time $genBestScore $bestScore" >> "$resultFile"

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
