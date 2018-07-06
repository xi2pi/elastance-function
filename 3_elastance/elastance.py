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

plt.rc('axes', prop_cycle=(cycler('color', ['b','k','k', 'r', 'k', 'k'])))

        
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
        parts[i] = parts[i] - parts_min
        parts[i] = parts[i] / (parts_max-parts_min)
        


        plt.plot(x, parts[i], color = "r", label= "elastance signal")
        
    plt.xlabel("Time [-]")
    plt.ylabel("Elastance [-]")
        
    plt.grid()    
    plt.savefig("elastance.png")
    plt.show()



pv = pd.read_excel("conductance_measurement.xls", header = 1)
plot_pvloop(pv)







