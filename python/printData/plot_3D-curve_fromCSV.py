import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

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

print(bcolors.WARNING + "This script is HUGE, you should read it.\n" + bcolors.ENDC)
print(bcolors.HEADER + "It is used to print data stored in a .csv file. Data is stored in a precise format with is not generalized in this script. Data owns to parameters : Param1 and Param2 and 2 corresponding results for each training (e.g. nbRoots and ratioDeletedRoots and their corresponding results: MNISTscore and trainingEndGeneration).")
print("This script plot the data in 2 different format :")
print("\t- A 3D curve with the raw data and a personnalized colormap")
print("\t- A batch of 2D curves each for a different Param1")
print("This script need only 1 argument: the path to the .csv to print (Check example/Roots.csv and example/Archive.csv).")

fileName = str(sys.argv[1]) # "/home/cleonard/dev/stage/results/Archive.csv"
nbStudy = 8
param1Name = "nbRoots"
param2Name = "ratioDeletedRoots"
nbDiffParam2 = 10

isArchiveStudy = fileName.split("/")[-1] == "Archive.csv"

if isArchiveStudy:
    nbStudy = 5
    param1Name = "archiveSize"
    param2Name = "archivingProbability"
    nbDiffParam2 = 11 # archivingProbability

# Define function importing data from a specific CSV file
def get_data_from_CSV_file(fileName):

    # Get file name
    print("Data from \"", str(fileName), "\"")

    # Open file, get every line except the 3 first, close the file
    with open(str(fileName), "r") as file:
        data = file.readlines()[3:]

    # Init empty arrays
    param1 = []
    param2 = []
    score = []

    # Browse rows and store specific values in arrays
    for i in range(len(data)):

        # Split data in a tab containing every pair
        values = data[i].split(";")

        # Pick up values
        param1.append(float(values[1]))
        param2.append(float(values[2]))
        score.append(float(values[2+nbStudy+1].replace(',','.')))

    # Return 3 arrays containing each parameter value and the corresponding score
    return [np.array(param1), np.array(param2), np.array(score)]


# Call the function to pick up data
[x_array, y_array, z_array] = get_data_from_CSV_file(fileName)

# -------------------------- DEBUG --------------------------
# print("Param N°1 : ", x_array, " param N°1 length : ", x_array.size)
# print("Param N°2 : ", y_array, " param N°2 length : ", y_array.size)
# print("Score : ", z_array)

# -------------------- Plotting 2D curves -------------------

# Compute the number of different curves (the number of different param1 values)
nbDiffParam1 = int(z_array.size/nbDiffParam2)
print(nbDiffParam1, "different curves")
print("X abscisses =", y_array[0:nbDiffParam2])

colors = ['#584E7A', '#38049A', '#16078A', '#7100A8', '#AC2694', '#BB3488', '#E26561',
        '#F2844B', '#FDB52E', '#FCCD25', '#F0F724', 'green', '#F4FD01']

# Plot the 3 first curves as 1 because uninteresting (always lowest score)
fig4 = plt.figure("MNIST Scores for each " + param1Name + " in function of " + param2Name)
ax4 = fig4.add_subplot(111)
ax4.plot(y_array[0:nbDiffParam2], z_array[0:nbDiffParam2], 'black', label="1, 5 and 10" + param1Name)


