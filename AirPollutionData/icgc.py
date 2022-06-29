# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from . import dades_obertes

# ---------------------------------------------------------------------------------------------------------------------
LCZ_NAME = {
    '1': 'compact high-rise', '2': 'compact midrise', '3': 'compact low-rise', 
    '4': 'open high-rise', '5': 'open midrise', '6': 'open low-rise', 
    '7': 'lightweight low-rise', '8': 'large low-rise', '9': 'sparsely built', '10': 'heavy industry',
    'A':  'dense trees', 'B': 'scattered trees', 'C': 'bush, scrub', 'D': 'low plants', 
    'E': 'bare rock or paved', 'F': 'bare soil or sand', 'G': 'water'
    }


LCZ_DEFINITION = {
    '1': 'Dense mix of tall buildings to tens of stories. Few or no trees. Land cover mostly paved. Concrete, steel, stone and glass construction materials.', 
    '2': 'Dense mix of midrise buildings (3–9 stories). Few or no trees. Land cover mostly paved. Stone, brick, tile, and concrete construction materials.', 
    '3': 'Dense mix of low-rise buildings (1–3 stories). Few or no trees. Land cover mostly paved. Stone, brick, tile, and concrete construction materials.', 
    '4': 'Open arrangement of tall buildings to tens of stories. Abundance of pervious land cover (low plants, scattered trees). Concrete, steel, stone, and glass construction materials.', 
    '5': 'Open arrangement of midrise buildings (3–9 stories). Abundance of pervious land cover (low plants, scattered trees). Concrete, steel, stone, and glass construction materials.', 
    '6': 'Open arrangement of low-rise buildings (1–3 stories). Abundance of pervious land cover (low plants, scattered trees). Wood, brick, stone, tile, and concrete construction materials.',
    '7': 'Dense mix of single-story buildings. Few or no trees. Land cover mostly hard-packed. Lightweight construction materials (e.g., wood, thatch, corrugated metal).', 
    '8': 'Open arrangement of large low-rise buildings (1–3 stories). Few or no trees. Land cover mostly paved. Steel, concrete, metal, and stone construction materials.', 
    '9': 'Sparse arrangement of small or medium-sized buildings in a natural setting. Abundance of pervious land cover (low plants, scattered trees).', 
    '10': 'Low-rise and midrise industrial structures (towers, tanks, stacks). Few or no trees. Land cover mostly paved or hard-packed. Metal, steel, and concrete construction materials.',
    'A': 'Heavily wooded landscape of deciduous and/or evergreen trees. Land cover mostly pervious (low plants). Zone function is natural forest, tree cultivation, or urban park.', 
    'B': 'Lightly wooded landscape of deciduous and/or evergreen trees. Land cover mostly pervious (low plants). Zone function is natural forest, tree cultivation, or urban park.', 
    'C': 'Open arrangement of bushes, shrubs, and short, woody trees. Land cover mostly pervious (bare soil or sand). Zone function is natural scrubland or agriculture.', 
    'D': 'Featureless landscape of grass or herbaceous plants/crops. Few or no trees. Zone function is natural grassland, agriculture, or urban park.', 
    'E': 'Featureless landscape of rock or paved cover. Few or no trees or plants. Zone function is natural desert (rock) or urban transportation.', 
    'F': 'Featureless landscape of soil or sand cover. Few or no trees or plants. Zone function is natural desert or agriculture.',
    'G': 'Large, open water bodies such as seas and lakes, or small bodies such as rivers, reservoirs, and lagoons.'
    }


# Valores de propiedades geometricas y de cobertura de superficie para zonas climaticas locales. 
# Todas las propiedades no tienen unidades, excepto la altura de los elementos de rugosidad (m).    
# LCZ_PROPERTIES = {'lcz': [ 'Sky view factor', 'Espaciado entre edificios/arboles', 'Fraccion edificios', 'Fraccion impermeable', 'Fraccion permeable', 'Altitud edificios', 'Rugosidad del terreno (m)'] }
# LCZ_PROPERTIES = {
#    '1': ['0.2-0.4',  '>2.0',      '40-60', '40-60', '<10',   '>25',   '8'],
#    '2': ['0.3-0.6',  '0.75-2.0',  '40-70', '40-70', '<20',   '10-25', '6-7'],
#    '3': ['0.2-0.6',  '0.75-1.5',  '40-70', '40-70', '<30',   '3-10',  '6'],
#    '4': ['0.5-0.7',  '0.75-1.25', '20-40', '20-40', '30-40', '>25',   '7-8'],
#    '5': ['0.5-0.8',  '0.3-0.75',  '20-40', '20-40', '20-40', '10-25', '5-6'],
#    '6': ['0.6-0.9',  '0.3-0.75',  '20-40', '20-40', '30-60', '3-10',  '5-6'],
#    '7': ['0.2-0.5',  '1.0-2.0',   '60-90', '60-90', '<30',   '2-4',   '4-5'],
#    '8': ['>0.7',     '0.1-0.3',   '30-50', '30-50', '<20',   '3-10',  '5'],
#    '9': ['>0.8',     '0.1-0.25',  '10-20', '10-20', '60-80', '3-10',  '5-6'],
#    '10': ['0.6-0.9', '0.2-0.5',   '20-30', '20-30', '40-50', '5-15',  '5-6'],
#    'A': ['<0.4',     '<0.1',      '<10',   '<10',   '>90',   '3-30',  '8'],
#    'B': ['0.5-0.8',  '0.25-0.75', '<10',   '<10',   '>90',   '3-15',  '5-6'],
#    'C': ['0.7-0.9',  '0.25-1.0',  '<10',   '<10',   '>90',   '<2',    '4-5'],
#    'D': ['>0.9',     '<0.1',      '<10',   '>90',   '>90',   '<1',    '3-4'],
#    'E': ['>0.9',     '<0.1',      '<10',   '<10',   '<10',   '<0.25', '1-2'],
#    'F': ['>0.9',     '<0.1',      '<10',   '<10',   '>90',   '<0.25', '1-2'],
#    'G': ['>0.9',     '<0.1',      '<10',   '<10',   '>90',   '-',     '1']
#    }

