import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil

# Defining paths
path_dataset_origin = '/home/cleonard/Data/binary_datasets/balanced_BTV_dataset/' #'/home/cleonard/Data/dataset_tpg_balanced/dataset_tpg_32x32_27_balanced2/'
path_dataset_arrival = '/home/cleonard/Data/binary_datasets/tmp/'

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

# Shuffle files
np.random.shuffle(fichiers)
count = [0,0,0,0,0,0]

# Which split is being targeted
# whichSplit = 5
# print(whichSplit)

for file in tqdm(fichiers):
    # Reading the split
    bin_file = open(path_dataset_origin+file,'rb')
    bin_file.read(1024)
    split = int.from_bytes(bin_file.read(1),'big')

    # Only counting:
    count[split] +=1

    # Copying every same split:
    # if split == whichSplit:
    #     count[split] += 1
    #     shutil.copy(path_dataset_origin+file,path_dataset_arrival)

    # Copying every other split in a limited quantity:
    # if split != whichSplit:
    #     if count[split] < 11000:
    #         count[split] += 1
    #         shutil.copy(path_dataset_origin+file,path_dataset_arrival)

print(count)
