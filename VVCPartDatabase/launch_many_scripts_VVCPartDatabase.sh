#!/bin/bash

# Checking the good use of the script
if [ "$#" -ne 7 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_many_scripts.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR SCRIPT_NAME TRAINING_NAME EXECUTABLE_NAME FIRST_TRAINING_NUMBER LAST_TRAINING_NUMBER"
    echo "Example: /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_many_scripts_VVCPartDatabase.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ /home/cleonard/dev/stage/scripts/paramStudy/VVCPartDatabase/launch_1train_TPG.sh BIG_training TPGVVCPartDatabase_featuresEnv 1 5"
    exit
fi

# Extracting parameters
pathExec=$1
pathRes=$2
scriptName=$3
trainingName=$4
nameExecutable=$5
firstNumTrain=$6
lastNumTrain=$7


# Storing trainings parameters
echo "Copy trainings parameters \"params.json\" in $pathRes"
cp "$pathExec"params.json "$pathRes"params.json
echo " "

# Launch ($lastNumTrain - $firstNumTrain) trainings to study parameter behavior and stores results in different directories
for i in $(seq $firstNumTrain $lastNumTrain); do

    echo "**************************************************************************************************************"
    echo " "
    echo "Training N°$i"

    # Which directory ?
    currentDir="$pathRes""$trainingName""$i"

    # If the result repertory doesn't exist, create it, else empty it
    if [ ! -d "$currentDir" ];then
        echo "Create $currentDir repertory"
        mkdir "$currentDir"
    else
        echo "Empty $currentDir repertory"
        rm -rf "$currentDir"/*
    fi

    # Call the script launching the study with the corresponding result repertory (and seed)
    echo "Launch  $scriptName"
    $scriptName "$pathExec" "$currentDir"/ $trainingName $nameExecutable $i


    echo " "
done

echo "**************************************************************************************************************"
