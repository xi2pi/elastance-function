# -*- coding: utf-8 -*-
'''
Author of this script: Christian Winkler
e-mail: s6cnwink@uni-bonn.de
date: 26.01.2018

Reference:

Senzaki H, Chen C, Kass D. 
Single-beat estimation of end-systolic pressure-volume relation in humans. 
A new method with the potential for noninvasive application. 
Circulation. 1996;94(10):2497-2506.
'''


import numpy as np
import matplotlib.pyplot as plt

def sin_func(x,i,A,phi):
    return A/100*np.sin(phi+i*x*2*np.pi)
    

I =[0,1,2,3,4,5,6,7,8,9,10,11,12]
AMP = [28.38975,37.58583,21.02345,7.665592,4.809436,4.181973,1.940692,0.5870049,1.181256,0.84039,0.02259011,0.3071458,0.3226207]
PHI=[0,0.08367674,-1.486758,2.865675,0.1677238,4.630239,3.088379,-0.3053668,4.410703,3.181538,1.242886,4.156753,2.946186]
y = np.zeros(500)
x = np.linspace(0, 1, num = 500)
for i in I[1:]:
    y += sin_func(x,I[i], AMP[i], PHI[i])
    
y = y + 0.2838975


'''
Senzaki's elastance function (1996)
'''

# Plotting
plt.plot(x, y, 'r-', linewidth = 3, alpha =0.6, label = "Senzaki et al. (1996)",zorder=3)

plt.legend(prop={'size': 8})
plt.xlabel("Time [-]")
plt.ylabel("Elastance [-]")
plt.ylim([-0.2, 1.2])
plt.grid()
plt.savefig("elastance_senzaki_1996.png")
plt.show()

