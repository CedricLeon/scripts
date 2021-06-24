import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

size = 32

# Get file name
print("Script name : ", str(sys.argv[0]))
print("File name : ", str(sys.argv[1]))
inputFile = str(sys.argv[1])
splitName = inputFile.split("/")[-2]
print(splitName)

# Open file, get last line and print it
file = open(inputFile, "r")
data = file.readlines()[-1]
print(data)
file.close()

# Remove first ('{') and last ('}' + any space if there is) char from data
data = data[1:]
while data[-1] != "}":
    data = data[:-1]
data = data[:-1]

# Split data in a tab containing every pair
pixels = data.split("} {")

# Init accesses
access = np.zeros((32, 32))

# Store data in access
for p in pixels:
    # Split every pair with the pixel index (var[0]) and the number of accesses (var[1])
    var = p.split(",")
    # Compute 2D indexes
    row = int(var[0]) // size
    col = int(var[0]) % size
    #print(var, row, col)
    # Store number of accesses in the corresponding pixel
    access[row][col] = int(var[1])

# *** Own colormap (pretty but not really efficient) ***
# # Create the colors (normalized)
# topo_colors = [(255/255, 255/255, 255/255),  # Blanc
#                (243/255, 232/255, 77/255),   # Jaune
#                (255/255, 146/255, 3/255),    # Orange
#                (255/255, 0/255, 0/255),      # Rouge
#                (197/255, 3/255, 255/255),    # Violet
#                (3/255, 205/255, 255/255),    # Bleu
#                (75/255, 255/255, 9/255)      # Vert
#               ]
# # Create the colormap from my personnalized colors
# my_cmap = LinearSegmentedColormap.from_list('topo_basic', topo_colors)
# # Print access as an image with my colormap
# plt.imshow(access, cmap=my_cmap)
# # Plot a colorbar with my colormap for the scale
# plt.colorbar(extend = 'both')

# *** JET colormap (internet) ***
cmap = plt.cm.jet  # define the colormap
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# force the first color entry to be grey
cmaplist[0] = (1, 1, 1, 1.0)
# create the new map
cmap = LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

# Show image
fig = plt.figure(splitName)
plt.imshow(access, cmap=cmap)
plt.colorbar(extend = 'both')
plt.show()