# Browse arrays and plot each curves
for i in range(3, nbDiffParam1):
    # For Roots: don't plot 360 param : weird
    #if(i != 6):
        # Each curve owns nbDiffParam2 points (nbDiffParam2 different values for param2)
        start_index = i * nbDiffParam2
        end_index = start_index + nbDiffParam2

        # Compute the trend line
        polyDeg = 3
        z_poly = np.polyfit(y_array[start_index:end_index], z_array[start_index:end_index], polyDeg) # Follow deg 3 polynomial
        z = np.poly1d(z_poly)
        param1 = int(x_array[start_index])

        # Define a fake linespace to plot a better representation of the trendline
        x_linespace = np.linspace(0, 0.99, 99)

        # Compute ymax and xmax for the linespace trend line
        ymax = max(z(x_linespace))
        xpos = np.where(z(x_linespace) == ymax)
        xmax = x_linespace[xpos]

        # Update legend label
        label = str(param1) + ": " + str(int(xmax*100)/100) + " (" + str(int(ymax)) + "%)"
        print("N°", i, ",", label, ", Scores =", z_array[start_index:end_index]) #, "Trend line equation =\n", z)

        # # Plot the true curve and its trend line (hardly readable)
        # ax4.plot(y_array[start_index:end_index], z_array[start_index:end_index], colors[i-3], label=label)
        # ax4.plot(y_array[start_index:end_index], z(y_array[start_index:end_index]), colors[i-3], label=label)

        # Plot only the trend line
        ax4.plot(x_linespace, z(x_linespace), colors[i-3], label=label) # , colors[i-3]

        # For the first curves : plot the true line
        if(param1 <= 1000 or param1 == 10000):
            ax4.plot(y_array[start_index:end_index], z_array[start_index:end_index], colors[i-3], linestyle='dashed', alpha=0.5)

        # Annotate Max value
        ax4.annotate("", xy=(xmax, ymax+1), xytext=(xmax, ymax-1), arrowprops=dict(color='r', width=2, headwidth=1, headlength=1), )

# Set axis value and labels
ax4.grid(axis='y', color='0.7')
if isArchiveStudy:
    ax4.axis([0, 1, 30, 55])
else:
    ax4.axis([0, 1, 0, 70])
ax4.set_xlabel(param2Name + "(prob)")
ax4.set_ylabel('MNIST Score (%)')
ax4.set_title("Trend lines (poly deg " + str(polyDeg) + ")", fontsize=12)
ax4.legend(loc='upper left')

# -------------------- Plotting 3D curves --------------------
# FULL RANGE
fig1 = plt.figure("MNIST Score in function of " + param1Name + " and " + param2Name + " (FULL RANGE)")
fig1.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array), vmax=max(z_array)), cmap='plasma'), label='MNIST Score (%)')
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot_trisurf(list(x_array), list(y_array), list(z_array), cmap='plasma', linewidth=0, antialiased=False)
ax1.set_xlabel(param1Name + "(int)")
ax1.set_ylabel(param2Name + "(prob)")
ax1.set_zlabel('score (%)')
if isArchiveStudy:
    ax1.set_zlim([30,45])

# # START RANGE
# endOfPlotIndex = 12 * nbDiffParam2
# fig2 = plt.figure("MNIST Score in function of " + param1Name + " and " + param2Name + " (START RANGE)")
# fig2.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array[:-36]), vmax=max(z_array[:-36])), cmap='plasma'), label='MNIST Score (%)')
# ax2 = fig2.add_subplot(111, projection='3d')
# ax2.plot_trisurf(list(x_array[:-endOfPlotIndex]), list(y_array[:-endOfPlotIndex]), list(z_array[:-endOfPlotIndex]), cmap='plasma', linewidth=0, antialiased=False)
# ax2.set_xlabel(param1Name + " (int)")
# ax2.set_ylabel(param2Name + " (prob)")
# ax2.set_zlabel('score (%)')
# ax2.set_zlim([30,45])

# # Special Plot for Roots study
# survivingRoots = (1 - y_array) * x_array
# fig3 = plt.figure("MNIST Score in function of " + param1Name + " and surviving Roots")
# fig3.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array[:-50]), vmax=max(z_array[:-50])), cmap='plasma'), label='MNIST Score (%)')
# ax3 = fig3.add_subplot(111, projection='3d')
# ax3.plot_trisurf(list(x_array[:-50]), list(survivingRoots[:-50]), list(z_array[:-50]), cmap='plasma', linewidth=0, antialiased=False)
# ax3.set_xlabel(param1Name + " (int)")
# ax3.set_ylabel(param2Name + " (prob)")
# ax3.set_zlabel('score (%)')

plt.show()

print("End plot")
