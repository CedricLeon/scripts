import sys
import shutil
from tqdm import tqdm
from os import listdir
from os.path import isfile, join

folder = "/home/cleonard/Data/binary_datasets/tmp/"
folder_copy = "/home/cleonard/Data/binary_datasets/balanced_BTV_dataset/"

files = [f for f in listdir(folder) if isfile(join(folder,f))]
i = 0
for file in tqdm(files):
   shutil.copyfile(folder+file,  folder_copy+str(i)+".bin")
   i = i+1
print(i)
