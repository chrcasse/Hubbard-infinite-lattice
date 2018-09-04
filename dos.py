
"""
Created on Sun Apr 29 15:42:53 2018

@author: Ch

Berechnung der Zustrandsdichte für ein Quadratgitter
in Tight-Binding-Naeherung unter ausschliesslicher
Beruecksichtigung von Naechstenachbar-Wechselwirkung.
"""

import numpy as np
import matplotlib.pyplot as plt






def dos_interp(d, dE, E): # density of states [Energie E, dos(E)] -> dos(E)
    ener = [[],[]]
    for erg in range(-int(E), int(E)):
        ener[0].append(erg * dE)
    ener[1] = np.interp(ener[0], d[0], d[1])
    return ener


def dos(dE, E,n):
    dk_x = 0.0001
    dk_y = 0.0001
    inte = 0.0
    k_x = -0.5
    k_y = 0.5
    #n = Felstellen pro Zelle
    
    dos = [[],[],[]]
    ddos = [[],[]]
    for ii in range(1,800):
        # Energie der Aequienergielinie entlang derer integriert wird
        dos[0].append(2*(1-2*n)*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi))) # t=1
        # anfangs k_x der entsprechenden Kurve
        dos[1].append(round(2*(1-2*n)*(np.cos(k_x*np.pi) + np.cos(k_y*np.pi)),1))
        while k_x < 0:
            inte += 1.0
            k_y += dk_y * np.abs(np.sin(k_x*np.pi))
            k_x += dk_x * np.abs(np.sin(k_y*np.pi))
        #print(inte)         
        # Zustandsdichte der entsprechenden Energie
        # * 8 da nur ein viertel des Weges integriert
        # und hoffentlich auf jedem Viertel gleich
        dos[2].append(inte) # *2 Um wie die anderen beiden Energien
                              # ueber die gesamtze Seite zu gehen
        
        inte = 0.0    
        k_y = 0.5 - 1*0.000625 * ii
        k_x = -0.5 + 1*0.000625 * ii

    
    
    for x in range(len(dos[0])-1, -1 ,-1):
        ddos[0].append(-dos[0][x])
        ddos[1].append(dos[2][x]) # Normiert auf 2
        
        
    for x in range(0, len(dos[0])-1):
        ddos[0].append(dos[0][x])
        ddos[1].append(dos[2][x]) # Normiert auf 2
        
    
    ddos = dos_interp([ddos[0], ddos[1]], dE, 2*2*(1-2*n)*E) # Energie = np.cos(0*np.pi) + np.cos(0*np.pi)

    
    inte = 0.0
    for x in ddos[1]:
        inte += x*dE
    ddos[1] = [x/inte for x in ddos[1]]

    return ddos








dos = dos(1/10000,10000,1/64)

fobj = open("test_dos_stoer64.dat", "w") 
for i in range(len(dos[0])):
    fobj.write(str(dos[0][i]) + " " + str(dos[1][i]) + "\n")
fobj.close()

    
