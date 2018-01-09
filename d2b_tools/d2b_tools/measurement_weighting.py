# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 00:15:56 2018

@author: Ana Cabrera
"""

import numpy as np
import matplotlib.pyplot as plt
 

def to_search_efficiency_raw(matrix_weighted,matrix_per_detector):
    T=len(matrix_per_detector)
    X=len(matrix_per_detector[0]) #filas
    Y=len(matrix_per_detector[0][0]) #columnas
    efficency_raw=np.zeros((T,X,Y))
    for a in range(0,T):
        efficency_raw[a]=np.divide(matrix_weighted, matrix_per_detector[a], out=np.zeros_like(matrix_weighted), where=matrix_per_detector[a]!=0)
    plt.figure(200)
    plt.imshow(efficency_raw[60],clim=(0.5,1.5))
    plt.figure(200+1)
    plt.hist(efficency_raw[60].ravel(), bins=266, range=(0.01, 4), fc='k', ec='k')
    return efficency_raw

def weight_per_inverse_of_relative_error(matrix_weighted):
    print(matrix_weighted)
    

def calculation_inverse_of_relative_error():
    pass

def weight_by_position_of_detector(D):
    T=len(D)
    X=len(D[0]) #filas
    Y=len(D[0][0]) #columnas
    W = D
    #W = np.sqrt(W_2)
    W1 = np.divide(W, W, out=np.zeros_like(W), where=W!=0)#np.ones((T, X, Y))
    #M = np.zeros((T, X, Y))
    M1 = np.zeros((T, X, Y))
    for i in range(T):
        #M[i] = np.multiply(D[i], W[i])
        M1[i] = np.multiply(D[i], W1[i])
     
    #E = np.sum(M, axis=2)
    #Wt = np.sum(W, axis=2)
     
    E1 = np.sum(M1, axis=2)
    Wt1 = np.sum(W1, axis=2)
    
    
    #Ideal=np.divide(E, Wt,out=np.zeros_like(E), where=Wt!=0)
    Ideal1=np.divide(E1, Wt1 ,out=np.zeros_like(E1),where=Wt1!=0)
    print(len(Ideal1))
    print(len(Ideal1[0]))
    plt.figure(300)
    plt.imshow(Ideal1,clim=(0.75,2))
    
    
if __name__ == '__main__':
    '''
    de d2b_tools importo el metodo, luego instancio un objeto de una clase dentro de ese metodo y luego con ese objeto puedo llamar a las funciones
    '''
    from d2b_tools import measurements_reader, measurements_sorter
    shots = measurements_reader.integration_test()
    ds = measurements_sorter.DetectorSorter(shots)
    matrix_per_detector, matrix_weighted = ds.integration_test_sorter()
    efficency_raw = to_search_efficiency_raw(matrix_weighted,matrix_per_detector)
    weight_by_position_of_detector(efficency_raw)