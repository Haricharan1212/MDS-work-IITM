#  Examples (simulation)

This folder contains example scripts for the implemented trajectory optimization, reinforcement learning and control methods.

## Trajectory Optimization

### Differential Dynamic Programming (DDP)

Trajectory optimization with DDP is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/trajectory_optimization/ddp).

It can be tested with

    python compute_BOXFDDP.py

The script computes a trajectory and stores the trajectory in a csv file at "log_data/ddp/trajectory.csv". The trajectory is also simulated as open loop controller with pinocchio and visualized with the gepetto viewer.

Requirements: Crocoddyl

### Direct Collocation

Trajectory optimization with direct collocation is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/trajectory_optimization/direct_collocation). 

It can be tested with

    python compute_dircol_swingup.py

The script computes a trajectory and stores the trajectory in a csv file at "log_data/direct_collocation/trajectory.csv". The trajectory is also simulated with a [TVLQR](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/tvlqr) controller which stabilizes the trajectory.

Requirements: Drake

### Iterative Linear Quadratic Regulator (iLQR)

Trajectory optimization with iLQR is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/trajectory_optimization/ilqr).

It can be tested with

    python compute_iLQR_swingup.py

The script computes a trajectory and stores the trajectory in a csv file at "log_data/ilqr/trajectory.csv". The trajectory is also simulated as open loop controller.

Requirements: Drake (optional)

If Drake is installed the symbolic libary of Drake will be used, else sympy is used.

## Reinforcement Learning

### State Actor Critic (SAC)

The SAC reinforcement learning method is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/sac).

To train a model:

    python train_sac.py

This might take a while. The model will be saved at "log_data/sac_training/sac_model.zip". A trained model is provided [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/data/models/sac_model.zip). It can be tested with

    python sim_sac.py

This will simulate and visualize the behavior of the pendulum following this policy for 10s.

Requirements: torch, stable-baselines3

Note: The provided model was trained with versions: torch==1.10.0 and stable-baselines==1.3.0. Loading it with other versions may cause errors.

### Deep Deterministic Policy Gradient (DDPG)

The DDPG reinforcement learning method is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/ddpg).

To train a model:

    python train_ddpg.py

This might take a while. The model will be saved at "log_data/ddpg_training/ddpg_model". A trained model is provided [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/data/models/ddpg_model). It can be tested with

    python sim_ddpg.py

This will simulate and visualize the behavior of the pendulum following this policy for 10s.

Requirements: tensorflow

Note: The provided model was trained with versions: tensorflow==2.6.1. Loading it with other versions may cause errors.

## Closed Loop Control

### Linear Quadratic Regulator (LQR)

The LQR method is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/lqr).

It can be tested with

    python sim_lqr.py

This will simulate and visualize the pendulum with control inputs from the LQR controller.
The start state of the pendulum is near the top position within the region of attraction of the LQR controller. The LQR controller stabilizes the pendulum at the top position.

### Energy Shaping

The energy shaping method is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/energy_shaping).

It can be tested with

    python sim_energy_shaping.py

This will simulate and visualize the pendulum with control inputs from the energy shaping controller. Near the top position the controller will switch to the LQR controller to stabilize the pendulum.´

### Model Predictive Control (MPC) with iLQR

Model Predictive control with iLQR is explained [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/ilqr).

It can be tested with

    python sim_ilqrMPC.py

This will simulate and visualize the pendulum with control inputs from the ilqr-MPC controller.
The controller computes an initial guess for a swingup trajectory and then swings up the pendulum and stabilizes the pendulum at the top position.

Requirements: Drake (optional)

If Drake is installed the symbolic libary of Drake will be used, else sympy is 
used.

## Region of Attraction estimation

### Time-invariant estimation

The Region of Atttraction estimation procedure is described [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/lqr/roa). The pendulum parameters are fixed to mass = 0.57288, length = 0.5, 
damping = 0.15, gravity = 9.81, coulomb_fric = 0.0. Also the goal position is fixed to the up-right position.

The different used methods can be compared in simulation with

    python plot_roa_estimations.py
Here the torque limits can be modified to see different results, they should be at most five different. The choosed torque limits are 0.1, 0.5, 1, 2, 3.

The RoA certification reliability can be verified with

    python verify_roa_estimation.py
where 500 different initial conditions have been chosen to verify the theory. Choosing a lot of different initial conditions will slow down the execution. The torque limit has been fixed to 4, but it is not a restrictive value for the code functionality.

Furthermore, the effects of the Taylor approximation on the closed-loop dynamics can be seen with

    python taylorApprox_roa_sos.py
where the maximum approximation order has been fixed to 7, enough to see the interesting results. The torque limit has been fixed to 8, the high value is due to the need of analyzing the all range of angles fro 0 to pi.

The RoA estimation plots can be found in the result folder [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/results/RoA_estimation_plots).

### Time-varying estimation

The time-varying version of the Region of Atttraction estimation procedure is described [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/software/python/simple_pendulum/controllers/tvlqr/roa). The pendulum parameters are fixed to mass = 0.57288, length = 0.5, 
damping = 0.15, gravity = 9.81, coulomb_fric = 0.0, torque limit = 2. Also the goal position is fixed to the up-right position. Furthermore, the other estimation parameters has been chosen to be: number of knot points = 60, number of simulations for the estimation = 100, number of simulations for the verification = 50.

The verification of the estimation procedure can be obtained with

    python verify_tvlqr_roa.py -prob
if we want to observe the probabilistic method behaviour or with

    python verify_tvlqr_roa.py -sos
if we want to analyse the SOS Method for estimating the RoA. In both cases a verification function will check the estimation for some knot points (0,20,40). This procedure takes some time.

Furthermore, by running

    python verify_tvlqr_roa.py -compare
the comparison between the two estimations will be shown with some plots ad hoc.

The RoA estimation, verification and comparison plots can be found in the result folder [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/results/RoA_estimation_plots).

## Analysis

### Plotting

The policies of the energy shaping, LQR, SAC and DDPG controllers can be plotted with

    python plot_controller.py

The controller to be plotted can be specified in the script.

### Benchmarking

The controllers can be benchmarked with

    python benchmark_controller.py

This script will perform the benchmark evaluation for all controllers which are specified within the "cons" list in the script. As default all available controllers are listed here. As many iterations of the controllers are necessary to perform the benchmark analysis, the execution of this script may take a while. The results will be written to "log_data/benchmarks".

The benchmarks can be plotted with

    python plot_benchmarks.py

By default the script will load the precomputed benchmarks from [here](https://github.com/dfki-ric-underactuated-lab/torque_limited_simple_pendulum/blob/master/data/benchmarks).



