# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 02:06:12 2017

@author: Ana Cabrera
"""
import numpy as np
#import matplotlib.pyplot as plt
#T = 3
#X = 4
#Y = 5
#D = np.ceil(np.random.rand(T, X, Y)*100)
def Prom_Ponderado(D,W_2,T,X,Y) :  
#    import ipdb; ipdb.set_trace()
    W=W_2
    W1 = np.divide(W, W ,out=np.zeros_like(W),where=W!=0)#np.ones((T, X, Y))
    
    
    
    #plt.imshow(W1[60])
    M = np.zeros((T, X, Y))
    M1 = np.zeros((T, X, Y))
    for i in range(T):
        M[i] = np.multiply(D[i], W[i])
        M1[i] = np.multiply(D[i], W1[i])
       
     
     
    E = np.sum(M, axis=0)
    Wt = np.sum(W, axis=0)
     
    E1 = np.sum(M1, axis=0)
    Wt1 = np.sum(W1, axis=0)
    
    
    Ideal=np.divide(E, Wt,out=np.zeros_like(E), where=Wt!=0)
    Ideal1=np.divide(E1, Wt1 ,out=np.zeros_like(E1),where=Wt1!=0)
    print 'Con pesos: ', Ideal
    print 'Sin pesos: ', Ideal1
    
    return Ideal,Ideal1
