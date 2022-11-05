from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

time.sleep(5)
def animate(i):
    arr = np.loadtxt("output_data.txt", "float")
    ax1.clear()
    ax1.set_title("Torque")

    if len(arr) != 0:
        ax1.set_xlim(arr[-500 if len(arr) > 500 else 0][0], arr[-1][0])
        ax1.set_ylim(-20, 20)

        ax1.plot(arr[:, 0], arr[:, 1])
        ax1.plot(arr[:, 0], arr[:, 2])
        ax1.plot(arr[:, 0], arr[:, 2] - arr[:, 1])
        ax1.legend(["t_in", "t_out", "t_pd"])

ani = FuncAnimation(fig, animate, interval=1000)

plt.show()