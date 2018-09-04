# -*- coding: utf-8 -*-
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


N=0.6
dos= []

fobj = open("test_dos_stoer64.dat", "r")
for line in fobj:
    z = line.split(" ")
    dos.append([float(z[0]), float(z[1].split("\n")[0])]) # hier durch faktoren mit Füllung spielen
    # J.E. Hirsch Fig. 3
fobj.close()


def ener(dE, E, m, U, n):
    en = 0
    nn=0
    m=0
    for d in dos:
        nn += 2*d[1]*dE
        if nn > N:
            break
        en += 2*(d[0] + U*(n-m)/2)*d[1]*dE
#    for d in dos:
#        en += (d[0] + U*(n+m)/2)*d[1]*dE
    return en - U*(n-m)*(n+m)/4



def energie_U(dE, E, n):
    en = [[],[]]
    m=[]
    fobj = open("m(U)_anti_1.0.dat", "r")
    for line in fobj:
        z = line.split("\t")
        m.append([float(z[0]), float(z[1].split("\n")[0])])
    fobj.close()
    for m_U in m:
        en[0].append(m_U[0])
        en[1].append(ener(dE, E, 0, m_U[0], n))
        #print(en[1][-1])
        
    return en

for i in range(00,201,1):
    N = float(i/100)
    print(N)
    #m = m_U(1/10000,10000,1)
    en = energie_U(1/10000, 10000, N)
    fobj = open("para_energie_"+str(N*100)+"stoer64.dat", "w")
    for i in range(len(en[0])):
        fobj.write(str(en[0][i]) + "\t" + str(en[1][i]) + "\n")
    print("\a")
    fobj.close()


#def ener(dE, E, m, U, n):
#    dk_x = 0.005
#    dk_y = 0.005
#    
#    k_x = -0.5
#    k_y = 0.5
#    e_ret = 0.0
#    norm = 0.0
#    for ii in range(1,400):
#        e_k = -2*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi))
#        
#        while k_x < 0.0:
#            k_y += dk_y * np.abs(np.sin(k_x*np.pi))
#            k_x += dk_x * np.abs(np.sin(k_y*np.pi))
#            #e_ret -= m*np.sqrt(e_k**2+(U*m/2)**2)
#            e_ret += 2*e_k
#            norm += 2
#        
#        k_y = 0.5 - 1/800 * ii
#        k_x = -0.5 + 1/800 * ii
#    return e_ret/norm * n + U*n**2/4 
