# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 21:22:29 2018

@author: Ch
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 15:42:53 2018

@author: Ch

Calculation of the density of states for a simple square lattice
with nearest neighbour hopping.


Berechnung der Zustrandsdichte für ein Quadratgitter
in Tight-Binding-Naeherung unter ausschliesslicher
Beruecksichtigung von Naechstenachbar-Wechselwirkung.
"""

import math as np






# Berechnung dos(E=0)
def dos(dE, E, U, m, n):
    dk_x = 0.00001
    dk_y = 0.00001
    inte = 0.0
    k_x = -0.5
    k_y = 0.5
    
    dos = [[],[],[]]
    dos_s = [[],[],[]]
    ddos = [[],[]]
    for ii in range(1,8000):
        # Energy for which the number of states will be counted
	# Energie der Aequienergielinie entlang derer integriert wird
        ener = 2*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi))
        dos[0].append(U*n/2-np.sqrt((U*m/2)**2+ener**2)) #t=1
        # anfangs k_x der entsprechenden Kurve
        dos[1].append(ener)
        while k_x < 0.0:
            inte += 1
            k_y += dk_y * abs(np.sin(k_x*np.pi))
            k_x += dk_x * abs(np.sin(k_y*np.pi))    
        dos[2].append(inte)

        inte = 0.0    
        k_y = 0.5 - 0.0000625 * ii
        k_x = -0.5 + 0.0000625 * ii
    
    
    for x in range(len(dos[0])-1, -1 ,-1):
        ddos[0].append(U*n-dos[0][x])
        ddos[1].append(dos[2][x]*(((U*m/2)**2+(dos[1][x])**2)**0.5-U*m/2)/((U*m/2)**2+(dos[1][x])**2)**0.5) # Normiert auf 2
        
        
    for x in range(0, len(dos[0])-1):
        ddos[0].append(dos[0][x])
        ddos[1].append(dos[2][x]*(((U*m/2)**2+(dos[1][x])**2)**0.5+U*m/2)/((U*m/2)**2+(dos[1][x])**2)**0.5) # Normiert auf 2




	
       
    inte = 0.0
    i=0
#normalization
    for x in ddos[1][0:-2]:
        i+=1
        inte -= x*(ddos[0][i]-ddos[0][i-1])
    ddos[1] = [x/inte/2 for x in ddos[1]]
    
    return ddos







dos = dos(1/10000,10000, 5, 0.77 ,1)


fobj = open("anti_dos_up.dat", "w")
for i in range(len(dos[0])):
    fobj.write(str(dos[0][i]) + " " + str(dos[1][i]) + "\n")
fobj.close()
    
