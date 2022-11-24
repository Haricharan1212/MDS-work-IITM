from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure()
ax1 = fig.add_subplot(2,3,1)
ax2 = fig.add_subplot(2,3,2)
ax3 = fig.add_subplot(2,3,3)
ax4 = fig.add_subplot(2,3,4)
ax5 = fig.add_subplot(2,3,5)
ax6 = fig.add_subplot(2,3,6)

def animate(i):
    data = np.loadtxt("output_data.txt")

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax4.clear()
    ax5.clear()
    ax6.clear()

    current_time = data[-1][0]

    ax1.set_title("Position: theta_5")
    ax2.set_title("Velocity: omega_5")
    ax3.set_title("Torque: theta_5")
    
    ax4.set_title("Position: theta_6")
    ax5.set_title("Velocity: theta_6")
    ax6.set_title("Torque: theta_6")

    ax1.set_xlim(current_time - 20, current_time)
    ax2.set_xlim(current_time - 20, current_time)
    ax3.set_xlim(current_time - 20, current_time)
    ax4.set_xlim(current_time - 20, current_time)
    ax5.set_xlim(current_time - 20, current_time)
    ax6.set_xlim(current_time - 20, current_time)

    ax1.set_ylim(-100, 100)
    ax2.set_ylim(-10, 10)
    ax3.set_ylim(-50, 50)
    ax4.set_ylim(-6.28, 6.28)
    ax5.set_ylim(-3, 3)
    ax6.set_ylim(-50, 50)

    ax1.plot(data[:, 0], 180 / 3.14 * data[:, 1])
    ax1.plot(data[:, 0], 180 / 3.14 * data[:, 2])
    
    ax2.plot(data[:, 0], data[:, 3])
    ax2.plot(data[:, 0], data[:, 4])
    
    ax3.plot(data[:, 0], data[:, 5])
    ax3.plot(data[:, 0], data[:, 6])

    
    # ax4.plot(t2, [57.1 * i for i in p2])
    # ax4.plot(t2, th2)
    # ax5.plot(t2, v2)    
    # ax5.plot(t2, omg2)
    # ax6.plot(t2, to2)
    # ax6.plot(t2, torq2)
    
ani = FuncAnimation(fig, animate, interval=1000)

plt.show()