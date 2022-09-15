#Librerias
#Manipulacion de datos
import os
import pandas as pd

#SIG
#import geopandas as gpd
#import shapely.geometry 
#from pyproj import CRS
#from shapely.geometry import Point, LineString, Polygon
  
#Graficacion
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#Dash
#from dash import Dash, dcc, html, Input, Output
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
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


#Formulas para los callbacks

#Lectura de datos: Estas son tablas resumidas y procesadas por el codigo anterior (Fauna.ipynb)

fp = r"" #Reemplazar con la ruta correpondiente

dh = pd.read_csv(os.path.join(fp, "Hidrobiota1.csv"))
dh1=dh.sort_values(by='DENS_CANTI')
dh2=dh.sort_values(by='UNIDAD_DEN')
dh3=dh.sort_values(by='ABUND_REL')

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=dh1["Punto"],
    y=dh1["DENS_CANTI"],
    ))
#fig1.show()

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=dh2["Punto"],
    y=dh2["UNIDAD_DEN"],
    ))
#fig2.show()

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=dh3["Punto"],
    y=dh3["ABUND_REL"],
    ))
#fig3.show()

#-----------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Puntos de Muestreo Factor Hidrobiotico'),
    dcc.Tabs(id="tabsgraph", value='tab-1graph', children=[
        dcc.Tab(label='Densidad', value='tab-1graph'),
        dcc.Tab(label='Unidad', value='tab-2graph'),
        dcc.Tab(label='Abundacia relativa', value='tab-3graph'),
    ]),
    html.Div(id='tabs-contentgraph')
])

@app.callback(Output('tabs-contentgraph', 'children'),
              Input('tabsgraph', 'value'))
def render_content(tab):
    if tab == 'tab-1graph':
        return html.Div([
            html.H3('Densidad'),
            dcc.Graph(
                id='graph-1-tabs-dcc',
                figure= fig1
            )
        ])
    if tab == 'tab-2graph':
        return html.Div([
            html.H3('Unidad'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure= fig2
            )
        ])
    elif tab == 'tab-3graph':
        return html.Div([
            html.H3('Abundancia Relativa'),
            dcc.Graph(
                id='graph-3-tabs-dcc',
                figure= fig3
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)

"""
H=np.array(pd.read_csv('C:/Users/jepul/OneDrive/Escritorio/Curaduria PPII/Kale/Datos de Vegetacion y CO2/Hidrobiota1.csv', delimiter=',', header=None))

key_M=np.asarray(H[1:,0],dtype=float)
Punto_M=np.asarray(H[1:,1],dtype=str)

NUM_REP= np.asarray(H[1:,2],dtype=float)
N_LECT_TOT= np.asarray(H[1:,3],dtype=float)
print()
plt.figure(figsize=(12,5))
plt.plot(N_LECT_TOT, N_LECT_TOT,'o')
plt.xlabel('N_LECT_TOT')
plt.ylabel('N_LECT_TOT')
plt.grid()

dh
"""