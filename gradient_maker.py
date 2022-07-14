from nancheck import nanchecker
import numpy as np

#This script takes in an array E of Laplace coordinates and returns the gradient or vector field
#along that coordinates direction

def gradient_maker(E):

    newdat = np.empty((E.shape))

    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            for k in range(E.shape[2]):
                if E[i,j,k] != 0: 
                    newdat[i,j,k] = E[i,j,k]
                else:
                    newdat[i,j,k] = np.nan
    
    sz_E=E.shape

    dxER,dxEL,dxE,dyER,dyEL,dyE,dzER,dzEL,dzE = np.empty((9,sz_E[0],sz_E[1],sz_E[2]))
    arr1 = np.empty(9)
    arr1[:] = np.nan
    dxER[:],dxEL[:],dxE[:],dyER[:],dyEL[:],dyE[:],dzER[:],dzEL[:],dzE[:] = arr1
  
    E = newdat 
    
    #Take derivative along each direction while considering border cases
    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            for k in range(E.shape[2]):
                if i+1<E.shape[0]:
                    dxEL[i, j, k] = E[i + 1, j, k] - E[i, j, k]
                if i>0:
                    dxER[i, j, k] = E[i, j, k] - E[i - 1, j, k]
                dxE[i,j,k]=nanchecker(dxEL[i, j, k],dxER[i, j, k],E[i,j,k])
                if j+1<E.shape[1]:
                    dyEL[i, j, k] = E[i , j + 1, k] - E[i, j, k]
                if j>0:
                    dyER[i, j, k] = E[i, j, k] - E[i, j-1, k]
                dyE[i, j, k] = nanchecker(dyEL[i, j, k], dyER[i, j, k],E[i,j,k])
                if k+1< E.shape[2]:
                    dzEL[i, j, k] = E[i, j, k+1] - E[i, j, k]
                if k> 0:
                    dzER[i, j, k] = E[i, j, k] - E[i, j, k-1]
                dzE[i,j,k]=nanchecker(dzEL[i, j, k],dzER[i, j, k],E[i,j,k])
                
                
    gradient = np.stack([dxE,dyE,dzE],axis=3)
    normgradient = np.empty((gradient.shape))
	
    #normalize gradient vectors 
    for i in range(gradient.shape[0]):
        for j in range(gradient.shape[1]):
            for k in range(gradient.shape[2]):
            	for l in range(gradient.shape[3]):
                     if gradient[i,j,k,l] != 0:
                          dennorm = np.linalg.norm(gradient[i,j,k,:])
                          new = gradient[i,j,k,l]/dennorm
                          normgradient[i,j,k,l] = new

    #return normalized gradient      	        
    return (np.asarray(normgradient).T)
