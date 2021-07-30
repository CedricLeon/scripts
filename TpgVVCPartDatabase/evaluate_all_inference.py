import sys
import os
import shutil
import time
import re
import numpy as np

# Define console logs colors
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

print(bcolors.HEADER + "This script is used to evaluate in inference every set of TPGs trained with launch_all_trainings.py. /!\\ Can only be used in specific conditions." + bcolors.ENDC)


# Create MACRO to execute bash commands adn print it in stdout
def execAndPrintBashCmd(cmd, spaces):
    print(bcolors.BLUE + spaces + cmd + bcolors.ENDC)
    os.system(cmd)

# Define a function to print a time from seconds to human redable format
def printHumanTimeFromSeconds(value, spaces):
    valueD  = (((value/60)/60)/24)
    Days    = int(valueD)
    valueH  = (valueD-Days)*24
    Hours   = int(valueH)
    valueM  = (valueH - Hours)*60
    Minutes = int(valueM)
    valueS  = (valueM - Minutes)*60
    Seconds = int(valueS)
    print(bcolors.CYAN + spaces + str(Days) + " days, " + str(Hours) + "h " + str(Minutes) + "min " + str(Seconds) + "s" + bcolors.ENDC)

# Time the whole script
veryStartTime = time.time()

# Init main arguments
pathExec         = "/home/cleonard/dev/TpgVvcPartDatabase/"
pathRes          = "/home/cleonard/dev/stage/results/scripts_results/BinaryFeatures/cascade-full/TaillesDif/ult-script1/"
pathBalancedDTB  = "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/"
execName         = "TPGVVCPartDatabase_inferenceBinaryFeatures"
seed             = 0
nbEvaluation     = 50

# Init and open recapitulative files
fileRecapBalancedName          = pathBalancedDTB + "Balanced_DTB_Composition.txt"
fileRecapAllScoreInferenceName = pathRes + "RecapAllInferenceEvaluations.txt"
singleResultInferenceFilename  = pathExec + "build/" + "InferenceRecapFile.log"

# Build and compile the executable once
print(bcolors.HEADER + "\n\nBuild and compile the executable:" + bcolors.ENDC)
execAndPrintBashCmd("/usr/local/bin/cmake " + pathExec + " -DCMAKE_BUILD_TYPE=Release -DTESTING=1", "")
execAndPrintBashCmd("/usr/local/bin/cmake --build " + pathExec + "build/ --target " + execName + " -- -j 38", "")

# Init fileRecapAllScore
with open(fileRecapAllScoreInferenceName, "a") as file:
    print("Inference scores are stored in \"" + fileRecapAllScoreInferenceName + "\"")
    file.write("Inference scores of BinaryFeatures TPGs:\n\n")
    file.write("DTB Score(%) NbMoySplits\n")

# Every dtb size
#size = np.array(["32x64", "64x16", "16x64", "32x16", "16x32", "64x8", "8x64", "32x8", "8x32", "16x8"]) # For test purposes
size = np.array(["128x128", "64x64", "32x32", "16x16", "8x8", "64x32", "32x64", "64x16", "16x64", "32x16", "16x32", "64x8", "8x64", "32x8", "8x32", "16x8", "8x16", "64x4", "4x64", "32x4", "4x32", "16x4", "4x16", "8x4", "4x8"]) # 25 different dtb (DO NOT SWITH ORDER)

# For each dtb, how many CNN features does a single .csv file own ?
nbFeaturesDict = {        "4x8" : 1,    "4x16" : 3,    "4x32" : 7,   "4x64" : 14,
             "8x4" : 1,   "8x8" : 4,   "8x16" : 10,   "8x32" : 22,   "8x64" : 46,
            "16x4" : 3, "16x8" : 10,  "16x16" : 24,  "16x32" : 52, "16x64" : 108,
            "32x4" : 7, "32x8" : 22,  "32x16" : 52, "32x32" : 112, "32x64" : 232,
           "64x4" : 14, "64x8" : 46, "64x16" : 108, "64x32" : 232, "64x64" : 480,
           "128x128" : 1984 }

