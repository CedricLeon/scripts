import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
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

print(bcolors.WARNING + "This script don't work, it's just a bunch of code to rotate a 3D-Curve.\n" + bcolors.ENDC)

# Our 2-dimensional distribution will be over variables X and Y
N = 60
X = np.linspace(-4, 6, N)
Y = np.linspace(-6, 5, N)
X, Y = np.meshgrid(X, Y)

# Pack X and Y into a single 3-dimensional array
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

fig = plt.figure()
ax = Axes3D(fig) #fig.gca(projection='3d')
ax.set_zlim(0,0.1)
ax.set_zticks(np.linspace(0,0.1,5))
ax.view_init(27, -21)

def init():
    ax.plot_surface(X, Y, 0.2*Z1+0.8*Z2, rstride=3, cstride=3, linewidth=1, antialiased=True,
                cmap=cm.viridis)

    # Remove the background
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Fond transparent
    ax.xaxis.set_label_text(r"x", horizontalalignment='center', verticalalignment='center', fontsize=12)
    ax.yaxis.set_label_text(r"y", horizontalalignment='center', verticalalignment='center', fontsize=12)

    return fig,


init()

def animate(i):
    ax.view_init(elev=10, azim=i*4)
    return fig,

ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=90, interval=100, blit=True)

fn = 'test'
# ani.save(fn+'.mp4',writer='ffmpeg',fps=1000/50)
ani.save(fn+'.gif', writer='imagemagick', fps=1000/100, savefig_kwargs={'transparent': True})
