import sys
import numpy as np
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil
import csv
import time
import re

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

print(bcolors.HEADER + "This script is used to count the classes repartition of a database containing files with features for 10 CUs. Please check full_DTB_management.py for it's full usage." + bcolors.ENDC)
# Defining paths
path_dataset_origin = sys.argv[1]   # '/home/cleonard/Data/features/32x32_unbalanced/'

storeResult = 1
if storeResult:
    store_file = sys.argv[2]        # '/media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/AllDtbCompo.txt'

dtb = path_dataset_origin.split('/')[-2]

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

# Init count
count = [0,0,0,0,0,0]

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

                # Only counting
                count[split] += 1

total = 0
for cnt in count:
    total = total + cnt

# print("Database : ", dtb)
print("Count:", count, total)

if storeResult:
    with open(store_file, "a") as file:
        file.write(str(dtb)+" "+str(count)+" "+str(total)+"\n")
