#!/bin/bash

echo "This script can be used to launch many times a specific script and to stores its result in different directories (Usage example: seed behavior study)."
echo "CARE : if the RESULT_DIR already exist this script will empty it ! Read the script carefully"

# Checking the good use of the script
if [ "$#" -ne 7 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_many_scripts_VVCPartDatabase.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR SCRIPT_NAME TRAINING_NAME EXECUTABLE_NAME FIRST_TRAINING_NUMBER LAST_TRAINING_NUMBER"
    echo "Example: /home/cleonard/dev/stage/scripts/TpgVVCPartDatabase/launch_many_scripts_TpgVVCPartDatabase.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ /home/cleonard/dev/stage/scripts/TpgVVCPartDatabase/launch_1train_TPG.sh BIG_training TPGVVCPartDatabase_featuresEnv 1 5"
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

echo "SEED BEST_SCORE GEN_BEST_SCORE TIME" > "$pathRes"recap.logs

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
    $scriptName "$pathExec" "$currentDir"/ "$trainingName""$i" $nameExecutable $i

    echo " "
done

echo "**************************************************************************************************************"
