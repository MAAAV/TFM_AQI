# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from . import ESTACIONS

DATA_ID = "tasf-thgu"
DATA_DOMAIN = "analisi.transparenciacatalunya.cat"
DATA_LIMIT = 50000

URL_DATA = "https://" + DATA_DOMAIN + "/resource/" + DATA_ID + ".json?"
#"https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json?"


HORES = [f"h0{i}" for i in range(1,10)] + [f"h{i}" for i in range(10,25)]


CONTAMINANTS = {
    "nom":  ['NO2', 'PM2.5', 'SO2', 'PS', 'CO', 'NO', 'PM10', 'PM1', 'NOX', 'O3', 'C6H6', 'HCT', 'HCNM', 'Cl2', 'HCl', 'H2S', 'Hg'],
    "codi": [ 8, 9, 1, 3, 6, 7, 10, 11, 12, 14, 30, 42, 44, 53, 58, 65, 331]
    }

# ---------------------------------------------------------------------------------------------------------------------
def get_all_EOI_data(ymd):
    # obtenim les dades en json de tots els contaminants i de totes les estacions per una data determinada
    df = pd.read_json(f"{URL_DATA}$where=data='{ymd}T00:00:00.000'", orient='records')
    if df.empty: 
        return df
    else:
        # abans de res li canviem les columnes de longitud i latitud per si s'han de mapejar despres...
        df.rename(columns={'latitud':'lat', 'longitud':'lon'}, inplace=True)
        # ara filtrem per a totes les estacions de l'estudi, segons estacions["nom_eoi"]:
        return df[df.nom_estacio.isin(ESTACIONS["nom_eoi"])]


# ---------------------------------------------------------------------------------------------------------------------
def get_contaminant_data(ymd, contaminante = 'NO2'):
    # obtenim les dades d'un contaminant per a totes les les estacions del projecte en una data determinada
    df = get_all_EOI_data(ymd)
    if df.empty: 
        return df
    else:
        return df[df.contaminant.eq(contaminante)]


# ---------------------------------------------------------------------------------------------------------------------
def get_data(ymd, nom_eoi, contaminante = 'NO2'):
    df = get_contaminant_data(ymd, contaminante)
    if df.empty:
        return df
    else:
        return df[df.nom_estacio.eq(nom_eoi)]


def get_CM(df):
    if df.empty:
        # retornem el centre del BBOX que defineix Catalunya lon [0,3] i lat [40.0 43.0]
        return 1.75, 41.5
    else:
        # obtenim el centre de masses definit per (lon,lat):
        return df.lon.mean(), df.lat.mean()
        
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
