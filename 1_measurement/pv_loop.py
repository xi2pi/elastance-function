# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:24:34 2017

@author: C Winkler
"""

import pandas as pd
import numpy as np
from cycler import cycler
import matplotlib.pyplot as plt
import os
from scipy.signal import argrelextrema
from statsmodels.nonparametric.smoothers_lowess import lowess

plt.rc('axes', prop_cycle=(cycler('color', ['b','k','k', 'r', 'k', 'k'])))

#print(os.listdir())

columns = ['Patient','Emax_BL', 'Emin_BL', 'Emax_dobu', 'Emin_dobu']
df = pd.DataFrame(columns=columns)
df['Patient'] = pd.Series(os.listdir())



def read_and_plot_data(): 
    
    pv = pd.read_excel("conductance_measurement.xls", header = 1)
    plot_pvloop(pv)
   

        
def plot_pvloop(pv):
    pv=pv.iloc[1:]
    pv.columns=["beat", "time", "pressure", "volume", "d(pressure)/dt"]
    pv["elastance"] = pv["pressure"]/pv["volume"]
    #m = max(pv["elastance"])
    maxima = max(pv["elastance"].values)
    minima = min(pv["elastance"].values)

    print(maxima)

    ## Filter
    filtered_pressure = lowess(pv["pressure"].values, pv["time"].values, is_sorted=True, frac=0.025, it=0)
    filtered_volume = lowess(pv["volume"].values, pv["time"].values, is_sorted=True, frac=0.025, it=0)
    #filtered_pv = lowess(pv["pressure"].values, pv["volume"].values, is_sorted=True, frac=0.025, it=0)
    
    ## Maxima and minima of filtered signal
    maxima_possible = [filtered_volume[:,1][i] for i in argrelextrema(filtered_volume[:,1], np.greater)]
    maxima_volume = [i for i in maxima_possible[0] if i > np.mean(pv["volume"].values)]
    
    maxima_possible = [filtered_pressure[:,1][i] for i in argrelextrema(filtered_pressure[:,1], np.greater)]
    maxima_pressure = [i for i in maxima_possible[0] if i > np.mean(pv["pressure"].values)]
    #print(minima)
    
      
    beats = str(len(maxima_pressure)) + " beats"
    
    
    plt.plot(pv["volume"], pv["pressure"], label = "PV - Loop (BL) "  +beats)
    
    
    plt.xlim([0, 60])
    plt.ylim([-10, 70])
    
    plt.grid()
    plt.xlabel(r"Volume [ml]")
    plt.ylabel(r"Pressure [mmHg]")
    plt.legend()
    plt.savefig("pv_loop.png", dpi = 500)
    plt.close()
    

    

try:
    read_and_plot_data()
except:
    print("error")




