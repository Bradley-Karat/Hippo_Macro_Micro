import numpy as np

def nanchecker(A,B,E=None):
    if (np.isnan(A) == True and np.isnan(B) == True):
        C = np.NaN
    if(np.isnan(A) == True and np.isnan(B) == False):
        C = B
    if(np.isnan(A) == False and np.isnan(B) == True):
        C = A
    if(np.isnan(A) == False and np.isnan(B) == False):
        C = 0.5 * (A + B)
    return C
