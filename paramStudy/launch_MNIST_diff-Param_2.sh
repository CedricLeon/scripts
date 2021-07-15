#!/bin/bash

echo "This script can be used to study the behaviour of 2 parameters on GEGELATI example MNIST application. It's a variation of launch_MNIST_diff-Param_1.sh with 2 parameters. It launches many trainings with different values of the specified parameters in the same environment (conditions). Result files are stored in the specified directory."
echo "CARE: depending on the type of your parameter (FLOAT / INT) tou may need to modify the script. You should also check and modify the serie of your parameter values."

# Check the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_MNIST_diff-Param_2.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR PARAM_NAME SEED"
    echo "Example: /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_2.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ pEdge 2021"
    exit
fi

# Extract parameters
pathExec=$1
pathRes=$2
param=$3        #for pEdgeDeletion and pEdgeAddition must be only "pEdge"
                #for pEdgeDestinationChange and pEdgeDestinationIsAction must be only "pEdgeDestination"
param1=pMutate
param2=pSwap
seed=$4

# # INTEGER: Get the original value of the param (in order to use sed)
# originalParam1=`cat "$pathExec"params.json | grep "\"$param1\"" | grep -o '[0-9]*'`
# last1=$originalParam1
# originalParam2=`cat "$pathExec"params.json | grep "\"$param2\"" | grep -o '[0-9]*'`
# last2=$originalParam2

# FLOAT: Get the original value of the param (in order to use sed)
originalParam1=`cat "$pathExec"params.json | grep "\"$param1\"" | grep -o '[0-9]*\.[0-9]*'`
last1=$originalParam1

originalParam2=`cat "$pathExec"params.json | grep "\"$param2\"" | grep -o '[0-9]*\.[0-9]*'`
last2=$originalParam2

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
echo "Tested Params: $param1 and $param2. Trainings lead on MNIST with default Kelly parameters on $nbGen generations. With seed : $seed." > "$resultFile"
echo "Training Value1 Value2 Temps Generation Score" >> "$resultFile"

#param2Values=( "0.01" "0.05" "0.1" "0.15" "0.2" "0.25" "0.3" "0.35" "0.4" "0.42" "0.44" "0.46" "0.48" "0.5" "0.52" "0.54" "0.56" "0.58" "0.6" "0.65" "0.7" "0.75" "0.8" "0.85" "0.9" "0.95" "1.0" ) # 27

# Main loop
for new in 0,01 $(seq 0.05 0.05 0.8) $(seq 0.82 0.02 1.0); do

    # seq generate float number with ',' and not '.' wich is annoying
    new="${new/,/.}"
    value1=$new
    value2=$new #"${param2Values[i]}"

    echo ' '
    echo "Training N°$i"

    # Time the script
    startTime=$SECONDS

    # Update paths
    fileName=_ent"$i"_MNIST_"$new""$param".txt
    logsFile=logs"$fileName"
    confMatFile=confMat"$fileName"

    # Modify the params.json file with the new value of the studied parameter
    echo "Modifying params.json with: \"$param1\": $value1 and \"$param2\": $value2"
    sed -i "s/\"$param1\": $last1/\"$param1\": $value1/g" "$pathExec"params.json
    sed -i "s/\"$param2\": $last2/\"$param2\": $value2/g" "$pathExec"params.json

    # Recompile the executable
    echo "Recompiling mnist"
    #/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release
    /usr/local/bin/cmake --build "$pathExec"bin/ --target mnist -- -j 38

    # Start the training
    # No &, we don't want to fork in this script : no parallel execution
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
    echo "$i $value1 $value2 $time $genBestScore $bestScore" >> "$resultFile"

    # Store whole files (confMat + logs)
    echo "Storing results "$logsFile", bestPolicyStats.md, out_best.dot and "$confMatFile""
    mv "$pathExec"bin/"$logsFile" "$pathRes""$logsFile"
    mv "$pathExec"bin/bestPolicyStats.md "$pathRes"bestPolicyStats_ent"$i"_MNIST_"$new""$param".md
    mv "$pathExec"bin/out_best.dot "$pathRes"out_best_ent"$i"_MNIST_"$new""$param".dot
    mv "$pathExec"fileClassificationTable.txt "$pathRes""$confMatFile"

    # Update parameters value and training number
    last1=$value1
    last2=$value2
    let "i += 1"
done

# Reset the param
echo "Reseting params.json with: \"$param1\": $originalParam1 and \"$param2\": $originalParam2"
sed -i "s/\"$param1\": $last1/\"$param1\": $originalParam1/g" "$pathExec"params.json
sed -i "s/\"$param2\": $last2/\"$param2\": $originalParam2/g" "$pathExec"params.json

echo "***********************************************************************************************"

# Compute and print running time
time=$(( SECONDS - $start ))
printf 'Total training time: %dh:%dm:%ds\n' $(($time/3600)) $(($time%3600/60)) $(($time%60))
