# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 08:55:48 2018

@author: C Winkler
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:24:34 2017

@author: C Winkler
"""

import pandas as pd
import numpy as np
from cycler import cycler
import matplotlib.pyplot as plt
import glob, os
from scipy.signal import argrelextrema
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.optimize import curve_fit

plt.rc('axes', prop_cycle=(cycler('color', ['b','k','k', 'r', 'k', 'k'])))

def func(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i]
        amp = params[i+1]
        wid = params[i+2]
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
    return y

        
def plot_pvloop(pv):
    pv=pv.iloc[1:]
    pv.columns=["beat", "time", "pressure", "volume", "d(pressure)/dt"]
    
    elastance = (pv["pressure"])/(pv["volume"] + 18.57)
    elastance = elastance.values

    ## Filter
    filtered_pressure = lowess(pv["pressure"].values, pv["time"].values, is_sorted=True, frac=0.025, it=0)
    filtered_volume = lowess(pv["volume"].values, pv["time"].values, is_sorted=True, frac=0.025, it=0)
    
    filtered_elastance = lowess(elastance, pv["time"].values, is_sorted=True, frac=0.1, it=0)

    ## Maxima and minima of filtered signal
    maxima_possible = [filtered_volume[:,1][i] for i in argrelextrema(filtered_volume[:,1], np.greater)]

    
    maxima_possible = [filtered_pressure[:,1][i] for i in argrelextrema(filtered_pressure[:,1], np.greater)]
    maxima_pressure = [i for i in maxima_possible[0] if i > np.mean(pv["pressure"].values)]
   
        
    beats = str(len(maxima_pressure)) + " beats"

       
    minima_pos =  argrelextrema(filtered_elastance[:,1], np.less)
    minima_pos = np.append(minima_pos, len(elastance))
    
    separator = np.array([0])
    separator = np.append(separator, minima_pos)

    parts = [elastance[i:j] for i,j in zip(separator, separator[1:])]
    parts_time = [pv["time"].values[i:j] for i,j in zip(separator, separator[1:])]
    

    # drop first and last one
    for i in range(1, len(parts)-1):
        x = np.linspace(0, 1, num = len(parts[i]))
        
        #y = np.array([])
        parts_min = min(parts[i])
        parts_max = max(parts[i])
        #print(parts_min)
#        parts[i] = parts[i] - parts_min
#        parts[i] = parts[i] / (parts_max-parts_min)
        


        plt.plot(x, parts[i], color = "r", label= "elastance signal")
        
        
    Y = [x for _,x in sorted(zip(x, parts[i]))]
    guess = [0.7, 1, 0.1]
    for i in range(1):
        guess += [0.5+80*i, 0.6, 0.1]
    popt, pcov = curve_fit(func, x, Y, p0=guess)
    print(popt[0])
#    popt[0] = popt[0] - 0.19
#    popt[3] = popt[3] - 0.19
    
#    popt[1] = popt[1]/ 1.16
#    popt[4] = popt[4]/ 1.16
    fit = func(x, *popt)
    
    fit_max = max(fit)
    #print("maximum ist: " + str(max(fit/fit_max)))
    
    plt.plot(x, fit , 'k-', linewidth = 3)
    #plt.plot(x,Y/fit_max,'b.', alpha = 0.3, label = "Measured Data")
    
    
    plt.text(0.1,0.5,'Double Gaussian:\nAmp$_1$ = %.2f\nAmp$_2$ = %.2f\nCenter$_1$ = %.2f\nCenter$_2$ = %.2f\n$\sigma_1$ = %.2f\n$\sigma_2$ = %.2f' % (popt[1],popt[4],popt[0],popt[3],popt[2],popt[5]))
    plt.text(0.1,0.3, "Max. " + str(round(fit_max, 2)))  
    
        
    plt.xlabel("Time [-]")
    plt.ylabel("Elastance [-]")
        
    plt.grid()    
    plt.savefig("elastance.png")
    plt.show()



pv = pd.read_excel("conductance_measurement.xls", header = 1)
plot_pvloop(pv)







