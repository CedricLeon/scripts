import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil

# Defining paths
path_dataset_origin = '/home/cleonard/Data/binary_datasets/'
#'/home/cleonard/Data/dataset_tpg_balanced/dataset_tpg_32x32_27_balanced2/'

other_dataset = ["NP_dataset/","QT_dataset/","BTH_dataset/","BTV_dataset/","TTH_dataset/","TTV_dataset/"]
#other_dataset = ["QT_dataset/"]

for dataset_name in other_dataset:

    # Which dataset ?
    path = path_dataset_origin+dataset_name
    print(path)

    # Picking every file
    fichiers = [f for f in listdir(path) if isfile(join(path, f))]

    count = [0,0,0,0,0,0]

    for file in tqdm(fichiers):
        # Reading the split
        bin_file = open(path+file,'rb')
        bin_file.read(1024)
        split = int.from_bytes(bin_file.read(1),'big')

        # Only counting:
        count[split] +=1
    print(count)