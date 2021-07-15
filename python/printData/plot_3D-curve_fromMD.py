import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_data_from_file(fileName1, fileName2):

    # Get file name
    print("File name : ", str(fileName1), ", ", str(fileName2))

    # Open file, get every line except the 2 first
    file1 = open(str(fileName1), "r")
    data1 = file1.readlines()[2:]

    file2 = open(str(fileName2), "r")
    data2 = file2.readlines()[2:]

    file1.close()
    file2.close()

    param1 = []
    param2 = []
    score = []

    for i in range(len(data1)):

        # Split data in a tab containing every pair
        values1 = data1[i].split(" ")
        values2 = data2[i].split(" ")
        # values = list(valuesSet)
        param1.append(float(values1[1]))  # ( (float(values1[1]) + float(values2[1])) / 2)
        param2.append(float(values1[1]))  # ( (float(values1[2]) + float(values2[2])) / 2 )
        score.append( (float(values1[4][:-2].replace(',','.')) + float(values2[4][:-2].replace(',','.'))) / 2)
        # [:-2] to remove '\n' char at the end of the line

    return [np.array(param1), np.array(param2), np.array(score)]


fileName1 = "/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs" # sys.argv[1]
fileName2 = "/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs" # sys.argv[2]
#fileName = "/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs" # sys.argv[3]

print("Script name : ", str(sys.argv[0]))

[x_array, y_array, z_array] = get_data_from_file(fileName1, fileName2)

# print("Param N°1 : ", x_array, " param N°1 length : ", x_array.size)
# print("Param N°2 : ", y_array, " param N°2 length : ", y_array.size)
# print("Score : ", z_array)

# Plotting
fig1 = plt.figure("MNIST Score in function of nbRoots and ratioDeletedRoots (FULL RANGE)")
ax1 = fig1.add_subplot(111, projection='3d')

ax1.plot_trisurf(list(x_array), list(y_array), list(z_array), cmap='plasma', linewidth=0, antialiased=False)
ax1.set_xlabel('nbRoots (int)')
ax1.set_ylabel('ratioDeletedRoots (prob)')
ax1.set_zlabel('score (%)')

fig2 = plt.figure("MNIST Score in function of nbRoots and ratioDeletedRoots (START RANGE)")
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot_trisurf(list(x_array[:-36]), list(y_array[:-36]), list(z_array[:-36]), cmap='plasma', linewidth=0, antialiased=False)
ax2.set_xlabel('nbRoots (int)')
ax2.set_ylabel('ratioDeletedRoots (prob)')
ax2.set_zlabel('score (%)')

plt.show()