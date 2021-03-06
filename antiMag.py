﻿# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 13:48:42 2018

@author: Ch
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 21:22:29 2018

@author: Ch
"""

import math as np
#import fermienergie as fe
#import phasenuebergang as ph
#import bandstruktur as bs


def sgn(x):
    if x > 0 or x == 0:
        return 1
    else:
        return -1


N=0.6
dos= []

fobj = open("test_dos_stoer64.dat", "r")
for line in fobj:
    z = line.split(" ")
    dos.append([float(z[0]), 1*float(z[1].split("\n")[0])]) # hier durch faktoren mit Füllung spielen
    # J.E. Hirsch Fig. 3
fobj.close()

def ener(dE, E, m, U, n):
    en = 0
    nn = 0
    for d in dos:#[x for x in dos if x[0]<0]:
        en += 2*(U*n/2 + sgn(d[0]) * np.sqrt(d[0]**2 + (U*m/2)**2))*d[1]*dE # U*(n-m)/2*d[1]*dE #
        nn += 2*d[1]*dE
        if nn > n:
            break
    return en - U*(n-m)*(n+m)/4

def mag(dE, E, m, U, n):
    ma = 0
    nn=0
    for d in dos:#[x for x in dos if x[0]<0]:
        ma += -sgn(d[0])*2*U*m/2/np.sqrt(d[0]**2 + (U*m/2)**2)*d[1]*dE
        nn += 2*d[1]*dE
        if nn > n:
            break
    return ma




def anti_mag(dE, E, U, n,m):
    mm = 1.0
    while abs(mm - m) > 0.001:
        mm = m
        m = mag(dE, E, mm, U, n)
    #print("{}:{}".format(U,m))
    return m

def m_U(dE, E, n):
    m = [[],[]]
    m[0].append(12.1)
    m[1].append(anti_mag(dE, E, 12.1, n,n*0.9))
    
    for U in [x*dE for x in range(int(12/dE), 00,-1000)]:
        m[0].append(U)
        m[1].append(anti_mag(dE, E, U, n,m[1][-1]))
        
    return m

def energie_U(dE, E, n):
    en = [[],[]]
    m=[]
    fobj = open("m(U)_anti_"+str(N*100)+"stoer64.dat", "r") #vorher II
    for line in fobj:
        z = line.split("\t")
        m.append([float(z[0]), float(z[1].split("\n")[0])])
    fobj.close()
    for m_U in m:#[x for x in m if x[1] > n*0.01]:
        en[0].append(m_U[0])
        en[1].append(ener(dE, E, m_U[1], m_U[0], n))
        #print(en[1][-1])
        
    return en


for j in range(0,201,1):
    N = float(j/100)
    print(N)
    m = m_U(1/10000,10000,N)
    fobj = open("m(U)_anti_"+str(N*100)+"stoer64.dat", "w") #ungestoert II statt stoer25
    for i in range(len(m[0])):
        fobj.write(str(m[0][i]) + "\t" + str(m[1][i]) + "\n")
    #print("\a")
    fobj.close()
    en = energie_U(1/10000, 10000, N)
    fobj = open("anti_energie_"+str(N*100)+"stoer64.dat", "w") #vorher II
    for i in range(len(en[0])):
        fobj.write(str(en[0][i]) + "\t" + str(en[1][i]) + "\n")
    #print("\a")
    fobj.close()









#def ener(dE, E, m, U, n):
#    dk_x = 0.005
#    dk_y = 0.005
#    inte = 0.0
#    k_x = -0.0
#    k_y = 0.0
#    
#    e_ret = 0.0
#    norm = 0.0
#    for ii in range(1,400):
#        e_k = 2*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi))
#        
#        while k_x < 0.0:
#            inte += 1.0
#            k_y += dk_y * np.abs(np.sin(k_x*np.pi))
#            k_x += dk_x * np.abs(np.sin(k_y*np.pi))
#            #e_ret -= m*np.sqrt(e_k**2+(U*m/2)**2)
#            e_ret -= np.sqrt(e_k**2+(U*m/2)**2)
#            norm += 1
#        
#        k_y = 0 + 1/800 * ii
#        k_x = -0 - 1/800 * ii
#    return e_ret/norm * n + U*n**2/2 - U*(n-m)*(n+m)/4
#
#def mag(dE, E, m, U, n):
#    dk_x = 0.005
#    dk_y = 0.005
#    inte = 0.0
#    k_x = -0.0
#    k_y = 0.0
#    
#    m_ret = 0.0
#    norm = 0.0
#    for ii in range(1,400):
#        
#        e_k = 2*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi))
#        while k_x < 0.0:
#            inte += 1.0
#            k_y += dk_y * np.abs(np.sin(k_x*np.pi))
#            k_x += dk_x * np.abs(np.sin(k_y*np.pi))
#            m_ret += U*m/2/np.sqrt(e_k**2+(U*m/2)**2)
#            norm += 1
#        
#        k_y = 0 + 1/800 * ii
#        k_x = -0 - 1/800 * ii
#    return m_ret/norm * n
