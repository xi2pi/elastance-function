# -*- coding: utf-8 -*-
'''
Author of this script: Christian Winkler
e-mail: s6cnwink@uni-bonn.de
date: 26.01.2018

Reference:

Kung E, Pennati G, Migliavacca F, et al. 
A Simulation Protocol for Exercise Physiology in Fontan Patients Using a Closed Loop Lumped-Parameter Model. 
ASME. J Biomech Eng. 2014;136(8):081007-081007-13. doi:10.1115/1.4027271
'''


import numpy as np
import matplotlib.pyplot as plt

def kung(x,i,A_1,A_2):
    return (A_1*np.cos(i*x*2*np.pi)-A_2*np.sin(i*x*2*np.pi))

# amplitudes for cosinus
AMP_kung_1 =[2.2379*10**-1,
4.1054*10**-2,
-2.3140*10**-1,
1.7515*10**-2,
1.3159*10**-2,
-4.7293*10**-2,
-1.3394*10**-3,
-3.9917*10**-5,
-1.2594*10**-2,
-1.1214*10**-3,
1.6008*10**-3,
-2.9655*10**-3,
4.4509*10**-4,
9.5826*10**-4,
4.1644*10**-6,
4.1503*10**-5,
-1.4608*10**-5,
-9.4191*10**-5,
-3.5561*10**-5,
-1.3225*10**-4]

# amplitudes for sinus
AMP_kung_2 =[0.00,
-4.0948*10**-1,
-2.6814*10**-2,
8.5190*10**-2,
-5.0110*10**-2,
2.1048*10**-4,
2.2155*10**-2,
-5.9333*10**-3,
2.4557*10**-3,
9.1653*10**-3,
5.5933*10**-4,
1.6101*10**-3,
3.4309*10**-3,
4.0949*10**-4,
5.5756*10**-4,
2.1745*10**-4,
3.3081*10**-4,
1.7029*10**-4,
1.9828*10**-4,
1.4701*10**-4]

# Vector for the 19 trems 
I_kung =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]


# Compute function values
x = np.linspace(0, 1, num = 500)
y_kung = np.zeros(500)
for i in I_kung:
    y_kung += kung(x, I_kung[i], AMP_kung_1[i], AMP_kung_2[i])


'''
Ethan Kung's elastance function (2014)
'''

# Plotting
plt.plot(x, y_kung, 'b-', linewidth = 3, alpha =0.6, label = "Kung et al. (2014)",zorder=3)

plt.axhline(1, color='k', linestyle='--', linewidth = 0.5)
plt.axvline(x[142], color='k', linestyle='--', linewidth = 0.5)
plt.legend(prop={'size': 8})
plt.xlabel("Time [-]")
plt.ylabel("Elastance [-]")
plt.grid()
plt.savefig("elastance_kung_2014.png")
plt.show()

