#!/bin/bash

# $1 : Path to the program directory (ex: /home/cleonard/dev/TpgVvcPartDatabase/)
# $2 : Path to store the results (ex: /home/cleonard/dev/stage/results/scripts_results/)
# $3 : Name of the studied parameter (ex: nbRoots)
# $4 : Seed of the MNIST training (ex: 2021)

# Check the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_MNIST_diff-Param.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR PARAM_NAME PARAM_CURRENT_VALUE"
    echo "Example: /home/cleonard/dev/stage/scripts/launch_MNIST_diff-Param_1.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ maxProgramSize 2021"
    exit
fi

# Extract parameters
pathExec=$1
pathRes=$2
param=$3
seed=$4

# INTEGER: Get the original value of the param (in order to use sed)
originalParam=`cat "$pathExec"params.json | grep "\"$param\"" | grep -o '[0-9]*'`
last=$originalParam

# FLOAT: Get the original value of the param (in order to use sed)
# originalParam=`cat "$pathExec"params.json | grep "\"$param\"" | grep -o '[0-9]*\.[0-9]*'`
# last=$originalParam

# Get the number of generations of the trainings
nbGen=`cat "$pathExec"params.json | grep "\"nbGenerations\"" | grep -o '[0-9]*'`

# Training number (to identify results)
let "i = 0"

echo "***********************************************************************************************"

# Initialise the file containing final results
resultFile="$pathRes"lastScore.logs
echo "Final results are stored in \"$resultFile\""
echo "Tested Param: $param. Trainings lead on MNIST with default Kelly parameters on $nbGen generations. With seed : $seed." > "$resultFile"
echo "Training Value Temps Generation Score" >> "$resultFile"

# Main loop
for new in 5000 7000 10000; do

    # seq generate float number with ',' and not '.' wich is annoying
    new="${new/,/.}"

    echo ' '
    echo "Training N°$i"

    # Time the script
    startTime=$SECONDS

    # Update paths
    fileName=_ent"$i"_MNIST_"$new""$param".txt
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Modify the params.json file with the new value of the studied parameter
    echo "Modifying params.json with: \"$param\": $new"
    sed -i "s/\"$param\": $last/\"$param\": $new/g" "$pathExec"params.json

    # Recompile the executable
    echo "Recompiling mnist"
    #/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release
    /usr/local/bin/cmake --build "$pathExec"bin/ --target mnist -- -j 38

    # Start the training (default: 200 generations ?)
    # No &, we don't want to fork in this script : no parallel execution
    echo "Executing and storing results in "$pathExec"bin/"$logsFile""
    "$pathExec"bin/Release/mnist $seed > "$pathExec"bin/"$logsFile"

    # Print the duration of this training
    time=$(( SECONDS - $startTime ))
    let "min = time/60"
    let "sec = time%60"

    # Store best generation score (and the corresponding policy .md)
    everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
    bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'` #awk '{print $NF}'`
    genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
    echo "Best Score: $bestScore at generation $genBestScore in "$min"min"$sec"s or "$time"s"
    bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)
    echo "$i $new $time $genBestScore $bestScore" >> "$resultFile"

    # Store whole files (confMat + logs)
    echo "Storing results "$logsFile", bestPolicyStats.md, out_best.dot and "$confMatFile""
    mv "$pathExec"bin/"$logsFile" "$pathRes""$logsFile"
    mv "$pathExec"bin/bestPolicyStats.md "$pathRes"bestPolicyStats_ent"$i"_MNIST_"$new""$param".md
    mv "$pathExec"bin/out_best.dot "$pathRes"out_best_ent"$i"_MNIST_"$new""$param".dot
    mv "$pathExec"fileClassificationTable.txt "$pathRes""$confMatFile"

    # Update parameter value and training number
    last=$new
    let "i += 1"
done

# Reset the param
echo "Reseting params.json with: \"$param\": $originalParam"
sed -i "s/\"$param1\": $last/\"$param\": $originalParam/g" "$pathExec"params.json

echo "***********************************************************************************************"

# Compute and print running time
duration=$(( SECONDS - start ))
let "min = duration/60"
let "hour = min/60"
let "min = min%60"
echo "The script runned for $duration seconds, or "$hour"h"$min""
echo ' '
