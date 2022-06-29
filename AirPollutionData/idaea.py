# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import operator

# ---------------------------------------------------------------------------------------------------------------------
# NO2 any 2019 determinat per l'IDAEA
# Unitats LCZ_*: m2  
#                                         0   1     2     3     4     5     6     7     8     9     10     11    12    13    14    15    16    17    18
# EOI_DATA[codi_eoi]["LCZvsNO2_500M"] = [NO2,LCZ_1,LCZ_2,LCZ_3,LCZ_4,LCZ_5,LCZ_6,LCZ_7,LCZ_8,LCZ_9,LCZ_10,LCZ_A,LCZ_B,LCZ_C,LCZ_D,LCZ_E,LCZ_F,LCZ_G,Total]

from . import EOI_DATA

def get_NO2_2019(eoi_code):
    dict = EOI_DATA.get(eoi_code, {})
    llista = dict.get("LCZvsNO2_500M",[])
    if llista:
        return llista[0]
    else:
        return np.nan


def get_LCZmax(eoi_code):
    lcz_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
    # anem a obtenir la informacio associada a les LCZs dins d'un buffer de 500m de l'estacio
    dict = EOI_DATA.get(eoi_code, {})
    llista = dict.get("LCZvsNO2_500M",[])
    if llista:
        total = float(llista[18])
        dict = {}
        for iP, value in enumerate(lcz_keys):
            dict[value] = round(100*float(llista[iP+1])/total, 2)
        # retornem la key (LCZ) associada que ocupa mes area en el buffer...
        return dict, max(dict, key=dict.get)
    else:
        return {}, "none"


if __name__ == '__main__': 
     #  LCZ | m2            |     %
     #    1 |      0        |  0.0
     #    2 | 409162.6443   | 63.419557135
     #    3 |  99192.50982  | 15.374680781
     #    4 |      0        |  0.0
     #    5 |   1190.02     |  0.184451201
     #    6 |      0        |  0.0
     #    7 |      0        |  0.0
     #    8 |  99502.416    | 15.422715745
     #    9 |      0        |  0.0
     #   10 |      0        |  0.0
     #    A |      0        |  0.0
     #    B |  35832.88324  |  5.554039738
     #    C |     18.94399  |  0.002936288
     #    D |      0        |  0.0
     #    E |     37.86917  |  0.00586966
     #    F |    230.644    |  0.035749452
     #    G |      0        |  0.0
     # total = 645167.9305

    codi = '08101001'
    no2 = get_NO2_2019(codi)
    print(f"NO2 for {codi}: {no2} (33)")
    lcz = get_LCZmax(codi)
    print(f"LCZ max: {lcz}")

