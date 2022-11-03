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
    graph_data = open('output_data.txt','r').read()
    lines = graph_data.split('\n')
    t1 = []
    p1 = []
    v1 = []
    to1 = []
    th1 = []
    omg1 = []
    torq1 = []
    t2 = []
    p2 = []
    v2 = []
    to2 = []
    th2 = []
    omg2 = []
    torq2 = []


    for line in lines:
        if len(line) > 1:
            a, b = line.split(';')

            time, theta, p_out,omega, v_out, torque, t_out = a.split(',')
            t1.append(float(time))
            p1.append(57.1 * float(p_out))
            v1.append(float(v_out))
            to1.append(float(t_out))
            th1.append(57.1 * float(theta))
            omg1.append(float(omega))
            torq1.append(float(torque))

            time, theta, p_out,omega, v_out, torque, t_out = b.split(',')
            t2.append(float(time))
            p2.append(float(p_out))
            v2.append(float(v_out))
            to2.append(float(t_out))
            th2.append(float(theta))
            omg2.append(float(omega))
            torq2.append(float(torque))

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax4.clear()
    ax5.clear()
    ax6.clear()

    current_time = t1[len(t1) - 1]

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

    ax1.plot(t1, p1)
    ax1.plot(t1, th1)
    
    ax2.plot(t1, v1)    
    ax2.plot(t1, omg1)
    # ax3.plot(t1, to1)
    # ax3.plot(t1, torq1)
    
    # ax4.plot(t2, [57.1 * i for i in p2])
    # ax4.plot(t2, th2)
    # ax5.plot(t2, v2)    
    # ax5.plot(t2, omg2)
    # ax6.plot(t2, to2)
    # ax6.plot(t2, torq2)
    
ani = FuncAnimation(fig, animate, interval=1000)

plt.show()