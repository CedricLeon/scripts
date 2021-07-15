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

# Defining paths
path_dataset_origin = sys.argv[1]   # '/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/32x32_balanced/'
path_dataset_arrival = sys.argv[2]  # '/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/32x32_binary/'
store_file = sys.argv[3]            # '/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/AllDtbCompo.txt'

totalNb = 100000
actionsName =  ["NP", "QT", "BTH", "BTV", "TTH", "TTV"]

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

for action in [4]: # 0 1 2 3 4

    # Shuffle files
    np.random.shuffle(fichiers)

    arriveDir = str(path_dataset_arrival+actionsName[action])

    if not os.path.isdir(arriveDir):
        print("Create directory \"", arriveDir, "\"")
        os.mkdir(arriveDir)

    nbMax = totalNb / (len(actionsName) - action)
    print("nbMax : ", nbMax)

    count = [0,0,0,0,0,0]

    # Init index to rename files
    filesCount = 0

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

                # Balance the database
                if split >= action and count[split] < nbMax:
                    shutil.copy(path_dataset_origin + file, arriveDir + "/" + str(filesCount) + ".csv")
                    count[split] += 1
                    filesCount += 1

    total = 0
    for cnt in count:
        total = total + cnt

    lastDir = path_dataset_origin.split('/')[-2]
    dtb = lastDir.replace("_balanced", "")

    print("Database : ", dtb, "_", actionsName[action])
    print("Count : ", count)
    print("Total : ", total)
    print("Copied files : ", filesCount)

    with open(store_file, "a") as file:
        file.write(str(dtb)+"_"+actionsName[action]+" "+str(count)+" "+str(total)+"\n")
