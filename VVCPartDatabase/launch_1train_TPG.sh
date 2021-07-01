#!/bin/bash

echo "This script can be used to train a TPG in the VVCPartdatabase environment. It's often used through launch_many_scripts_VVCPartDatabase.sh."

# Checking the good use of the script
if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters"
    echo "Usage: launch_1train_TPG.sh PATH_TO_PROGRAM_DIR PATH_TO_RESULT_DIR NAME_OF_TRAINING NAME_OF_EXECUTABLE SEED"
    echo "Example: /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_1train_TPG.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/ BIG_training TPGVVCPartDatabase_featuresEnv 2021"
    exit
fi

# Extracting parameters
pathExec=$1
pathRes=$2
name=$3
nameExec=$4
seed=$5

# Time the script
startTime=$SECONDS

# Build and compile the executable
echo "Build and compile $nameExec"
/usr/local/bin/cmake "$pathExec" -DCMAKE_BUILD_TYPE=Release -DTESTING=1
/usr/local/bin/cmake --build "$pathExec"build/ --target $nameExec -- -j 38

# Create a file storing the final scores
resultFile="$pathRes"recap.logs
echo "Final result is stored in \"$resultFile\""

# Init files name
fileName=_features_"$name"
logsFile=logs"$fileName"
confMatFile=confMat"$fileName"

# Start the training (No &, we don't want to fork in this script : no parallel execution)
echo "Execute and redirect logs in "$logsFile".txt"
"$pathExec"build/"$nameExec" $seed > "$pathExec"build/"$logsFile".txt

# Compute the duration of this training
time=$(( SECONDS - $startTime ))
let "min = time/60"
let "sec = time%60"

# Store best generation score (and the corresponding policy .md)
everyScore=`cat "$pathExec"fileClassificationTable.txt | grep -o '[0-9]*\.[0-9]*$' | sort -n`
bestScore=`echo $everyScore | perl -ne 'print if eof' | grep -o '[0-9]*\.[0-9]*$'`
genBestScore=`cat "$pathExec"fileClassificationTable.txt | grep "$bestScore" | grep -o '^\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$'`
echo "Best Score: "$bestScore" at generation number N°"$genBestScore" with seed "$seed" in "$min"min"$sec"s or "$time"s"
bestScore="${bestScore/./,}"  # Replace . with , (Libre Office Calc usage)
echo "Final result: "$bestScore" at generation N°"$genBestScore" with seed "$seed" in "$min"min"$sec"s or "$time"s" > "$resultFile"

# Store whole files (logs.txt + best_root.dot + best_stats.md + confMat.txt + bestPolicyStats.md)
echo "Store results in "$pathRes""
mv "$pathExec"build/"$logsFile".txt "$pathRes"/"$logsFile"_"$bestScore".txt
mv "$pathExec"build/out_best.dot "$pathRes"/out_best_"$fileName"_"$bestScore".dot
mv "$pathExec"build/out_best_stats.md "$pathRes"/out_best_stats_"$fileName"_"$bestScore".md
mv "$pathExec"build/bestPolicyStats.md "$pathRes"/bestPolicyStats_"$fileName"_"$bestScore".md
mv "$pathExec"fileClassificationTable.txt "$pathRes"/"$confMatFile"_"$bestScore".txt
