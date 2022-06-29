# -*- coding: utf-8 -*-
# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.CO

import os
import numpy as np
import pandas as pd

import streamlit as st
import pydeck as pdk

import operator

import AirPollutionData


CWD = os.getcwd()

def get_information_about_data(eoi_name, ymd, contaminante, df):
    if df.empty:
        return f"No {contaminante} for {eoi_name} in {ymd}"
    elif df.shape[0] != 1:
        return f"Insconsistent {contaminante} for {eoi_name} in {ymd} data"
    else:
        return f"{contaminante} for station {eoi_name} ({eoi_code}) in {ymd}"

        
        
def get_station_map_data(df):
    # obtenemos los datos necesarios de las estaciones del proyecto que estan almacenadas en AirPollutionData.ESTACIONS y AirPollutionData.EOI_DF
    # a partir de ellas calcularemos las capas que queremos mostrar en el mapa.
    llocs = AirPollutionData.EOI_DF[['lon','lat','etiqueta']]
    
    # calculamos el punto central del conjunto de estaciones.
    lonCM, latCM = AirPollutionData.get_CM(llocs)

    # definimos la capa d'estaciones del proyecto
    layerS = pdk.Layer("ScatterplotLayer", 
        data = llocs, 
        get_position = ['lon','lat'], 
        auto_highlight = True,
        get_radius = 500, 
        get_color = '[0,0,255,75]', 
        pickable = True )
    
    # definimos ahora la capa d'etiquetas (labels) de las estaciones
    layerL = pdk.Layer("TextLayer", 
        data = llocs, 
        get_position = ['lon','lat'], 
        get_text = 'etiqueta', 
        get_color = '[0,0,255]', 
        get_size = 12, 
        get_alignment_baseline = "'bottom'" )

    # ahora nos falta la capa de la estacion escogida, si es que hay datos asociados
    if df.empty:
        selected_layers = [layerS, layerL]
    else:
        layerP = pdk.Layer("ScatterplotLayer", 
            data =  df[['lon','lat','codi_eoi']], 
            get_position = ['lon','lat'], 
            auto_highlight = True,
            get_radius = 500, 
            get_color = '[255,0,255,150]', 
            pickable = True )

        selected_layers = [layerS, layerL, layerP]

    # Una vez tenemos las capas que queremos poner en el mapa (selected_layers), vamos a definir el mapa base. 
    # Cambiamos mapbox (default) per ICGC contextmaps: mapstyle = "mapbox://styles/mapbox/light-v9"
    map_style = "https://geoserveis.icgc.cat/contextmaps/icgc_mapa_base_gris_simplificat.json"
    
    # Y ahora definimos la vista inicial:
    init_view_state = pdk.ViewState(latitude=latCM, longitude=lonCM, zoom=10)
    
    return ( map_style, init_view_state, selected_layers )


class AirPollutionRisk:
    def __init__(self, contaminante, eoi_code, df):
        # calculamos los porcentajes de cada LCZ, que se almacenan en un diccionario {lcz:%}
        # devolvemos tambien el codigo de LCZ maximo
        self.lcz_dict, self.lcz_max = AirPollutionData.get_LCZmax(eoi_code)
        
        # obtenemos el Vulnerability Urban Climate Index (VUCI): 
        self.vuci = AirPollutionData.get_VUCI(self.lcz_max)
    
        # calculamos el Climate Vulnerable People Index (CVPI):
        self.cvpi = AirPollutionData.get_CVP(eoi_code, 1)

        # ahora determinamos el VUCI-CVPI escenario
        self.scenario_code, self.scenario_name = AirPollutionData.get_scenario(self.vuci, self.cvpi)

        self.no2_19 = AirPollutionData.get_NO2_2019(eoi_code)
        if df.empty:
            self.hazard_value = np.nan
        else:
            self.hazard_value = AirPollutionData.get_hazard_data(contaminante, df)
            
        #risk = hazard * scenario            


# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON (1rst sentence Streamlit!!!)
    st.set_page_config(layout="wide", page_title="Test Streamlit Qualitat Aire Dataset", page_icon=":earth:")

    st.title("Geospatial System of Air Pollution Data and Local Climate Zones in the AMB")
    st.markdown("""
       Cities are growing fast and LCZs are a new way of classifying urban areas. 
       We know that air pollution is a factor that internally affects humans and their health. 
       It has direct repercussions on the human being and its analysis helps to know and understand what we must do to mitigate the damage.
       
       This viewer contains cross information between the classifications of the LCZs and air quality data, 
       with NO2 and PM2.5 concentrations as target pollutants, at the Barcelona Metropolitan Area (AMB).
       """)
    #st.latex(r''' a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right) ''')

    # ======================================================
    row1_1, row1_2 = st.columns((2,3))
    
    row1_1.subheader(f"Select ...")
    # escogemos el nombre de la estacion de la cual queremos consultar los datos
    eoi_name = row1_1.selectbox("station:", pd.DataFrame(AirPollutionData.ESTACIONS))  
    # escogemos la fecha que nos interesa, por defecto el dia de la consulta...
    ymd = row1_1.date_input("one day:")
    # Restringimos a los dos contaminantes descritos en el TFM, aunque por defecto trataremos siempre el NO2.
    # contaminante = row1_1.radio("pollutant:", ('NO2', 'PM2.5'))
    #contaminante = row1_1.selectbox("contaminant:", pd.DataFrame(AirPollutionData.CONTAMINANTS)) 
    Contaminante = 'NO2'
    
    # A partir de estos datos, obtenemos los datos (JSON) del dataset de dades obertes.
    # En principio nos tiene que devolver un DataFrame con solo una fila. En caso contrario el DataFrame estara vacio.
    df = AirPollutionData.get_data(ymd, eoi_name, contaminante)

    # Primero, vamos a pintar el mapa de situacion de las estaciones:
    mapstyle, initviewstate, selectedlayers = get_station_map_data(df)
    # row1_2.map(data=df, zoom=13, use_container_width=True)
    row1_2.pydeck_chart( pdk.Deck(map_style = mapstyle, initial_view_state = initviewstate, layers = selectedlayers) )

    # buscamos el codigo de estacion asociado a eoi_name:
    eoi_code = AirPollutionData.get_codi_eoi(eoi_name)
    
    # calculamos todos los datos del riesgo associado al contaminante:
    risk_data = AirPollutionRisk(contaminante, eoi_code, df)
    
    row1_1.write(" ")
    row1_1.subheader(f" NO2 Air Quality Index :")
    #semaforo con risk_data.risk
    row1_1.write(f"LCZ max: {risk_data.lcz_max} >> VUCI: {risk_data.vuci}")
    row1_1.write(f"CVP: {risk_data.cvpi}")
    row1_1.write(f"Scenario: {risk_data.scenario_code} ({risk_data.scenario_name})")
    row1_1.write(f"Hazard ({contaminante}): {risk_data.hazard_value}   |   NO2(2019): {risk_data.no2_19}")
    #row1_1.write(f"Risk: {risk_data.risk}")
    
    # ======================================================
    # Vamos a comprovar si tenemos datos o no y calculamos todos los datos del riesgo asociado al contaminante:
    st.write(f" ")
    st.subheader(get_information_about_data(eoi_name, ymd, contaminante, df))
    
    # ======================================================
    row2_1, row2_2 = st.columns(2)
    # imagen del buffer de LCZ de la estacion escogida (eoi_code)
    row2_1.write(f"LCZ data in {eoi_name} area")
    row2_1.image(f"{eoi_code}_lcz.jpg")
    
    # pintamos ahora el histograma de valores del contaminante...
    if not df.empty:
        row2_2.write(f"{contaminante} data in {eoi_name} ({ymd})")
        row2_2.bar_chart(AirPollutionData.get_df_histograma_hores(contaminante, df))

    # ======================================================
    st.subheader(f"LCZ distribution:")
    # vamos a pintar la informacion asociada a cada LCZ, con la imagen associada
    # el procedimiento va a ser muy rudimentario y seguro que se puede optimizar mas...
    # partimos la columna en 10 subcolumnas (una para cada LCZ)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

    col1.metric("% LCZ 1", risk_data.lcz_dict['1'])
    col1.image("LCZ1.png") # col1.image(AirPollutionData.get_LCZ_image('1'))
    col1.metric(AirPollutionData.LCZ_NAME['1'], "")
    col1.metric("% LCZ A", risk_data.lcz_dict['A'])
    col1.image("LCZA.png") # col1.image(AirPollutionData.get_LCZ_image('A'))
    col1.metric(AirPollutionData.LCZ_NAME['A'], "")

    col2.metric("% LCZ 2", risk_data.lcz_dict['2'])
    col2.image("LCZ2.png") # col2.image(AirPollutionData.get_LCZ_image('2'))
    col2.metric(AirPollutionData.LCZ_NAME['2'], "")
    col2.metric("% LCZ B", risk_data.lcz_dict['B'])
    col2.image("LCZB.png") # col2.image(AirPollutionData.get_LCZ_image('B'))
    col2.metric(AirPollutionData.LCZ_NAME['B'], "")

    col3.metric("% LCZ 3", risk_data.lcz_dict['3'])
    col3.image("LCZ3.png") # col3.image(AirPollutionData.get_LCZ_image('3'))
    col3.metric(AirPollutionData.LCZ_NAME['3'], "")
    col3.metric("% LCZ C", risk_data.lcz_dict['C'])
    col3.image("LCZC.png") # col3.image(AirPollutionData.get_LCZ_image('C'))
    col3.metric(AirPollutionData.LCZ_NAME['C'], "")

    col4.metric("% LCZ 4", risk_data.lcz_dict['4'])
    col4.image("LCZ4.png") # col4.image(AirPollutionData.get_LCZ_image('4'))
    col4.metric(AirPollutionData.LCZ_NAME['4'], "")
    col4.metric("% LCZ D", risk_data.lcz_dict['D'])
    col4.image("LCZD.png") # col4.image(AirPollutionData.get_LCZ_image('D'))
    col4.metric(AirPollutionData.LCZ_NAME['D'], "")

    col5.metric("% LCZ 5", risk_data.lcz_dict['5'])
    col5.image("LCZ5.png") # col5.image(AirPollutionData.get_LCZ_image('5'))
    col5.metric(AirPollutionData.LCZ_NAME['5'], "")
    col5.metric("% LCZ E", risk_data.lcz_dict['E'])
    col5.image("LCZE.png") # col5.image(AirPollutionData.get_LCZ_image('E'))
    col5.metric(AirPollutionData.LCZ_NAME['E'], "")

    col6.metric("% LCZ 6", risk_data.lcz_dict['6'])
    col6.image("LCZ6.png") # col6.image(AirPollutionData.get_LCZ_image('6'))
    col6.metric(AirPollutionData.LCZ_NAME['6'], "")
    col6.metric("% LCZ F", risk_data.lcz_dict['F'])
    col6.image("LCZF.png") # col6.image(AirPollutionData.get_LCZ_image('F'))
    col6.metric(AirPollutionData.LCZ_NAME['F'], "")

    col7.metric("% LCZ 7", risk_data.lcz_dict['7'])
    col7.image("LCZ7.png") # col7.image(AirPollutionData.get_LCZ_image('7'))
    col7.metric(AirPollutionData.LCZ_NAME['7'], "")
    col7.metric("% LCZ G", risk_data.lcz_dict['G'])
    col7.image("LCZG.png") # col7.image(AirPollutionData.get_LCZ_image('G'))
    col7.metric(AirPollutionData.LCZ_NAME['G'], "")
    
    col8.metric("% LCZ 8", risk_data.lcz_dict['8'])
    col8.image("LCZ8.png") # col8.image(AirPollutionData.get_LCZ_image('8'))
    col8.metric(AirPollutionData.LCZ_NAME['8'], "")
    
    col9.metric("% LCZ 9", risk_data.lcz_dict['9'])
    col9.image("LCZ9.png") # col9.image(AirPollutionData.get_LCZ_image('9'))
    col9.metric(AirPollutionData.LCZ_NAME['9'], "")
    
    col10.metric("% LCZ 10", risk_data.lcz_dict['10'])
    col10.image("LCZ10.png") # col10.image(AirPollutionData.get_LCZ_image('10'))
    col10.metric(AirPollutionData.LCZ_NAME['10'], "")
