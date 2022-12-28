#Libraries
import logging
import azure.functions as func
import json
import numpy as np
from scipy.integrate import solve_ivp


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Reactor designing begins...')



    production= 21000 # petrol barrels per day
    V0 = production * 0.006624470622 # m3/h
    density = 0.715 #g/cm3

    massic_flow_0 = V0  * density * 100**3 #g/h
    D = 3.5 #m
    #      res , vgo , des , naf , gas
    y0 = [0.394,0.281,0.204,0.121,0] # initial non-processed petrol composition
    k1 = 0.147
    k2 = 0.022
    k3 = 0.020
    k4 = 0.098
    k5 = 0.057
    k6 = 0.007
    k7 = 0
    k8 = 0.003
    k9 = 0
    k10 = 0

    V_init = 0
    V_final = 500

    def reactionSystem(V,y):
        y1 = y[0]
        y2 = y[1]
        y3 = y[2]
        y4 = y[3]
        y5 = y[4]

        dyWastes = (-k1*y1-k2*y1-k3*y1-k4*y1)/V0
        dyVGO = (k1*y1-k5*y2-k6*y2-k7*y2)/V0
        dyDistilled = (k2*y1+k5*y2-k8*y3-k9*y3)/V0
        dyNaftas = (k3*y1+k6*y2-k8*y3-k10*y4)/V0
        dyGases = (k4*y1+k7*y2+k9*y3+k10*y4)/V0

        return np.array([dyWastes, dyVGO,dyDistilled,dyNaftas,dyGases])


    sol = solve_ivp(reactionSystem, (V_init,V_final),y0)

    logging.info(sol)



    
   
    return func.HttpResponse("Reactor designed successfully")