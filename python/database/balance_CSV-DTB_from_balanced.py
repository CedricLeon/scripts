import sys
import numpy as np
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil
import csv
import time

# Defining paths
path_dataset_origin = '/home/cleonard/Data/features/balanced1/' # unbalanced
path_dataset_arrival = '/home/cleonard/Data/features/balanced1/' # balanced1

# If balancing the database, Init the nbMax elements of each class
# For "/home/cleonard/Data/features/unbalanced/" min class is "TTH" with 119375 elements
nbMax = 2

# Picking every file
fichiers = [f for f in listdir(path_dataset_origin) if isfile(join(path_dataset_origin, f))]

# Shuffle files
np.random.shuffle(fichiers)
count = [0,0,0,0,0,0]

# Init index to rename files
i = 0

for file in tqdm(fichiers):

    # Open each file in the repertory
    with open(path_dataset_origin+file) as csv_file:

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

            # Only counting
            count[split] += 1

print(count)
print(i)
