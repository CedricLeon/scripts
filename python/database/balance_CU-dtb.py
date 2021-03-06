import sys
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import shutil

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

print(bcolors.HEADER + "This script is used to balance a database of CU (.bin files). /!\\ May not be up to date." + bcolors.ENDC)

# Defining paths
path_dataset_origin = '/media/cleonard/alex/cedric_TPG-VVC/CU_datasets/dataset_tpg_32x32_27/'
path_dataset_arrival = '/home/cleonard/Data/CU/CU_32x32_balanced/'

print("Origin Database  :", path_dataset_origin)
print("Arrival Database :", path_dataset_arrival)

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

# Shuffle files
np.random.shuffle(fichiers)
count = [0,0,0,0,0,0]

# Total number of file per class
totalNb = 70000
# Init index to rename files
filesCount = 0

for file in tqdm(fichiers):
    # Reading the split
    with open(path_dataset_origin + file, 'rb') as bin_file:
        bin_file.read(1024) # Last Byte
        split = int.from_bytes(bin_file.read(1), 'big') # BigEndian
    # bin_file.close()

    # Copying the file only if there isn't already totalNb files of this class
    if count[split] < totalNb:
        # print("Origin :", path_dataset_origin + file)
        # print("Arrival :", path_dataset_arrival + str(filesCount) + ".bin")
        shutil.copyfile(path_dataset_origin + file, path_dataset_arrival + str(filesCount) + ".bin")
        count[split] += 1
        filesCount += 1

total = 0
for cnt in count:
    total = total + cnt

print("Count :", count)
print("Total :", total)
print("Copied files :", filesCount)
