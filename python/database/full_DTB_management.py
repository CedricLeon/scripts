import sys
import os
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'

print(bcolors.HEADER + "This script unzip, count, balance and create personnnalized datasets for a set of databases. /!\\ Can only be used in specific conditions and with other specific scripts. Please check count_10CSV-dtb.py, balance_10CSV-dtb_from_unbalanced.py and balance_1CSV-dtb_from_balanced.py." + bcolors.ENDC)

# Init scripts
pathExec = "/home/cleonard/dev/stage/scripts/python/database/"
script1  = pathExec + "count_10CSV-dtb.py"
script2  = pathExec + "balance_10CSV-dtb_from_unbalanced.py"
script3  = pathExec + "balance_1CSV-dtb_from_balanced.py"

# Init absolute paths
path_zip        = "/media/cleonard/alex/inter_data_zip/"
path_unbalanced = "/media/cleonard/alex/cedric_TPG-VVC/unbalanced_datasets/"
path_balanced   = "/media/cleonard/alex/cedric_TPG-VVC/balanced_datasets/"

# Init and open recapitulative files
fileRecapUnbalancedName = path_unbalanced + "Unbalanced_DTB_Composition.txt"
fileRecapBalancedName   = path_balanced   + "Balanced_DTB_Composition.txt"
fileRecapUnbalanced     = open(fileRecapUnbalancedName, "w")
fileRecapBalanced       = open(fileRecapBalancedName,   "w")

# Init fileRecapUnbalanced
print("Composition summary of every CU features database from A.Tissier.\n Each database is composed of files owning 10 different CUs, this array resume the number of CUs in function of their optimal split (VTM groundtruth).\n", file = fileRecapUnbalanced)

#size = np.array(["4x8"]) # for test purposes
size = np.array(["4x8", "4x16", "4x32", "4x64", "8x4", "8x8", "8x16", "8x32", "8x64", "16x4", "16x8", "16x16", "16x32", "16x64", "32x4", "32x8", "32x16", "32x32", "32x64", "64x4", "64x8", "64x16", "64x32", "64x64", "128x128"])

#                       4   8   16   32   64
nbFeatures = np.array([     1,   3,   7,  14,      #  4x?
                        1,  4,  10,  22,  46,      #  8x?
                        3, 10,  24,  52, 108,      # 16x?
                        7, 22,  52, 112, 232,      # 32x?
                       14, 46, 108, 232, 480,      # 64x?
                       1984 # 128x128
                     ])

#                                 ?x4           ?x8                ?x16                ?x32                ?x64
availableSplits = np.array([
                                             [0, 3],          [0, 3, 5],          [0, 3, 5],          [0, 3, 5],      #  4x?
                               [0, 2],    [0, 2, 3],       [0, 2, 3, 5],       [0, 2, 3, 5],       [0, 2, 3, 5],      #  8x?
                            [0, 2, 4], [0, 2, 3, 4], [0, 1, 2, 3, 4, 5],    [0, 2, 3, 4, 5],    [0, 2, 3, 4, 5],      # 16x?
                            [0, 2, 4], [0, 2, 3, 4],    [0, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5],    [0, 2, 3, 4, 5],      # 32x?
                            [0, 2, 4], [0, 2, 3, 4],    [0, 2, 3, 4, 5],    [0, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5],      # 64x?
                            [0, 1]], # 128x128
                           dtype=object)

for i in range(len(size)): # range(len(size))

    print(bcolors.RED + "******************************************************* " + size[i] + " *******************************************************" + bcolors.ENDC)

    # ------------ Initialise paths and names ------------
    zippedDTB     = path_zip        + size[i] + ".zip"
    unbalancedDTB = path_unbalanced + size[i] + "/"
    balancedDTB   = path_balanced   + size[i] + "_balanced/"

    print(bcolors.HEADER + "Paths:" + bcolors.ENDC)
    print("DTB zipped:     " + zippedDTB)
    print("DTB unbalanced: " + unbalancedDTB)
    print("DTB balanced:   " + balancedDTB + "\n")

    # ------------ Create unbalanced by unzipping ------------
    print(bcolors.HEADER + "--- Unzip " + size[i] + " (overwrite \"-o\", silently \"-q\"): ---" + bcolors.ENDC)
    print(bcolors.BLUE + "unzip -oq " + zippedDTB + " -d " + path_unbalanced + bcolors.ENDC)
    os.system("unzip -oq " + zippedDTB + " -d " + path_unbalanced)
    print("")

    # ------------ Count unbalanced and store result ------------
    print(bcolors.HEADER + "--- Count unbalanced " + size[i] + " : ---" + bcolors.ENDC)
    print(bcolors.BLUE + "python3.6 " + script1 + " " + unbalancedDTB + " " + fileRecapUnbalancedName + bcolors.ENDC)
    os.system("python3.6 " + script1 + " " + unbalancedDTB + " " + fileRecapUnbalancedName)
    print("")

    # Init fileRecapBalanced for this DTB
    print("------------ " + size[i] + " ------------", file = fileRecapBalanced)

    # ------------ Balanced the original database ------------
    print(bcolors.HEADER + "--- Create Balanced " + size[i] + " : ---" + bcolors.ENDC)
    print(bcolors.BLUE + "python3.6 " + script2 + " " + unbalancedDTB + " " + path_balanced + " " + fileRecapUnbalancedName + " " + fileRecapBalancedName + bcolors.ENDC)
    os.system("python3.6 " + script2 + " " + unbalancedDTB + " " + path_balanced + " " + fileRecapUnbalancedName + " " + fileRecapBalancedName)
    print("")

    print("\n", file = fileRecapBalanced)

    # ------------ From balance, create the 50%_balanced_DTB ------------
    print(bcolors.HEADER + "--- Create " + str(len(availableSplits[i])) + " 50 DTBs for " + size[i] + " : ---" + bcolors.ENDC)
    print(bcolors.BLUE + "python3.6 " + script3 + " " + balancedDTB + " " + path_balanced + " " + fileRecapBalancedName + " \"" + str(availableSplits[i]) + "\"" + bcolors.ENDC)
    os.system("python3.6 " + script3 + " " + balancedDTB + " " + path_balanced + " " + fileRecapBalancedName + " \"" + str(availableSplits[i]) + "\"")
    print("\n")

    print("\n", file = fileRecapBalanced)

# Close files
fileRecapUnbalanced.close()
fileRecapBalanced.close()
