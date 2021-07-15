import sys
import numpy as np
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import shutil
import csv
import time
import re

# Defining paths
path_dataset_origin = sys.argv[1]   # '/home/cleonard/Data/features/32x32_unbalanced/'
path_dataset_arrival = sys.argv[2]  # '/home/cleonard/Data/features/balanced2/'
recap_file = sys.argv[3]            # '/media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/AllDtbCompo.txt'

# If balancing the database, Init the nbMax elements of each class
# For "/home/cleonard/Data/features/unbalanced/" min class is "TTH" with 119375 elements
dtb = path_dataset_origin.split('/')[-2]

with open(recap_file, "r") as file:
    for line in file:
        if re.search(dtb, line):

            words = line.split(' ')
            words = words[1:]
            words = words[:-1]
            print(words)

            nbMax = 1
            for w in words:
                if w: # Check if w isn't empty
                    w = w.replace("[", "")
                    w = w.replace(",", "")
                    w = w.replace("]", "")
                    print(w)
                    if nbMax == 1 or nbMax > int(w):
                        nbMax = int(w)

print("Min :", nbMax)

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

                count[split] += 1

                # Balance the database
                if count[split] < nbMax:
                    # Transform row in a string by concatenating each word and a ','
                    data = ""
                    for word in row[1:]: # We don't take the first word wich corresponds to the "CU" number in the original csv file: no interest
                        data += word + ','
                    data = data[:-1]
                    #print(data)

                    # Create or overwrite a file and write data in it
                    file = open(path_dataset_arrival + str(i) + ".csv", "w")
                    file.write(data)

                    # Increment the index of copied files
                    i += 1

total = 0
for cnt in count:
    total = total + cnt

print("Database : ", dtb)
print("Count : ", count)
print("Total : ", total)
print("Copied files : ", i)

with open(store_file, "a") as file:
    file.write(str(dtb)+" "+str(count)+" "+str(total)+"\n")
