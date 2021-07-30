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
import subprocess

size = np.array(["128x128", "64x64", "32x32", "16x16", "8x8", "64x32", "32x64", "64x16", "16x64", "32x16", "16x32", "64x8", "8x64", "32x8", "8x32", "16x8", "8x16", "64x4", "4x64", "32x4", "4x32", "16x4", "4x16", "8x4", "4x8"]) # 25 different dtb

availableSplitsDict = {            "4x8" : [0, 3],            "4x16" : [0, 3, 5],           "4x32" : [0, 3, 5],           "4x64" : [0, 3, 5],
            "8x4" : [0, 2],     "8x8" : [0, 2, 3],         "8x16" : [0, 2, 3, 5],        "8x32" : [0, 2, 3, 5],        "8x64" : [0, 2, 3, 5],
        "16x4" : [0, 2, 4], "16x8" : [0, 2, 3, 4],  "16x16" : [0, 1, 2, 3, 4, 5],    "16x32" : [0, 2, 3, 4, 5],    "16x64" : [0, 2, 3, 4, 5],
        "32x4" : [0, 2, 4], "32x8" : [0, 2, 3, 4],     "32x16" : [0, 2, 3, 4, 5], "32x32" : [0, 1, 2, 3, 4, 5],    "32x64" : [0, 2, 3, 4, 5],
        "64x4" : [0, 2, 4], "64x8" : [0, 2, 3, 4],     "64x16" : [0, 2, 3, 4, 5],    "64x32" : [0, 2, 3, 4, 5], "64x64" : [0, 1, 2, 3, 4, 5],
        "128x128" : [0, 1] }

for i in range(3, len(size)):
    print(size[i] + " " + str(availableSplitsDict[size[i]]))