#!/bin/bash

# $1 : Path to the program directory (ex: /home/cleonard/dev/TpgVvcPartDatabase/)
# $2 : Path to store the results (ex: /home/cleonard/dev/stage/results/scripts_results/)
# $3 : The specific split of the binary TPG (NP, QT, BTH, BTV, TTH, TTV)
# $4 : Name of the studied parameter (ex: nbRoots)
# $5 : Current value of the studied parameter (ex: 2000)
# $6 : Number of generations for each training (ex: 150)
# $7 : Current value for nbGenerations
# (bonus) $8 : range of modification (ex: "seq -1 500 10001")

# Checking the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_TPGVVC_diff-Param.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR NB_ACT PARAM_NAME"
    echo "Example: /home/cleonard/dev/stage/scripts/launch_NP-Train_diff-Param.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ 0 nbRoots"
    exit
fi

# Time the script
startTime=$SECONDS

# Extracting parameters
pathExec=$1
pathRes=$2
action=$3
param=$4

# Getting the original value of the param (in order to use sed)
originalParam=`cat "$pathExec"params.json | grep "\"$param\"" | grep -o '[0-9]*'`
last=$originalParam

# Training number (to store results)
let "i = 0"

echo "***********************************************************************************************"

resultFile="$pathRes"lastScore.logs
echo "Final results are stored in \"$resultFile\""

echo "Tested Param: $param / Action: $action " > "$resultFile"
echo "Training Value Score" >> "$resultFile"

# Main loop
for new in $(seq 5 5 500); do
    echo ' '
    echo "Training N°$i"

    # Updating paths
    fileName=_ent"$i"_DTB3_b"$action"_"$new""$param".txt
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Modifying the params.json file with the new value of the studied parameter
    echo "Modifying params.json with: \"$param\": $new"
    sed -i "s/\"$param\": $last/\"$param\": $new/g" "$pathExec"params.json

    # Recompiling the executable
    echo "Recompiling TPGVVCPartDatabase_binary"
    #cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release -DTESTING=1
    cmake --build "$pathExec"build/ --target TPGVVCPartDatabase_binary -- -j 38

    # Starting the training (default: 200 generations ?)
    # No &, we don't want to fork in this script : no parallel execution
    echo "Executing and storing results in "$pathExec"build/"$logsFile""
    "$pathExec"build/TPGVVCPartDatabase_binary "$action" > "$pathExec"build/"$logsFile"

    # Storing last generation score
    lastLine=`cat "$pathExec"/fileClassificationTable.txt | perl -ne 'print if eof'`
    result=$(echo $lastLine | awk '{print $NF}')
    result="${result/./,}"  # Replace . with , (Libre Office Calc usage)
    echo "Result : $result"
    echo "$i $new $result" >> "$resultFile"

    # Store whole files (confMat + logs)
    echo "Storing results "$pathRes""$logsFile" and "$confMatFile""
    mv "$pathExec"build/"$logsFile" "$pathRes""$logsFile"
    mv "$pathExec"fileClassificationTable.txt "$pathRes""$confMatFile"

    # Update parameter value and training number
    last=$new
    let "i += 1"
done

# Reset the param
echo "Reseting params.json with: \"$param\": $new"
sed -i "s/\"$param\": $last/\"$param\": $originalParam/g" "$pathExec"params.json

# Compute and print running time
duration=$(( SECONDS - start ))
let "min = duration/60"
let "hour = min/60"
let "min = min%60"
echo "The script run for $duration seconds, or "$hour"h"$min""
echo "***********************************************************************************************"
echo ' '
