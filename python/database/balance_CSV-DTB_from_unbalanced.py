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
path_dataset_arrival = '/home/cleonard/Data/features/balanced2/' # balanced1

# If balancing the database, Init the nbMax elements of each class
# For "/home/cleonard/Data/features/unbalanced/" min class is "TTH" with 119375 elements
nbMax = 100000

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

                # Only counting
                count[split] += 1

                # Balance the database
                # if count[split] < nbMax:
                #     # Transform row in a string by concatenating each word and a ','
                #     data = ""
                #     for word in row[1:]: # We don't take the first word with corresponds to the "CU" number in the original csv file: no interest
                #         data += word + ','
                #     data = data[:-1]
                #     #print(data)

                #     # Create or overwrite a file and write data in it
                #     file = open(path_dataset_arrival + str(i) + ".csv", "w")
                #     file.write(data)

                #     # Increment the index of copied files
                #     i += 1

print(count)
print(i)
