import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_data_from_file(fileName):

    # Get file name
    print("File name : ", str(fileName))

    # Open file, get every line except the 3 first
    file = open(str(fileName), "r")
    data = file.readlines()[3:]

    file.close()

    param1 = []
    param2 = []
    score = []

    for i in range(len(data)):

        # Split data in a tab containing every pair
        values = data[i].split(";")
        # values = "Training nbRoots ratioDeletedRoots ScoreN°1 ScoreN°2 ScoreN°3 Moyenne GenerationN°1 GenerationN°2 GenerationN°3 Moyenne Temps"
        # values = list(valuesSet)
        param1.append(float(values[1]))  # ( (float(values1[1]) + float(values2[1])) / 2)
        param2.append(float(values[2]))  # ( (float(values1[2]) + float(values2[2])) / 2 )
        score.append(float(values[6][:-2].replace(',','.')))
        # [:-2] to remove '\n' char at the end of the line

    return [np.array(param1), np.array(param2), np.array(score)]


fileName = "/home/cleonard/dev/stage/results/MoyRoots.csv" #"/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs"
#fileName2 = "/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs" # sys.argv[2]
#fileName3 = "/home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots1/lastScore.logs" # sys.argv[3]

print("Script name : ", str(sys.argv[0]))

[x_array, y_array, z_array] = get_data_from_file(fileName)

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