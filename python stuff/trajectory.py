import numpy as np

def theta_5(w, t): 
    a0 =      0.1836 
    a1 =      0.2662 
    b1 =     0.07282 
    a2 =     0.01358 
    b2 =     -0.0538 
    a3 =    -0.02318 
    b3 =    -0.01697 
    a4 =  -0.0007335 
    b4 =     0.01067 
    a5 =    0.005122 
    b5 =   -0.009857 
    a6 =   -0.004598 
    b6 =    -0.00232 

    return (a0 + a1*np.cos(t*w) + b1*np.sin(t*w) + 
    a2*np.cos(2*t*w) + b2*np.sin(2*t*w) + a3*np.cos(3*t*w) + b3*np.sin(3*t*w) + 
    a4*np.cos(4*t*w) + b4*np.sin(4*t*w) + a5*np.cos(5*t*w) + b5*np.sin(5*t*w) + 
    a6*np.cos(6*t*w) + b6*np.sin(6*t*w))
    
def omega_5(w, t):

    a0 =      0.1836 
    a1 =      0.2662 
    b1 =     0.07282 
    a2 =     0.01358 
    b2 =     -0.0538 
    a3 =    -0.02318 
    b3 =    -0.01697 
    a4 =  -0.0007335 
    b4 =     0.01067 
    a5 =    0.005122 
    b5 =   -0.009857 
    a6 =   -0.004598 
    b6 =    -0.00232 

    return w * (-a1*np.sin(t*w) + b1*np.cos(t*w) - 
    2 * a2 * np.sin(2*t*w) + 2 * b2*np.cos(2*t*w) - 3 * a3 * np.sin(3*t*w) + 3 * b3 * np.cos(3*t*w) + 
    - 4 * a4*np.sin(4*t*w) + 4 * b4*np.cos(4*t*w) - 5 *  a5*np.sin(5*t*w) + 5 * b5 * np.cos(5*t*w) - 
    6 * a6*np.sin(6*t*w) + 6 * b6 * np.cos(6*t*w))



def theta_6(w, t): 
    
    a0 =       -0.27
    a1 =     -0.2869 
    b1 =     -0.3615
    a2 =      0.2361 
    b2 =    -0.01295 
    a3 =    -0.04462 
    b3 =     0.04176 
    a4 =    0.006039 
    b4 =   -0.002234  
    a5 =    -0.01259  
    b5 =   -0.000709  
    a6 =    0.006121  
    b6 =   -0.004853  
    a7 =   -0.001197  
    b7 =   0.0002855  
    a8 =    0.001966  
    b8 =   2.208e-05  

    return (a0 + a1*np.cos(t*w) + b1*np.sin(t*w) + a2*np.cos(2*t*w) + b2*np.sin(2*t*w) + a3*np.cos(3*t*w) + b3*np.sin(3*t*w) +   
    a4*np.cos(4*t*w) + b4*np.sin(4*t*w) + a5*np.cos(5*t*w) + b5*np.sin(5*t*w) 
    + a6*np.cos(6*t*w) + b6*np.sin(6*t*w) + a7*np.cos(7*t*w) + b7*np.sin(7*t*w) 
    + a8*np.cos(8*t*w) + b8*np.sin(8*t*w))

def omega_6(w, t): 
    
    a0 =       -0.27
    a1 =     -0.2869 
    b1 =     -0.3615
    a2 =      0.2361 
    b2 =    -0.01295 
    a3 =    -0.04462 
    b3 =     0.04176 
    a4 =    0.006039 
    b4 =   -0.002234  
    a5 =    -0.01259  
    b5 =   -0.000709  
    a6 =    0.006121  
    b6 =   -0.004853  
    a7 =   -0.001197  
    b7 =   0.0002855  
    a8 =    0.001966  
    b8 =   2.208e-05  

    return w * (-a1*np.sin(t*w) + b1*np.cos(t*w) - 
    2 * a2 * np.sin(2*t*w) + 2 * b2*np.cos(2*t*w) - 3 * a3 * np.sin(3*t*w) + 3 * b3 * np.cos(3*t*w) + 
    - 4 * a4*np.sin(4*t*w) + 4 * b4*np.cos(4*t*w) - 5 *  a5*np.sin(5*t*w) + 5 * b5 * np.cos(5*t*w) - 
    6 * a6*np.sin(6*t*w) + 6 * b6 * np.cos(6*t*w) - 7 * a7*np.sin(7*w*t) + 7 * b7 * np.cos(7*w*t) 
    - 8 * a8 * np.sin(8*w*t) + 8 * b8 * np.cos(8 * w * t))

# from matplotlib import pyplot as plt
# import numpy as np

# t = np.array([i/100 for i in range(500)])
# plt.plot(t, theta_5(1.7, t))
# plt.show()
