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

print(bcolors.HEADER + "This script launch a bunch of trainings of TpgVVCPartDatabase for different database. /!\\ Can only be used in specific conditions." + bcolors.ENDC)

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
pathExec        = "/home/cleonard/dev/TpgVvcPartDatabase2/"
pathRes         = "/home/cleonard/dev/stage/results/scripts_results/BinaryFeatures/cascade-full/TaillesDif/ult-script2_BIG/"
pathBalancedDTB = "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/"
execName        = "TPGVVCPartDatabase_binaryFeaturesEnv"
seed            = 0

# Init and open recapitulative files
fileRecapBalancedName = pathBalancedDTB + "Balanced_DTB_Composition.txt"
fileRecapAllScoreName = pathRes + "RecapAllScore.txt"

# Store params.json file
print("\n\nCopy trainings parameters \"params.json\" in " + pathRes + "params.json")
shutil.copy(pathExec + "params.json", pathRes)

# Build and compile the executable once
print(bcolors.HEADER + "Build and compile the executable:" + bcolors.ENDC)
execAndPrintBashCmd("/usr/local/bin/cmake " + pathExec + " -DCMAKE_BUILD_TYPE=Release -DTESTING=1", "")
execAndPrintBashCmd("/usr/local/bin/cmake --build " + pathExec + "build/ --target " + execName + " -- -j 38", "")

# Init fileRecapAllScore
with open(fileRecapAllScoreName, "a") as fileRecapAllScore:
    print("Final results are stored in \"" + fileRecapAllScoreName + "\"")
    fileRecapAllScore.write("Final scores of each training:\n")
    fileRecapAllScore.write("DTB Split Score Generation Time\n")

# Define actions name
actionsName      = ["NP", "QT", "BTH", "BTV", "TTH", "TTV"]
remainingActions = ["{1,2,3,4,5}", "{0,2,3,4,5}", "{0,1,3,4,5}", "{0,1,2,4,5}", "{0,1,2,3,5}", "{0,1,2,3,4}"]

# Every dtb size
#size = np.array(["128x128"]) # For test purposes
size = np.array(["128x128", "64x64", "32x32", "16x16", "8x8", "64x32", "32x64", "64x16", "16x64", "32x16", "16x32", "64x8", "8x64", "32x8", "8x32", "16x8", "8x16", "64x4", "4x64", "32x4", "4x32", "16x4", "4x16", "8x4", "4x8"]) # 25 different dtb

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

trainingNumber = 1

