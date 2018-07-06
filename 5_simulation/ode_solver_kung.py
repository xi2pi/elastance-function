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
    
def ethan(x,i,A_1,A_2):
    return (A_1*np.cos(i*x*2*np.pi)-A_2*np.sin(i*x*2*np.pi))
    
def kung_func(t):
    AMP_ethan_1 =[2.2379*10**-1,
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
    AMP_ethan_2 =[0.00,
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
    I_ethan =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    y_ethan = 0
    
    for i in I_ethan:
        y_ethan += ethan(t, I_ethan[i], AMP_ethan_1[i], AMP_ethan_2[i])
        
    return y_ethan


#x = np.linspace(0, 1, num = 500)
#y_ethan = np.zeros(500)



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
    
        
def E_kung(t):
    heart_cycle = int(t/T)
    #print("heart Cycle" + str(heart_cycle))
    t = t - heart_cycle * T
    
    E_kung = kung_func(t)
    
#    popt2=[0.62,0.61,0.09,0.46,0.82,0.17]
#    fit2 = func(t, *popt2)
    #print(type(fit3))
    #plt.plot(x, np.roll(fit3/max(fit3), -np.argmax(fit3)+142) , 'r-', linewidth = 3, alpha =0.6, label = "Patient 1")
    return E_kung
    

### Elastance function
def Elastance(Emax,Emin,t):
    return (E_kung(t) * (Emax-Emin) + Emin)
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

    




    
    