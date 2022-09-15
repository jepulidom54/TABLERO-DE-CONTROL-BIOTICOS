#Librerias
#Manipulacion de datos
import os
import pandas as pd
import numpy as np

#SIG
#import geopandas as gpd
#import shapely.geometry 
#from pyproj import CRS
#from shapely.geometry import Point, LineString, Polygon
  
#Graficacion
#import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#Dash
from dash import Dash, dcc, html, Input, Output
#from dash import Dash, dcc, html
#from dash.dependencies import Input, Output
#import dash_bootstrap_components as dbc

#Diccionarios para interpretar los puntos

    #Informacion presente en el EIA sobre a qué habitat corresponde la codificación
cod_puntos = {'VSA':'Vegetacion Secundaria Alta',
              'VSB':'Vegetacion Secundaria Baja',
              'BDAI':'Bosque Denso Alto Inundable',
              'BR':'Bosque de Galeria y/o Ripario',
              'PL':'Pastos Limpios',
              'PEM':'Pastos Enmalezados',
              'PARB':'Pastos Arbolados',
              'HDINA':'Herbazal Denso Inundable No Arbolado',
              'HDIA':'Herbazal Denso Inundable Arbolado'}
    #Caracteristica y unidades de cada uno de los puntos cuantitativos de la tabla

cod_campos ={'ESPECIE':'Especie',
             'ABUN':'Abundancia (Ind.)',
             'DAP_INDIV':'Diametro (m)',
             'AB_INDIV':'Area Basal (m2)',
             'H_TOTAL':'Altura Total (m)',
             'H_FUSTE':'Altura Fuste (m)',
             'VOL_TOTAL':'Volumen Total (m3)',
             'VOL_COM':'Volumen Comercial (m3)',
             'BIOM_INDIV':'Biomasa (kg)',
             'CARB_INDIV':'Carbono (kg)',
             'NUM_IND':'Abundancia',
             'NOM_DESP':'Especie',
             'LAT':'Latitud',
             'LON':'Longitud',
             'N_COBERT':'Cobertura',
             'N_ESPECIES':'No. de especies',
             'CAMPANA':'Fecha de muestreo',

             'OBJECTID':'OBJECTID',
             'EXPEDIENTE':'EXPEDIENTE',
             'ID_METAB':'ID_METAB',
             'FEAT_CLASS':'FEAT_CLASS',
             'ID_MUESTRA':'ID_MUESTRA',
             'LABORAT':'LABORAT',
             'COD_LAB':'COD_LAB',
             'FEC_MUEST':'FECHA',
             'ESTACIONAL':'ESTACIONAL',
             'HORA':'HORA',
             'FEC_ANALIS':'FECHA_ANALISIS',
             'T_SUSTR':'TIPO_SUSTRATO',
             'UMBRAL_SIMIL':'UMBRAL_SIMILITUD',
             'READS':'READS',
             'MARCADOR':'MARCADOR',
             'N_COBERT':'N_COBERTURA',
             'PROF_MUES':'PROF_MUESTRA',
             'MET_PRES':'MET_PRES',
             'PROT_MUEST':'PROT_MUESTRA',
             'ESFU_MUEST':'ESFU_MUESTRA',
             'CANT_MUEST':'CANT_MUESTRA',
             'BD_REF':'BD_REF',
             'V_BD_REF':'V_BD_REF',
             'OTU_PHYLUM':'OTU_PHYLUM',
             'OTU_CLASE':'OTU_CLASE',
             'OTU_ORDEN':'OTU_ORDEN',
             'OTU_FAM':'OTU_FAM',
             'OTU_GEN':'OTU_GEN',
             'OTU_ESP':'OTU_ESP',
             'N_LECT_TOT':'N_LECT_TOT',
             'NUM_REP':'NUM_REP',
             'SECU_F_R':'SECU_F_R',
             'TEC_SEC':'TEC_SEC',
             'SOFT_AB':'SOFT_AB',
             'NUM_OTU':'NUM_OTU',
             'OBSERV':'OBSERVACION'}

#Lectura de datos: Estas son tablas resumidas y procesadas por el codigo anterior (Fauna.ipynb)

fp = r"" #Reemplazar con la ruta correpondiente

dv = pd.read_csv(os.path.join(fp, "Especies_Vegetales_Kale.csv"))
dv1=dv.sort_values(by='Average of VOL_TOTAL')
dv2=dv.sort_values(by='Average of CARB_INDIV')

#-----------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Puntos de Muestreo Vegetacion'),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        dv['Key1'].min(),
        dv['Key1'].max(),
        step=100,
        value=dv['Key1'].max(),
        marks=range((len(dv['Key1'])),dv['Key1']),
        #marks=str(Key1): str(Key1) for Key1 in df['Key1']},
        id='Key1-slider'
    )
])

@app.callback(Output('graph-with-slider', 'figure'),
                Input('Key1-slider', 'value'))
def update_figure(Selected_Key1):
    filtered_df = dv[dv.Key1 < Selected_Key1]

    fig = px.scatter(filtered_df, x="Average of VOL_TOTAL", y="Average of CARB_INDIV",
                     size="Average of VOL_TOTAL", color="Row Labels", hover_name="Row Labels", size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

    