# For every database
for i in range(len(size)):

    # Compute dtb name + result directory name
    dtb = size[i]
    arrivalDir = pathRes + "dtb" + str(i) + "_" + dtb + "/"
    cuHeight = dtb.split("x")[0]
    cuWidth  = dtb.split("x")[1]

    print(bcolors.RED + "\n****************************************************** " + dtb + " ******************************************************" + bcolors.ENDC)

    # Create database specific directory + "all"
    print(bcolors.HEADER + "Create specific database directory and the \"all\" directory" + bcolors.ENDC + bcolors.WARNING)
    os.system("mkdir " + arrivalDir)
    os.system("mkdir " + arrivalDir + "all/")

    # Copy inside params.json
    shutil.copy(pathExec + "params.json", arrivalDir + "all/params.json")

    # Init the recapfile
    resultFile = arrivalDir + "recapScore.log"
    with open(resultFile, "w") as file:
        file.write("Final scores of each training :\n")

    # For each available splits for this dtb: launch one training
    for j in range(len(availableSplitsDict[dtb])):

        # ------- Time this single training -------
        startTime = time.time()

        # ------- Define split, split name, dtb path and results file names -------
        act         = availableSplitsDict[dtb][j]
        actName     = actionsName[act]
        logsFile    = "logs_ent"        + str(j) +"_b" + actName
        confMatFile = "confMat_ent"     + str(j) +"_b" + actName
        fullconfMat = "FullConfMat_ent" + str(j) +"_b" + actName
        dtbPath     = pathBalancedDTB + dtb + "_binary-50%/"

        # ------- Print which training is starting -------
        print(bcolors.ENDC + bcolors.CYAN + "    --------------- Training N°" + str(trainingNumber) + ": " + actName + " ---------------" + bcolors.ENDC)

        # ------- Get nbDatabaseElements from "Balanced_DTB_Composition.txt" -------
        nbDtbElements = -1
        with open(fileRecapBalancedName, "r") as file:
            for line in file:
                if re.search("^" + dtb + "_" + actName, line):
                    print("    Database composition: \"" + bcolors.GREEN + line[:-1] + bcolors.ENDC + "\"")
                    words = line.split(' ')
                    nbDtbElements = int(words[-1][:-1])
                    #print("    Total elements in the database: " + bcolors.GREEN + str(nbDtbElements) + bcolors.ENDC)

        # ------- Start the training -------
        print(bcolors.HEADER + "    Launch training and redirect logs in " + logsFile + ".log:" + bcolors.ENDC)
        execAndPrintBashCmd(pathExec +"build/" + execName +
                               " \"{" + str(act) + "}\"" +
                               " \"" + remainingActions[act] + "\"" +
                               " \"" + str(seed) + "\"" +
                               " \"" + cuHeight  + "\"" +
                               " \"" + cuWidth   + "\"" +
                               " \"" + str(nbFeaturesDict[dtb]) + "\"" +
                               " \"" + str(nbDtbElements) + "\"" +
                               " " + actName +
                               " " + dtbPath + " 0 > " + pathExec + "build/" + logsFile + ".log", "    ")

        # ------- Look for best score and generation in the confusion matrix -------
        print(bcolors.HEADER + "\n    Look for best score and generation in confusion matrix:" + bcolors.ENDC + bcolors.WARNING)
        # Get every scores of the file, sort them
        os.system("cat " + pathExec + "fileClassificationTable.txt | grep -o '[0-9]*\\.[0-9]*$' | sort -n > everyScore.txt")
        # Get last score, after the sort: the higher <=> the best
        os.system("cat everyScore.txt | perl -ne 'print if eof' | grep -o '[0-9]*\\.[0-9]*$' > bestScore.txt")
        os.system("rm everyScore.txt")
        # Get bestScore from temporary file
        bestScore = -1.0
        with open("bestScore.txt", "r") as file:
            for line in file:
                bestScore = float(line)
                #print(bestScore)
        os.system("rm bestScore.txt")
        # Get best generation number from bestScore
        execAndPrintBashCmd("cat " + pathExec + "fileClassificationTable.txt | grep " + str(bestScore) + " | grep -o '^\\s*[0-9]*' | sort -n | perl -ne 'print if eof' | grep -o '[0-9]*$' > genBestScore.txt", "    ")
        genBestScore = -1
        with open("genBestScore.txt", "r") as file:
            for line in file:
                genBestScore = int(line)
                #print(genBestScore)
        os.system("rm genBestScore.txt")

        # ------- Replace . with , (Libre Office Calc usage) -------
        bestScore = str(bestScore).replace(".", ",")

        # ------- Time this training -------
        endTime = int(time.time() - startTime)

        # ------- Store results in the recap file -------
        with open(resultFile, "a") as file:
            results = str(act) + " " + remainingActions[act] + " " + str(endTime) + " " + str(genBestScore) + " " + bestScore + "\n"
            print(bcolors.ENDC + bcolors.GREEN + "    " + results + bcolors.ENDC)
            file.write(results)

        # ------- Store results in the overall recap file -------
        with open(fileRecapAllScoreName, "a") as fileRecapAllScore:
            fileRecapAllScore.write(dtb + "_" + actName + " " + bestScore + " " + str(genBestScore) + " " +  str(endTime) + "\n")

        # ------- Move every results files in pathRes (logs, best stats, etc.) -------
        print(bcolors.HEADER + "    Store results in " + arrivalDir + actName + "/" + bcolors.ENDC + bcolors.WARNING)
        # Create action directory
        os.system("mkdir " + arrivalDir + actName)
        # logs.log
        os.system("mv " + pathExec + "build/" + logsFile + ".log " + arrivalDir + actName + "/" + logsFile + "_" + bestScore + ".log")
        # bestStats
        os.system("mv " + pathExec + "build/out_best_stats.md " + arrivalDir + actName + "/out_best_stats_ent" + str(trainingNumber) + "_b" + actName + "_" + bestScore + ".md")
        # TPG (.dot)
        tpgFileName = arrivalDir + actName + "/out_best_last_ent" + str(trainingNumber) + "_b" + actName + "_" + bestScore + ".dot"
        execAndPrintBashCmd("mv " + pathExec + "build/out_best.dot " + tpgFileName, "    ")
        # Special Policy stats
        os.system("mv " + pathExec + "build/bestPolicyStats.md " + arrivalDir + actName + "/bestPolicyStats_ent" + str(trainingNumber) + "_b" + actName + "_" + bestScore + ".md")
        # Confusion matrix
        os.system("mv " + pathExec + "fileClassificationTable.txt " + arrivalDir + actName + "/" + confMatFile + "_" + bestScore + ".txt")
        # Full Confusion matrix
        os.system("mv " + pathExec + "fullClassifTable.txt " + arrivalDir + actName + "/" + fullconfMat + "_" + bestScore + ".txt")


        # ------- Copy .dot file for all/ directory -------
        #print(bcolors.ENDC + "    Copy .dot file: " + bcolors.BLUE + "mv " + tpgFileName + " " + arrivalDir + "all/" + actName + ".dot" + bcolors.ENDC + bcolors.WARNING)
        shutil.copy(tpgFileName, arrivalDir + "all/" + actName + ".dot")

        # ------- Print training time -------
        print(bcolors.ENDC + "    This training last:")
        printHumanTimeFromSeconds(endTime, "    ")
        print("")

        # ------- Go to next training -------
        trainingNumber += 1


    # ------- Complete all/ directory with the final scores file -------
    print("  Copy recapScore file: " + bcolors.BLUE + "mv " + resultFile + " " + arrivalDir + "all/recapScore.log" + bcolors.ENDC)
    shutil.copy(resultFile, arrivalDir + "all/recapScore.log")

    # Jump one line in overall recap file between databases
    with open(fileRecapAllScoreName, "a") as fileRecapAllScore:
        fileRecapAllScore.write("\n")

# Print total time
print("The script went on for: ")
printHumanTimeFromSeconds(round(time.time() - veryStartTime), "")
