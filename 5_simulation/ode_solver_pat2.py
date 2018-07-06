import numpy as np
import pandas as pd
from scipy.integrate import odeint

from scipy import interpolate

#import pressure_estimation
def func(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i]
        amp = params[i+1]
        wid = params[i+2]
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
    #print("y:" + str(y))
    return y

### ODE
def heart_ode(y, t, Rp, Ra, Rin, Ca, Cv, Vd, Emax, Emin):
    #print("ODE time:", t )
    Vlv, Pa, Pv = y
    
    Plv_0 = Plv(Vlv,Vd,Emax,Emin,t) 
    
    Qin_0 = Qin(Plv_0,Pv, Rin)
    Qa_0 = Qa(Plv_0,Pa,Ra)
    Qp_0 = Qp(Pa,Pv,Rp)
    
    dydt = [Qin_0-Qa_0, (Qa_0-Qp_0)/Ca, (Qp_0-Qin_0)/Cv]
    return dydt
    
def Qa(Plv,Pa,Ra):
    if (Plv>Pa):
        return (Plv - Pa)/Ra
    else: 
        return int(0)
        
def Qin(Plv,Pv, Rin):
    if (Pv>Plv):
        return (Pv - Plv)/Rin
    else:
        return int(0)
        
def Qp(Pa,Pv,Rp):
    return (Pa - Pv)/Rp
    
def Plv(Vlv,Vd,Emax,Emin,t):
    return Elastance(Emax,Emin,t)*(Vlv-Vd)
    

def E_pat2(t):
    heart_cycle = int(t/T)
    #print("heart Cycle" + str(heart_cycle))
    t = t - heart_cycle * T
    popt2=[0.62,0.61,0.09,0.46,0.82,0.17]
    fit2 = func(t, *popt2)
    #print(type(fit3))
    #plt.plot(x, np.roll(fit3/max(fit3), -np.argmax(fit3)+142) , 'r-', linewidth = 3, alpha =0.6, label = "Patient 1")
    return fit2
    

### Elastance function
def Elastance(Emax,Emin,t):
    return (E_pat2(t) * (Emax-Emin) + Emin)
    #return (Esin(t) * (Emax-Emin) + Emin)
        
### Solving the ODE
def compute_ode(Rp,Ra,Rin,Ca,Cv,Vd,Emax,Emin,t,start_v,start_pa,start_pv):
    y0 = [start_v, start_pa, start_pv]

    sol = odeint(heart_ode, y0, t, args = (Rp,Ra,Rin,Ca,Cv,Vd,Emax,Emin,))
    result_Vlv = sol[:, 0]
    result_Pa = sol[:, 1]
    result_Pv = sol[:, 2]
    return (result_Vlv, result_Pa, result_Pv)


    
def init_glob_para(HC):
    global T
    global Tsys
    global Tir
    
    T = HC                  #s Datensatz IM
    Tsys = 0.3*np.sqrt(T)   #s Samar (2005)
    #Tsys = 0.3
    Tir = 0.5*Tsys          #s Datensatz IM

    




    
    