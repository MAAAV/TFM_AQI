# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from . import EOI_DATA


# buffer_poblacion_500m.csv
#            0     1     2     3      4       5
#EOI_DATA[codi_eoi]["POBLACION_500M "] = [TOTAL,HOMES,DONES,P_0_14,P_15_64,P_65_I_MES,P_ESPANYOL,P_ESTRANGE,P_NASC_CAT,P_NASC_RES,P_NASC_EST]


def get_CVP(eoi_code, iP = 1):
    # iP: num. indice o tasa
    # 1. El indice o mal llamada «tasa» de envejecimiento (por que no es una tasa), 
    #    en realidad es simplemente la proporcion de mayores de 64 anyos
    #    = ((Poblacion >64 anyos / Poblacion total) x100) (proporcion de individuos 
    #    mayores de 64 anyos sobre el total de la poblacion. Se suele expresar como porcentaje).
    #
    # 2. Index d'envelliment (IDESCAT). Poblacio de 65 anys i mes per cada 100 habitants de menys de 15 anys.
    
    dict = EOI_DATA.get(eoi_code, {})
    llista = dict.get("POBLACION_500M", [])
    if not llista: return np.nan
    
    # comprovem que hem trobat les dades associades a l'estacio. 
    total = float(llista[0])
    p_0_14 = float(llista[3])
    p_65 = float(llista[5])

    if iP == 1:
        return round(100.0 * p_65 / total, 2)
    elif iP == 2:
        return round(100.0 * p_65 / p_0_14, 2)
    else:
        return np.nan 



if __name__ == '__main__':  
    #'08101001': [52579,25616,26940,7585,35542,9280,36791,15545,19944,10495,21981]
    # total = 52579  |  p_0_14 = 7585  |  p_65 = 9280
    # iP=1: 100*9280/52579 = 17.6496319824
    # iP=2: 100*9280/7585 = 122.346736981
    
    cvp = get_CVP('08101001',1)
    print(f" CVP (iP=1) for 08101001: {cvp} | 17.6496319824")
    
    cvp = get_CVP('08101001')
    print(f" CVP (iP=1 default) for 08101001: {cvp}")
    
    cvp = get_CVP('08101001',2)
    print(f" CVP (iP=2) for 08101001: {cvp} | 122.346736981")

