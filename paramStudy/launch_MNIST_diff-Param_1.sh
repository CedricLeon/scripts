#!/bin/bash

echo "This script can be used to study the behaviour of 1 parameter on GEGELATI example MNIST application. It launches many trainings with different values of the specified parameter in the same environment (conditions). Result files are stored in the specified directory."
echo "CARE: depending on the type of your parameter (FLOAT / INT) tou may need to modify the script. You should also check and modify the serie of your parameter values."

# Check the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_MNIST_diff-Param_1.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR PARAM_NAME SEED"
    echo "Example: /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_1.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ nbRoots 2021"
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
let "i = 1"

# Script duration
start=$SECONDS

echo "***********************************************************************************************"

# Initialise the file containing final results
resultFile="$pathRes"lastScore.logs
echo "Final results are stored in \"$resultFile\""
echo "Tested Param: $param. Trainings lead on MNIST with default Kelly parameters on $nbGen generations. With seed : $seed." > "$resultFile"
echo "Training Value Temps Generation Score" >> "$resultFile"

# Main loop
for new in 1 5 10 30 50 100 360 500 1000 2000 3000 4000 5000 7000 10000; do

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

    # Start the training
    echo "Executing and storing results in "$pathExec"bin/"$logsFile""
    "$pathExec"bin/Release/mnist $seed > "$pathExec"bin/"$logsFile"

    # Print the duration of this training
    time=$(( SECONDS - $startTime ))

    # Store best generation score (and the corresponding policy .md)
    everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
    bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'` #awk '{print $NF}'`
    genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
    printf 'Best Score: %s at generation number %d in %dh:%dm:%ds\n' $bestScore $genBestScore $(($time/3600)) $(($time%3600/60)) $(($time%60))
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
time=$(( SECONDS - $start ))
printf 'Total training time: %dh:%dm:%ds\n' $(($time/3600)) $(($time%3600/60)) $(($time%60))
