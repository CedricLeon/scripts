#!/bin/bash

# Checking the good use of the script
if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_many_scripts.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR SCRIPT_NAME PARAM_NAME FIRST_TRAINING_NUMBER LAST_TRAINING_NUMBER"
    echo "Example: /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_1.sh nbRoots 2 5"
    exit
fi

# Extracting parameters
pathExec=$1
pathRes=$2
scriptName=$3
paramName=$4
#paramSeq=$5 # PARAM_SEQUENCE
firstNumTrain=$5
lastNumTrain=$6

# Build mnist if ./bin/ is clear
/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release

# Launch ($lastNumTrain - $firstNumTrain) trainings to study parameter behavior and stores results in different directories
for i in $(seq $firstNumTrain $lastNumTrain); do

    # Which directory ?
    currentDir="$pathRes""$paramName""$i"

    # If the result repertory doesn't exist, create it, else empty it
    if [ ! -d "$currentDir" ];then
        mkdir "$currentDir"
    else
        rm -rf "$currentDir"/*
    fi

    # Call the script launching the study with the corresponding result repertory and seed
    $scriptName "$pathExec" "$currentDir"/ $paramName $i
done
