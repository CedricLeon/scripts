#!/bin/bash

# $1 : Path to the program directory (ex: /home/cleonard/dev/TpgVvcPartDatabase/)
# $2 : Path to store the results (ex: /home/cleonard/dev/stage/results/scripts_results/)

# Check the good use of the script
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_non-parallel_trainings.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR"
    echo "Example: /home/cleonard/dev/stage/scripts/launch_NP-Train_diff-Actions.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/"
    exit
fi

# Extract and initialize parameters
pathExec=$1
pathRes=$2
actionsName=( "NP" "QT" "BTH" "BTV" "TTH" "TTV" )
let "i = 0"                                         # Training number (to store results)

# Create a file storing the final scores
resultFile="$pathRes"recapScore.logs
echo "Final results are stored in \"$resultFile\""
echo "Final scores of each training (NO CONVOLUTION) :" > "$resultFile"
echo ' ' >> "$resultFile"
echo "N°Action BestGeneration Score" >> "$resultFile"

# Storing trainings parameters
echo "Copy trainings parameters \"params.json\" in $pathRes"
cp "$pathExec"params.json "$pathRes"params.json

# Build and compile the executable
echo "Build and compile TPGVVCPartDatabase_binary"
# Since last cmake update (3.19.8) bash doesn't find cmake in /usr/bin/, so I call the default cmake (included in $PATH)
/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release -DTESTING=1
/usr/local/bin/cmake --build "$pathExec"build/ --target TPGVVCPartDatabase_binary -- -j 38

# Main loop
for action in 5 0 1 2 3; do # TTV NP QT BTH BTV
    echo " "
    echo "Training N°$i"

    # Update paths
    nameAct="${actionsName[action]}"
    fileName=_ent"$i"_b"$nameAct"
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Start the training (No &, we don't want to fork in this script : no parallel execution)
    echo "Execute and redirect logs in "$logsFile".txt"
    "$pathExec"build/TPGVVCPartDatabase_binary "$action" > "$pathExec"build/"$logsFile".txt

    # # Store last generation score
    # lastLine=`cat "$pathExec"/fileClassificationTable.txt | perl -ne 'print if eof'`    # Get last line of the file
    # bestScore=$(echo $lastLine | awk '{print $NF}')                                        # Get last "word" of the string
    # bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)
    # echo "Result : $bestScore"
    # echo "$nameAct $bestScore" >> "$resultFile"

    # Storing best generation score (and the corresponding policy .md)
    everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
    bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'`
    genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
    echo "Best Score: $bestScore at generation number $genBestScore"
    bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)
    echo "$action $genBestScore $bestScore" >> "$resultFile"

    # Store whole files (logs.txt + best_root.dot + best_stats.md + confMat.txt + bestPolicyStats.md)
    echo "Store results in "$pathRes""$nameAct"/"
    mkdir "$pathRes""$nameAct"
    mv "$pathExec"build/"$logsFile".txt "$pathRes""$nameAct"/"$logsFile"_"$bestScore".txt
    mv "$pathExec"build/out_best.dot "$pathRes""$nameAct"/out_best_ent"$i"_b"$nameAct"_"$bestScore".dot
    mv "$pathExec"build/out_best_stats.md "$pathRes""$nameAct"/out_best_stats_ent"$i"_b"$nameAct"_"$bestScore".md
    mv "$pathExec"build/bestPolicyStats.md "$pathRes""$nameAct"/bestPolicyStats_ent"$i"_b"$nameAct"_"$bestScore".md
    mv "$pathExec"fileClassificationTable.txt "$pathRes""$nameAct"/"$confMatFile"_"$bestScore".txt

    # Update training number
    let "i += 1"
done
