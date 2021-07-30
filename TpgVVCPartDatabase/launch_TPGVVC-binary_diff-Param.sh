#!/bin/bash

echo "This script can be used to study multiple trainings of a binary TPG (specific action) with different values of a particular parameter. This script is a variation of the classic paramStudy on MNIST."

# Checking the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_TPGVVC-binary_diff-Param.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR NB_ACT PARAM_NAME"
    echo "Example: /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_TPGVVC-binary_diff-Param.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ 0 nbRoots"
    exit
fi

# Time the script
start=$SECONDS

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

# Build the soft
/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release -DTESTING=1

# Create a file storing the final scores
resultFile="$pathRes"lastScore.logs
echo "Final results are stored in \"$resultFile\""
echo "Tested Param: $param / Action: $action " > "$resultFile"
echo "Training Value Score" >> "$resultFile"

# Main loop
for new in $(seq 5 5 500); do
    echo ' '
    echo "Training N°$i"

    startTime=$SECONDS

    # Updating paths
    fileName=_ent"$i"_DTB3_b"$action"_"$new""$param".txt
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Modifying the params.json file with the new value of the studied parameter
    echo "Modifying params.json with: \"$param\": $new"
    sed -i "s/\"$param\": $last/\"$param\": $new/g" "$pathExec"params.json

    # Recompiling the executable
    echo "Recompiling TPGVVCPartDatabase_binary"
    cmake --build "$pathExec"build/ --target TPGVVCPartDatabase_binary -- -j 38

    # Starting the training
    echo "Executing and storing results in "$pathExec"build/"$logsFile""
    "$pathExec"build/TPGVVCPartDatabase_binary "$action" > "$pathExec"build/"$logsFile"

    # Compute training duration
    time=$(( SECONDS - $startTime ))

    # Storing last generation score
    lastLine=`cat "$pathExec"/fileClassificationTable.txt | perl -ne 'print if eof'`
    result=$(echo $lastLine | awk '{print $NF}')
    result="${result/./,}"  # Replace . with , (Libre Office Calc usage)
    printf 'Result : %s, in %dh:%dm:%ds\n' $result $(($time/3600)) $(($time%3600/60)) $(($time%60))
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

time=$(( SECONDS - $start ))
printf 'Total training time: %dh:%dm:%ds\n' $(($time/3600)) $(($time%3600/60)) $(($time%60))
echo "***********************************************************************************************"
echo ' '
