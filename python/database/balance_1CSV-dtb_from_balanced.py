import sys
import os
import numpy as np
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil
import csv
import time
import re
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.HEADER + "This script is used to create a directory owning different databases with 50% of one class and last 50% equalized between others available classes for this dtb. Please check full_DTB_management.py for it's full usage." + bcolors.ENDC)

print("Example: python3.6 /home/cleonard/dev/stage/scripts/python/database/balance_1CSV-dtb_from_balanced.py /media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/64x64_balanced/ /home/cleonard/Data/BinaryFeatures/64x64_binary-50%/ /media/cleonard/alex/cedric_TPG-VVC/AllDtbCompo.txt")

# Defining paths
path_dataset_origin  = sys.argv[1]  # "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/32x32_balanced/"
path_dataset_arrival = sys.argv[2]  # "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/32x32_binary/"
store_file           = sys.argv[3]  # "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/AllDtbCompo.txt"
availableSplitsStr   = sys.argv[4]  # "[0, 1, 2, 3, 4, 5]"

# Create arrival directory if it doesn't exist (/!\ DOESN'T EMPTY IT ELSE)

dtb = path_dataset_origin.split("/")[-2].split("_")[0]

path_dataset_arrival = str(path_dataset_arrival + dtb + "_binary-50%/")
if not os.path.isdir(path_dataset_arrival):
    print("Create directory \"", path_dataset_arrival, "\"")
    os.mkdir(path_dataset_arrival)

# print("path_dataset_origin: ", path_dataset_origin)
# print("path_dataset_arrival:", path_dataset_arrival)

# If balancing the database, Init the min elements of each class
# For "/home/cleonard/Data/features/unbalanced/" min class is "TTH" with 119375 elements

total = -1
nbMin = math.inf

with open(store_file, "r") as file:
    for line in file:
        if re.search(dtb + "_balanced", line):

            print(line)
            words = line.split(' ')
            total = words[-1]
            words = words[1:]
            words = words[:-1]
            #print(words)

            for w in words:
                if w: # Check if w isn't empty
                    w = w.replace("[", "")
                    w = w.replace(",", "")
                    w = w.replace("]", "")
                    #print(w)
                    if int(w) != 0 and nbMin > int(w):
                        nbMin = int(w)

totalNb = nbMin * 2
if totalNb > 100000:
    totalNb = 100000

# Get available splits
availableSplits = []
#print("Available splits String:", availableSplitsStr)
availableSplitsStr = availableSplitsStr.replace("[", "")
availableSplitsStr = availableSplitsStr.replace(",", "")
availableSplitsStr = availableSplitsStr.replace("]", "")
splits             = availableSplitsStr.split(' ')

for s in splits:
    availableSplits.append(int(s))
print(bcolors.OKGREEN + "Available splits: " + str(availableSplits) + bcolors.ENDC)

nbActions = len(availableSplits)

print("Min: " + str(nbMin) + ", nbActions: " + str(nbActions))
#print("Total files in the   balanced DTB :", int(total[:-1]))
#print("Total files in the binary-50% DTB :", totalNb)

actionsName =  ["NP", "QT", "BTH", "BTV", "TTH", "TTV"]

# Pick every file
#print("Picking every file in", path_dataset_origin)
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

for action in availableSplits: # [0, 1, 2, 3, 4, 5]

    print("\nStarting the", actionsName[action], "database")

    # Shuffle files
    np.random.shuffle(fichiers)

    # Create arrival directory if it doesn't exist (/!\ DOESN'T EMPTY IT ELSE)
    arriveDir = str(path_dataset_arrival+actionsName[action])
    if not os.path.isdir(arriveDir):
        print("Create directory \"", arriveDir, "\"")
        os.mkdir(arriveDir)

    # # For a sink database
    # nbMax = totalNb / (len(actionsName) - action)
    # print("nbMax : ", nbMax)
    # For 50% database :
    if action not in availableSplits:
        nbMain = 0
        nbOther = totalNb / nbActions
    else:
        nbMain  = int(totalNb / 2)                                   # 50 000
        nbOther = int((totalNb - nbMain) / (nbActions - 1))          # 10 000
    print("nbMain: " + str(nbMain) + ", nbOther: " + str(nbOther))

    # Init count and index to rename files
    count = [0,0,0,0,0,0]
    copiedFiles = 0

    # Browse files
    for file in tqdm(fichiers):

        # Open each file in the repertory
        with open(path_dataset_origin+file) as csv_file:

            # Open the file as a .csv and specify the delimiter
            csv_reader = csv.reader(csv_file, delimiter=',')

            # ... There is only 1 row whatever
            for row in csv_reader:
                # Get the split name
                splitString = row[1]

                # Deduce split number
                if splitString == "NS":
                    split = 0;
                elif splitString == "QT":
                    split = 1;
                elif splitString == "BTH":
                    split = 2;
                elif splitString == "BTV":
                    split = 3;
                elif splitString == "TTH":
                    split = 4;
                elif splitString == "TTV":
                    split = 5;
                else:
                    print("WTF : ", splitString)
                    sys.exit("Unknown split name in : ", csv_file)

                # # SINK: Balance the database
                # if split >= action and count[split] < nbMax:
                #     shutil.copy(path_dataset_origin + file, arriveDir + "/" + str(copiedFiles) + ".csv")
                #     count[split] += 1
                #     copiedFiles += 1

                # 50%: Balance the database
                if (split != action and count[split] < nbOther) or (split == action and count[split] < nbMain):
                    shutil.copy(path_dataset_origin + file, arriveDir + "/" + str(copiedFiles) + ".csv")
                    count[split] += 1
                    copiedFiles += 1

    total = 0
    for cnt in count:
        total = total + cnt

    lastDir = path_dataset_origin.split('/')[-2]
    dtb = lastDir.replace("_balanced", "")

    #print("Database:", dtb + "_" + actionsName[action])

    check = bcolors.OKGREEN
    if copiedFiles != total:
        check = bcolors.WARNING

    print("Count: " + str(count) + ", total: " + check + str(total) + bcolors.ENDC + " Copied files: " + check + str(copiedFiles) + bcolors.ENDC)

    with open(store_file, "a") as file:
        file.write(str(dtb)+"_"+actionsName[action]+" "+str(count)+" "+str(total)+"\n")

with open(store_file, "a") as file:
        file.write("\n")
