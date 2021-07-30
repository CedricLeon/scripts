#!/bin/bash

echo "This script can be used to study the behaviour of many parameters on GEGELATI example MNIST application. It's a variation of launch_MNIST_diff-Param_2.sh with X parameters, but these parameters will all have the same value. It launches many trainings with different values of the specified parameters in the same environment (conditions). Result files are stored in the specified directory."
echo "CARE: you should check and modify the serie of your parameters values."

# Check the good use of the script
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_MNIST_diff-Param_all-prob.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR PARAM_NAME SEED"
    echo "Example: /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_all-prob.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ AllProbTPG 2021"
    exit
fi

# Extract parameters
pathExec=$1
pathRes=$2
p1="pDelete"
p2="pAdd"
p3="pMutate"
p4="pSwap"
#p5="pEdgeDestinationIsAction"
param=$3
seed=$4

# FLOAT: Get the original value of the param (in order to use sed)
originalP1=`cat "$pathExec"params.json | grep "\"$p1\"" | grep -o '[0-9]*\.[0-9]*'`
originalP2=`cat "$pathExec"params.json | grep "\"$p2\"" | grep -o '[0-9]*\.[0-9]*'`
originalP3=`cat "$pathExec"params.json | grep "\"$p3\"" | grep -o '[0-9]*\.[0-9]*'`
originalP4=`cat "$pathExec"params.json | grep "\"$p4\"" | grep -o '[0-9]*\.[0-9]*'`
#originalP5=`cat "$pathExec"params.json | grep "\"$p5\"" | grep -o '[0-9]*\.[0-9]*'`

lastP1=$originalP1
lastP2=$originalP2
lastP3=$originalP3
lastP4=$originalP4
#lastP5=$originalP5

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
echo "Tested Param: "$param". Trainings lead on MNIST with default Kelly parameters on $nbGen generations. With seed : $seed." > "$resultFile"
echo "Training Value Temps Generation Score" >> "$resultFile"

# Main loop
for new in 0,01 $(seq 0.05 0.05 1.0); do

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
    echo "Modifying params.json with: "$param": $new"
    sed -i "s/\"$p1\": $lastP1/\"$p1\": $new/g" "$pathExec"params.json
    sed -i "s/\"$p2\": $lastP2/\"$p2\": $new/g" "$pathExec"params.json
    sed -i "s/\"$p3\": $lastP3/\"$p3\": $new/g" "$pathExec"params.json
    sed -i "s/\"$p4\": $lastP4/\"$p4\": $new/g" "$pathExec"params.json
    #sed -i "s/\"$p5\": $lastP5/\"$p5\": $new/g" "$pathExec"params.json

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
    lastP1=$new
    lastP2=$new
    lastP3=$new
    lastP4=$new
    #lastP5=$new

    let "i += 1"
done

# Reset the param
echo "Reseting params.json with original values for every tpg Prob"
sed -i "s/\"$p1\": $lastP1/\"$p1\": $originalP1/g" "$pathExec"params.json
sed -i "s/\"$p2\": $lastP2/\"$p2\": $originalP2/g" "$pathExec"params.json
sed -i "s/\"$p3\": $lastP3/\"$p3\": $originalP3/g" "$pathExec"params.json
sed -i "s/\"$p4\": $lastP4/\"$p4\": $originalP4/g" "$pathExec"params.json
#sed -i "s/\"$p5\": $lastP5/\"$p5\": $originalP5/g" "$pathExec"params.json

echo "***********************************************************************************************"

# Compute and print running time
time=$(( SECONDS - $start ))
printf 'Total training time: %dh:%dm:%ds\n' $(($time/3600)) $(($time%3600/60)) $(($time%60))