# For each dtb, which splits are available ?
availableSplitsDict = {            "4x8" : [0, 3],            "4x16" : [0, 3, 5],           "4x32" : [0, 3, 5],           "4x64" : [0, 3, 5],
            "8x4" : [0, 2],     "8x8" : [0, 2, 3],         "8x16" : [0, 2, 3, 5],        "8x32" : [0, 2, 3, 5],        "8x64" : [0, 2, 3, 5],
        "16x4" : [0, 2, 4], "16x8" : [0, 2, 3, 4],  "16x16" : [0, 1, 2, 3, 4, 5],    "16x32" : [0, 2, 3, 4, 5],    "16x64" : [0, 2, 3, 4, 5],
        "32x4" : [0, 2, 4], "32x8" : [0, 2, 3, 4],     "32x16" : [0, 2, 3, 4, 5], "32x32" : [0, 1, 2, 3, 4, 5],    "32x64" : [0, 2, 3, 4, 5],
        "64x4" : [0, 2, 4], "64x8" : [0, 2, 3, 4],     "64x16" : [0, 2, 3, 4, 5],    "64x32" : [0, 2, 3, 4, 5], "64x64" : [0, 1, 2, 3, 4, 5],
        "128x128" : [0, 1] }

# For every database
for i in range(17, 18): # len(size)

    # Time the inference test
    startTime = time.time()

    # Compute dtb name + result directory name
    dtb = size[i]
    arrivalDir = pathRes + "dtb" + str(i) + "_" + dtb + "/"
    cuHeight = dtb.split("x")[0]
    cuWidth  = dtb.split("x")[1]

    print(bcolors.RED + "\n****************************************************** " + dtb + " ******************************************************" + bcolors.ENDC)

    # Delete old TPGs files in the pathExec dir
    print(bcolors.HEADER + "  Delete old TPGs files" + bcolors.ENDC)
    execAndPrintBashCmd("rm " + pathExec + "TPG/*", "  ")

    # Copy new TPGs files in the pathExec dir
    print(bcolors.HEADER + "  Copy new TPGs files" + bcolors.ENDC)
    execAndPrintBashCmd("cp " + arrivalDir + "all/* " + pathExec + "TPG/", "  ")

    # ------- Get nbDatabaseElements from "Balanced_DTB_Composition.txt" -------
    nbDtbElements = -1
    with open(fileRecapBalancedName, "r") as file:
        for line in file:
            if re.search("^" + dtb + "_balanced", line):
                print("  Database composition: \"" + bcolors.GREEN + line[:-1] + bcolors.ENDC + "\"")
                words = line.split(' ')
                nbDtbElements = int(words[-1][:-1])
                #print("  Total elements in the database: " + bcolors.GREEN + str(nbDtbElements) + bcolors.ENDC)

    # Run the inference test
    execAndPrintBashCmd(pathExec +"build/" + execName +
                        " \"" + str(availableSplitsDict[dtb]) + "\"" +
                        " \"" + str(seed)                     + "\"" +
                        " \"" + cuHeight                      + "\"" +
                        " \"" + cuWidth                       + "\"" +
                        " \"" + str(nbFeaturesDict[dtb])      + "\"" +
                        " \"" + str(nbDtbElements)            + "\"" +
                        " \"" + str(nbEvaluation)             + "\"", "  ")
    # Get results
    scoreMoy = -1
    nbSplitsMoy = -1
    with open(singleResultInferenceFilename, "r") as file:
        for line in file:
            print(line)
            words = line.split(" ")
            scoreMoy = words[0]
            nbSplitsMoy = words[1]

    scoreMoy = float(scoreMoy)/10
    print("  ScoreMoy: " + bcolors.GREEN + str(scoreMoy) + "%" + bcolors.ENDC + ", NbSplitsMoy: " + bcolors.GREEN + nbSplitsMoy + bcolors.ENDC)

    # Delete the old singleResultInferenceFilename
    execAndPrintBashCmd("rm " + singleResultInferenceFilename, "  ")

    # Store it in the main recap file
    print("  Store result in the main recap file")
    with open(fileRecapAllScoreInferenceName, "a") as file:
        file.write(dtb + " " + str(scoreMoy) + " " + nbSplitsMoy)

    # ------- Time this training -------
    endTime = int(time.time() - startTime)

    # ------- Print training time -------
    print(bcolors.ENDC + "    This training last:")
    printHumanTimeFromSeconds(endTime, "    ")
    print("")

# Print total time
print("The script went on for: ")
printHumanTimeFromSeconds(round(time.time() - veryStartTime), "")
