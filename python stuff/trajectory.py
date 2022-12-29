import numpy as np

def theta_5(w, t, phi): 
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

    return (a0 + a1*np.cos(t*w + phi) + b1*np.sin(t*w + phi) + 
    a2*np.cos(2*t*w + phi) + b2*np.sin(2*t*w + phi) + a3*np.cos(3*t*w + phi) + b3*np.sin(3*t*w + phi) + 
    a4*np.cos(4*t*w + phi) + b4*np.sin(4*t*w + phi) + a5*np.cos(5*t*w + phi) + b5*np.sin(5*t*w + phi) + 
    a6*np.cos(6*t*w + phi) + b6*np.sin(6*t*w + phi))
    
def omega_5(w, t, phi):

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

    return w * (-a1*np.sin(t*w+phi) + b1*np.cos(t*w+phi) - 
    2 * a2 * np.sin(2*t*w+phi) + 2 * b2*np.cos(2*t*w+phi) - 3 * a3 * np.sin(3*t*w+phi) + 3 * b3 * np.cos(3*t*w+phi) + 
    - 4 * a4*np.sin(4*t*w+phi) + 4 * b4*np.cos(4*t*w+phi) - 5 *  a5*np.sin(5*t*w+phi) + 5 * b5 * np.cos(5*t*w+phi) - 
    6 * a6*np.sin(6*t*w+phi) + 6 * b6 * np.cos(6*t*w+phi))

def theta_6(w, t, phi): 
    
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

    return (a0 + a1*np.cos(t*w+phi) + b1*np.sin(t*w+phi) + a2*np.cos(2*t*w+phi) + b2*np.sin(2*t*w+phi) + a3*np.cos(3*t*w+phi) + b3*np.sin(3*t*w+phi) +   
    a4*np.cos(4*t*w+phi) + b4*np.sin(4*t*w+phi) + a5*np.cos(5*t*w+phi) + b5*np.sin(5*t*w+phi) 
    + a6*np.cos(6*t*w+phi) + b6*np.sin(6*t*w+phi) + a7*np.cos(7*t*w+phi) + b7*np.sin(7*t*w+phi) 
    + a8*np.cos(8*t*w+phi) + b8*np.sin(8*t*w+phi))

def omega_6(w, t, phi): 
    
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

    return w * (-a1*np.sin(t*w+phi) + b1*np.cos(t*w+phi) - 
    2 * a2 * np.sin(2*t*w+phi) + 2 * b2*np.cos(2*t*w+phi) - 3 * a3 * np.sin(3*t*w+phi) + 3 * b3 * np.cos(3*t*w+phi) + 
    - 4 * a4*np.sin(4*t*w+phi) + 4 * b4*np.cos(4*t*w+phi) - 5 *  a5*np.sin(5*t*w+phi) + 5 * b5 * np.cos(5*t*w+phi) - 
    6 * a6*np.sin(6*t*w+phi) + 6 * b6 * np.cos(6*t*w+phi) - 7 * a7*np.sin(7*t*w+phi) + 7 * b7 * np.cos(7*t*w+phi) 
    - 8 * a8 * np.sin(8*t*w+phi) + 8 * b8 * np.cos(8*t*w+phi))
