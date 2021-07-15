import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

nbStudy = 8

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
        # values = list(valuesSet)
        param1.append(float(values[1]))  # ( (float(values1[1]) + float(values2[1])) / 2)
        param2.append(float(values[2]))  # ( (float(values1[2]) + float(values2[2])) / 2 )
        score.append(float(values[2+nbStudy+1].replace(',','.')))

    return [np.array(param1), np.array(param2), np.array(score)]




fileName = "/home/cleonard/dev/stage/results/MoyRoots.csv"
#"/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs"
#sys.argv[1]

[x_array, y_array, z_array] = get_data_from_CSV_file(fileName)

# -------------------------- DEBUG --------------------------
# print("Param N°1 : ", x_array, " param N°1 length : ", x_array.size)
# print("Param N°2 : ", y_array, " param N°2 length : ", y_array.size)
# print("Score : ", z_array)

# -------------------- Plotting 2D curves -------------------

# Compute the number of different curves (the number of different nbRoots values)
nbDiffnbRoots = int(z_array.size/10)
print(nbDiffnbRoots, "different curves")
print("X abscisses =", y_array[0:9])

colors=['#584E7A', '#16078A', '#7100A8', '#AC2694', '#BB3488', '#E26561',
        '#F2844B', '#FDB52E', '#FCCD25', '#F0F724', '#F4FD01']

# Plot the 3 first curves as 1 because uninteresting (always lowest score)
fig4 = plt.figure("MNIST Scores for each nbRoots in function of ratioDeletedRoots")
ax4 = fig4.add_subplot(111)
ax4.plot(y_array[0:10], z_array[0:10], 'black', label="1, 5 and 10 nbRoots")


# Browse arrays and plot each curves
for i in range(3, nbDiffnbRoots):
    # Don't plot 360 nbRoots : weird
    if(i != 6):
        # Each curve owns 10 points (10 different values for ratioDeletedRoots)
        start_index = i*10
        end_index = start_index+10

        # Compute the trend line
        z_poly = np.polyfit(y_array[start_index:end_index], z_array[start_index:end_index], 3) # Follow deg 3 polynomial
        z = np.poly1d(z_poly)
        nbRoots = int(x_array[start_index])

        # Define a fake linespace to plot a better representation of the trendline
        x_linespace = np.linspace(0, 0.99, 99)

        # Compute ymax and xmax for the linespace trend line
        ymax = max(z(x_linespace))
        xpos = np.where(z(x_linespace) == ymax)
        xmax = x_linespace[xpos]

        # Update legend label
        label = str(nbRoots) + ": " + str(int(xmax*100)/100) + " (" + str(int(ymax)) + "%)"
        print("N°", i, ",", label, ", Scores =", z_array[start_index:end_index]) #, "Trend line equation =\n", z)

        # # Plot the true curve and its trend line (hardly readable)
        # ax4.plot(y_array[start_index:end_index], z_array[start_index:end_index], label=label)
        # ax4.plot(y_array[start_index:end_index], z(y_array[start_index:end_index]), label=label)

        # Plot only the trend line
        ax4.plot(x_linespace, z(x_linespace), colors[i-3], label=label)

        # For the first curves : plot the true line
        if(nbRoots <= 1000):
            ax4.plot(y_array[start_index:end_index], z_array[start_index:end_index], colors[i-3], linestyle='dashed', alpha=0.5)

        # Annotate Max value
        ax4.annotate("", xy=(xmax, ymax+1), xytext=(xmax, ymax-1), arrowprops=dict(color='r', width=2, headwidth=1, headlength=1), )

# Set axis value and labels
ax4.grid(axis='y', color='0.7')
ax4.axis([0, 1, 0, 70])
ax4.set_xlabel('ratioDeletedRoots (prob)')
ax4.set_ylabel('MNIST Score (%)')
ax4.set_title('Trend lines (poly deg 3)', fontsize=10)
ax4.legend(loc='upper left')

# -------------------- Plotting 3D curve --------------------

fig1 = plt.figure("MNIST Score in function of nbRoots and ratioDeletedRoots (FULL RANGE)")
fig1.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array), vmax=max(z_array)), cmap='plasma'), label='MNIST Score (%)')
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot_trisurf(list(x_array), list(y_array), list(z_array), cmap='plasma', linewidth=0, antialiased=False)
ax1.set_xlabel('nbRoots (int)')
ax1.set_ylabel('ratioDeletedRoots (prob)')
ax1.set_zlabel('score (%)')

# fig2 = plt.figure("MNIST Score in function of nbRoots and ratioDeletedRoots (START RANGE)")
# fig2.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array[:-36]), vmax=max(z_array[:-36])), cmap='plasma'), label='MNIST Score (%)')
# ax2 = fig2.add_subplot(111, projection='3d')
# ax2.plot_trisurf(list(x_array[:-36]), list(y_array[:-36]), list(z_array[:-36]), cmap='plasma', linewidth=0, antialiased=False)
# ax2.set_xlabel('nbRoots (int)')
# ax2.set_ylabel('ratioDeletedRoots (prob)')
# ax2.set_zlabel('score (%)')

# survivingRoots = (1 - y_array) * x_array
# fig3 = plt.figure("MNIST Score in function of nbRoots and surviving Roots")
# fig3.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=min(z_array[:-50]), vmax=max(z_array[:-50])), cmap='plasma'), label='MNIST Score (%)')
# ax3 = fig3.add_subplot(111, projection='3d')
# ax3.plot_trisurf(list(x_array[:-50]), list(survivingRoots[:-50]), list(z_array[:-50]), cmap='plasma', linewidth=0, antialiased=False)
# ax3.set_xlabel('nbRoots (int)')
# ax3.set_ylabel('surviving Roots (int)')
# ax3.set_zlabel('score (%)')

plt.show()

print("End plot")
