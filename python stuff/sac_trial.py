# Global imports
import time
import numpy as np
import tmotorCAN
import numpy as np
# from simple_pendulum.controllers.ilqr.iLQR_MPC_controller import iLQRMPCController
from simple_pendulum.controllers.lqr.lqr_controller import LQRController
from matplotlib import pyplot as plt

def prepare_empty(dt, tf):
    n = int(tf/dt)

    # create 4 empty numpy array, where measured data can be stored
    des_time_list = np.zeros(n)
    des_pos_list = np.zeros(n)
    des_vel_list = np.zeros(n)
    des_tau_list = np.zeros(n)

    meas_time_list = np.zeros(n)
    meas_pos_list = np.zeros(n)
    meas_vel_list = np.zeros(n)
    meas_tau_list = np.zeros(n)
    vel_filt_list = np.zeros(n)

    data_dict = {"des_time_list": des_time_list,
                 "des_pos_list": des_pos_list,
                 "des_vel_list": des_vel_list,
                 "des_tau_list": des_tau_list,
                 "meas_time_list": meas_time_list,
                 "meas_pos_list": meas_pos_list,
                 "meas_vel_list": meas_vel_list,
                 "meas_tau_list": meas_tau_list,
                 "vel_filt_list": vel_filt_list,
                 "n": n,
                 "dt": dt,
                 "t": tf}
    return data_dict

def ak80_6(controller, kp=0., kd=0., dt=0.005, tf=10., torque_limit = 10):

    n = int(tf/dt)

    data_dict = prepare_empty(dt, tf)

    kp_in = kp
    kd_in = kd
    
    motor = tmotorCAN.tmotor(1, 'ak80-64')

    meas_pos, meas_vel, meas_tau = 0, 0, 0

    motor.attain(meas_pos, meas_vel, meas_tau, kp, kd)
    time.sleep(2)

    print("After enabling motor, pos: ", meas_pos, ", vel: ", meas_vel,
          ", tau: ", meas_tau)

    i = 0
    meas_dt = 0.0
    meas_time = 0.0
    vel_filtered = 0
    start = time.time()

    try:
        while i < n:
            start_loop = time.time()
            meas_time += meas_dt

            des_pos, des_vel, des_tau = controller.get_control_output(meas_pos, vel_filtered, meas_tau, meas_time)
            
            if des_pos is None:
                des_pos = 0
                kp_in = 0
            else:
                kp_in = kp

            if des_vel is None:
                des_vel = 0
                kd_in = 0
            else:
                kd_in = kd

            # kp_in = 0
            # kd_in = 0
            meas_pos, meas_vel, meas_tau = motor.attain(des_pos, des_vel, des_tau, kp_in, kd_in)

            # filter noisy velocity measurements
            # if i > 0:
            #     vel_filtered = np.mean(data_dict["meas_vel_list"][max(0, i-10):i])
            # else:
            #     vel_filtered = 0
            # or use the time derivative of the position instead
            # vel_filtered = (meas_pos - meas_pos_prev) / dt
            # meas_pos_prev = meas_pos

            data_dict["meas_pos_list"][i] = meas_pos
            data_dict["meas_vel_list"][i] = meas_vel
            data_dict["meas_tau_list"][i] = meas_tau
            data_dict["meas_time_list"][i] = meas_time
            data_dict["vel_filt_list"][i] = vel_filtered
            data_dict["des_pos_list"][i] = des_pos
            data_dict["des_vel_list"][i] = des_vel
            data_dict["des_tau_list"][i] = des_tau
            data_dict["des_time_list"][i] = dt * i

            i += 1
            exec_time = time.time() - start_loop
            if exec_time > dt:
                print("Control loop is too slow!")
                print("Control frequency:", 1/exec_time, "Hz")
                print("Desired frequency:", 1/dt, "Hz")
                print()
            while time.time() - start_loop < dt:
                pass
            meas_dt = time.time() - start_loop

    except BaseException as e:
        print('*******Exception Block!********')
        print(e)

    try:
        print("Disabling Motors...")
        motor.attain(0, 0, 0, 0, 0)
        motor.exit_motor_mode()
    except BaseException as e:
        print('Motors already disabled')

    end = time.time()
    return start, end, meas_dt, data_dict

# --------

# data_dict = {}
# times = np.linspace(0, 10, 300)

# data_dict["des_time_list"] = times
# data_dict["des_pos_list"] = np.ones(times.shape) * 0
# data_dict["des_vel_list"] = np.ones(times.shape) * 0
# data_dict["des_tau_list"] = np.zeros(times.shape) * 0

# PID

# control_method = PIDController(data_dict=data_dict, Kp= 12.0, Ki=0.0001, Kd=2, use_feed_forward=True)

# --------

# SAC


# params_file = "sp_parameters_sac.yaml"

# with open(params_file, 'r') as fle:
#     params = yaml.safe_load(fle)

# control_method = SacController(model_path="best_model_latest", torque_limit = 10, state_representation=3, use_symmetry=True)

# --------

mass = 0.5
length = 0.44
inertia = (mass*(length**2))/3
damping = 0.1
gravity = 9.81
coulomb_fric = 0.0
torque_limit = 100

control_method = LQRController(mass=mass,
                           length=length,
                           damping=damping,
                           coulomb_fric=coulomb_fric,
                           gravity=gravity,
                           torque_limit=torque_limit,
                           moment_of_inertia=(mass * (length**2)) / 3,
                           Q=np.diag([0.1, 0.01]),
                           R=np.array([[0.01]]),
                           compute_RoA=False)

control_method.set_goal([-1.57, 0])

# --------

# mass = 0.5
# length = 0.44
# inertia = (mass*(length**2))/3
# damping = 0.1
# gravity = 9.81
# coulomb_fric = 0.0
# torque_limit = 100

# gr= 6
# kp= 0
# kd= 0
# mass= 0.6755 # 0.57288
# damping= 0.35
# dt= 0.010
# runtime= 20

# #ilqr specific parameters
# n_horizon= 50
# n_x= 2
# dt= 0.02
# t_final= 10.0
# x0= np.array([0.0, 0.0])
# sCu= 50.0
# sCp= 5.0
# sCv= 1.0
# sCen= 10.0
# fCp= 5.0
# fCv= 1.0
# fCen= 80.0
# dynamics= 'runge_kutta'
# max_iter= 1
# break_cost_redu= 0.1

# control_method = iLQRMPCController(
#                             mass=mass,
#                             length=length,
#                             damping=damping,
#                             coulomb_friction=coulomb_fric,
#                             gravity=gravity,
#                             dt=dt,
#                             n=n_horizon,
#                             max_iter=max_iter,
#                             break_cost_redu=break_cost_redu,
#                             sCu=sCu,
#                             sCp=sCp,
#                             sCv=sCv,
#                             sCen=sCen,
#                             fCp=fCp,
#                             fCv=fCv,
#                             fCen=fCen,
#                             dynamics=dynamics,
#                             n_x=n_x)

# control_method.set_goal(np.array([np.pi, 0]))
# control_method.init(x0=x0)


data_dict = {}
start, end, meas_dt, data_dict = ak80_6(control_method, dt=0.05, tf=5., torque_limit=100)

plt.plot(data_dict["meas_pos_list"])
plt.plot(data_dict["des_tau_list"])

plt.legend(["Position", "Torque"])

# plt.show()