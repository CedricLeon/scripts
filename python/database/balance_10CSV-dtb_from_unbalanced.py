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

print(bcolors.HEADER + "This script is used to balance a database of .csv files owning features for 10 CUs. Please check full_DTB_management.py for it's full usage." + bcolors.ENDC)

print("Example: python3.6 /home/cleonard/dev/stage/scripts/python/database/balance_10CSV-dtb_from_unbalanced.py /media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/32x64/ /media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/ /media/cleonard/alex/cedric_TPG-VVC/Composition_unbalanced_dtb.txt /media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/AllDtbCompo.txt")

# Defining paths
path_dataset_origin  = sys.argv[1]  # '/home/cleonard/Data/features/32x32_unbalanced/'
path_dataset_arrival = sys.argv[2]  # '/home/cleonard/Data/features/balanced2/'
recap_file = sys.argv[3]            # '/media/cleonard/alex/cedric_TPG-VVC/Composition_unbalanced_dtb.txt'
store_file = sys.argv[4]            # '/media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/AllDtbCompo.txt'

# Create arrival directory if it doesn't exist (/!\ DOESN'T EMPTY IT ELSE)
path_dataset_arrival = str(path_dataset_arrival + path_dataset_origin.split("/")[-2] + "_balanced/")
if not os.path.isdir(path_dataset_arrival):
    print("Create directory \"", path_dataset_arrival, "\"")
    os.mkdir(path_dataset_arrival)

# Get dtb name
dtb = path_dataset_origin.split('/')[-2]

# Init the min elements of each class
# For "/home/cleonard/Data/features/unbalanced/" min class is "TTH" with 119375 elements
nbCus = np.array([])
with open(recap_file, "r") as file:
    for line in file:
        if re.search(dtb, line):
            # Get CUs repartition (avoid dtb_name and total)
            words = line.split(' ')
            words = words[1:]
            words = words[:-1]

            # Avoid nbFeatures in the count
            i = 0
            for w in words:
                if w and w[0] == "[":
                    words = words[i:]
                    break
                i += 1

            for w in words:
                w = w.replace("[", "")
                w = w.replace(",", "")
                w = w.replace("]", "")
                nbCus = np.append(nbCus, int(w))

# Compute min and print it
min = int(min(nbCus[ nbCus != 0 ]))
print(str(nbCus) + bcolors.OKCYAN + " Min: " + str(min) + bcolors.ENDC)

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

# Shuffle files
np.random.shuffle(fichiers)
count = [0,0,0,0,0,0]

# Init index to rename files
copiedFiles = 0

# Browse files
for file in tqdm(fichiers):

    # Open each file in the repertory
    with open(path_dataset_origin+file) as csv_file:

        # Open the file as a .csv and specify the delimiter
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Count which line we are (needed to avoid computing the first line)
        line_count = 0

        for row in csv_reader:
            # Avoid first line (contain column names)
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1

                # Get the split name
                splitString = row[2]

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
                    sys.exit("Unknown split name in : ", csv_file, ", at line ", line_count)

                # Balance the database
                if count[split] < min:
                    # Transform row in a string by concatenating each word and a ','
                    data = ""
                    for word in row[1:]: # We don't take the first word wich corresponds to the "CU" number in the original csv file: no interest
                        data += word + ','
                    data = data[:-1]

                    # Create or overwrite a file and write data in it
                    arrivalFile = path_dataset_arrival + str(copiedFiles) + ".csv"
                    file = open(arrivalFile, "w")
                    file.write(data)

                    # Increment the index of copied files
                    count[split] += 1
                    copiedFiles += 1

# Compute Total and check if there is as much copied files as expected
total = 0
for cnt in count:
    total = total + cnt

check = bcolors.OKGREEN
if copiedFiles != total:
    check = bcolors.WARNING

# Print and store results
print("Count: " + str(count) + ", total: " + check + str(total) + bcolors.ENDC + " Copied files: " + check + str(copiedFiles) + bcolors.ENDC)
with open(store_file, "a") as file:
    file.write(str(dtb)+"_balanced"+" "+str(count)+" "+str(total)+"\n\n")