def get_LCZ_image(lcz):
    return f"LCZ{lcz}.png"


def get_LCZ_station_image(eoi_code):
    return f"{eoi_code}_lcz.jpg"


# ---------------------------------------------------------------------------------------------------------------------
# Vulnerability Urban Climate Index (taula Joan Gilabert). 
# Diccionari del tipus lcz:vuci
VUCI = {
    '1': 100, '2': 80, '3': 70, '4': 70, '5': 60, '6': 50, '7': 60, '8': 50, '9': 30, '10': 70,
    'A':  50, 'B': 30, 'C': 30, 'D': 20, 'E': 40, 'F': 10, 'G': 20
    }


# ---------------------------------------------------------------------------------------------------------------------
def get_VUCI(lcz):
    return VUCI.get(lcz, 0)


# ---------------------------------------------------------------------------------------------------------------------
# VUCI_CVP scenarios
#
# A1 ... Extremadamente vulnerable
# A2 ... Muy vulnerable
# B  ... Vulnerable
# C1 ... Vulnerable VUCI, poco vulnerable CVP
# C2 ... Poco vulnerable VUCI, vulnerable CVP
# D  ... Poco vulnerable
#-------------------------------------------------------
#            | cvp<50 | 50<cvp<60 | 60<cvp<70 | 70<cvp |
#-------------------------------------------------------
# vuci<50    |   D    |   C2      |   C2      |   C2   |
# 50<vuci<60 |   C1   |   B       |   B       |   B    |
# 60<vuci<70 |   C1   |   B       |   A2      |   A2   |
# 70<vuci    |   C1   |   B       |   A2      |   A1   |
#-------------------------------------------------------
def get_scenario(vuci, cvp):
    if vuci < 50:
        if cvp <50:
            return "D", "Poco vulnerable"
        else:
            return "C2", "Poco vulnerable VUCI, vulnerable CVP"
    elif vuci < 60:
        if cvp <50:
            return "C1", "Vulnerable VUCI, poco vulnerable CVP"
        else:
            return "B", "Vulnerable"
    elif vuci < 70:
        if cvp <50:
            return "C1", "Vulnerable VUCI, poco vulnerable CVP"
        elif cvp < 60:
            return "B", "Vulnerable"
        else:
            return "A2", "Muy vulnerable"
    else:
        if cvp <50:
            return "C1", "Vulnerable VUCI, poco vulnerable CVP"
        elif cvp < 60:
            return "B", "Vulnerable"
        elif cvp < 70:
            return "A2", "Muy vulnerable"
        else:
            return "A1", "Extremadamente vulnerable"


# ---------------------------------------------------------------------------------------------------------------------
def get_df_histograma_hores(contaminante, df):
    # df es el registre que conte els valors horaris del contaminant.
    # Aixo vol dir que df.shape[0] == 1
    value_list = [ df[h].iloc[0]  if h in df.columns  else 0.0  for h in dades_obertes.HORES ]
    return pd.DataFrame(np.array(value_list), columns=[f"{contaminante}"])


# ---------------------------------------------------------------------------------------------------------------------
def get_hazard_data(contaminante, df):
    # df es el registre que conte els valors horaris del contaminant.
    # Aixo vol dir que df.shape[0] == 1
    value_list = [ df[h].iloc[0]  if h in df.columns  else np.nan  for h in dades_obertes.HORES ]
    return round(np.nanmean(np.array(value_list), dtype=np.float64), 2)


# ---------------------------------------------------------------------------------------------------------------------
# Conversión Urban Atlas a LCZ urbanas. (taula 6.1 tesis JGilabert)
# Urban Atlas <-> LCZ
# 'Tejido urbano continuo': ['1', '2', '3']
# 'Tejido urbano denso discontinuo': ['4', '5', '6']
# 'Tejido urbano discontinuo de densidad media': ['5', '6']
# 'Tejido urbano discontinuo de baja densidad': ['6']
# 'Tejido urbano discontinuo de muy baja densidad': ['6']
# 'Estructuras aisladas': ['9']
# 'Unidades industriales, comerciales, públicas y privadas': ['1', '2', '3', '4', '5', '6']
# 'Carreteras y calles': ['E'] 
# 'Otros caminos y terrenos asociados': ['E']
# 'Ferrocarriles': ['E']
# 'Zona portuaria': ['E']
# 'Aeropuerto': ['E']
# 'Extracción de minerales': ['E']
# 'Sitios de construcción': ['E']
# 'Terreno sin uso actual': ['F']
# 'Verde Urbano': ['B','D']
# 'Instalaciones deportivas': ['D']
# 'Huertos urbanos': ['B']
# 'Zonas de vegetación herbácea': ['B']
# ---------------------------------------------------------------------------------------------------------------------
