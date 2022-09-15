#Librerias
    #Manipulacion de datos
import os
import pandas as pd
import numpy as np
"""   #SIG
import geopandas as gpd
import shapely.geometry 
from pyproj import CRS
from shapely.geometry import Point, LineString, Polygon
"""  #Graficacion
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
    #Dash
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

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
             'CAMPANA':'Fecha de muestreo'}
#Formulas para los callbacks
def graf_diver_fauna(DataFrame, campana):
    """
    Grafica en el mapa los puntos de muestreo junto con la diversidad de especies de flora fustal de cada uno, discriminado
    por época de muestreo.
    - Inputs: DataFrame generado por la función tabla_diversidad.
    - Outputs: Gráfico de Plotly
    """
    val_max = max(DataFrame.N_ESPECIES)
    display = []
    for element in DataFrame.CAMPANA:
        if len(element) == 6:
            display.append(element.replace('-','-0'))
        else:
            display.append(element)
    DataFrame['CAMPANA'] = pd.Series(display)
    DataFrame = DataFrame[DataFrame['CAMPANA'] == campana]
    fig = px.scatter_mapbox(DataFrame, lat="LAT", lon="LON", hover_name="ID_MUES_PT", hover_data=["N_ESPECIES"], 
                        color="N_ESPECIES", color_continuous_scale="rainbow", zoom=10, height=300, labels=cod_campos, 
                        range_color=[0,val_max])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":1,"l":1,"b":0})
    
    return fig
    
def graf_diver_fauna_slider(DataFrame):
    """
    Grafica en el mapa los puntos de muestreo junto con la diversidad de especies de flora fustal de cada uno, discriminado
    por época de muestreo.
    - Inputs: DataFrame generado por la función tabla_diversidad.
    - Outputs: Gráfico de Plotly
    """
    display = []
    for element in DataFrame.CAMPANA:
        if len(element) == 6:
            display.append(element.replace('-','-0'))
        else:
            display.append(element)
    DataFrame['CAMPANA'] = pd.Series(display)
    DataFrame = DataFrame.sort_values(by='CAMPANA')
    fig = px.scatter_mapbox(DataFrame, lat="LAT", lon="LON", animation_frame='CAMPANA', hover_name="ID_MUES_PT", hover_data=["N_ESPECIES"], 
                        color="N_ESPECIES", color_continuous_scale="rainbow", zoom=10, height=300, labels=cod_campos, 
                        range_color=[0,max(DataFrame.N_ESPECIES)])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":1,"l":1,"b":0})
    fig["layout"].pop("updatemenus")
    return fig

def graficar_tro_fauna(DataFrame, campana = 'Todas'):
    """
    if campana == 'Todas':
        None
    else:
        DataFrame = DataFrame[DataFrame.CAMPANA == campana]
    
    lats = []
    lons = []
    names = []
    num_sp = []

    for feature, name, num in zip(DataFrame.geometry, DataFrame.ID_MUES_TR, DataFrame.N_ESPECIES):
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
            
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            num_sp = np.append(num_sp, [num]*len(y))
            names = np.append(names,[name]*len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            num_sp = np.append(num_sp, None)
            
    fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names, color=names, hover_data=[num_sp], zoom=11,
                         labels={'hover_data_0':'No. especies','color':'ID transecto','lat':'Latitud','lon':'Longitud'})
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.update_geos(fitbounds="locations")
    
    return fig
"""
def graf_cober_fauna(DataFrame, campana, dic=cod_campos):
    """
    Grafica en el mapa los puntos de muestreo junto con la cobertura donde se encuentra cada uno, discriminado
    por época de muestreo. Si no se especifica una época se grafican todas.
    - Inputs: DataFrame generado por la función tabla_diversidad.
    - Outputs: Gráfico de Plotly
    """
    if campana == 'Todas':
        DataGraf = DataFrame
    else:
        DataGraf = DataFrame[DataFrame.CAMPANA == campana]
    
    fig = px.scatter_mapbox(DataGraf, lat="LAT", lon="LON", hover_name="ID_MUES_PT", hover_data=["N_ESPECIES"], 
                        color='N_COBERT', zoom=10, height=300, labels=dic)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

def graf_char_fauna(DataFrame, caracter, campana='Todas', dic=cod_campos):
    """
    Grafica en el mapa los puntos de muestreo junto con la diversidad de especies de flora fustal de cada uno, discriminado
    por época de muestreo. Si no se especifica una época se grafican todas.
    - Inputs: DataFrame generado por la función tabla_diversidad.
    - Outputs: Gráfico de Plotly
    """
    if campana == 'Todas':
        DataGraf = DataFrame
    else:
        DataGraf = DataFrame[DataFrame.CAMPANA == campana]
    
    fig = px.scatter_mapbox(DataGraf, lat="LAT", lon="LON", hover_name="ID_MUEST", hover_data=[caracter], 
                            color=caracter, color_continuous_scale="rainbow", zoom=10, height=300, 
                            labels=dic)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

def info_pto_fauna(DataFrame, punto, caracter, dic=cod_campos):
    
    data = DataFrame[DataFrame.ID_MUES_PT == punto].reset_index()
    data[caracter] = data[caracter].round(2)
    fig = px.bar(data, y='NOM_DESP', x=caracter, color=caracter,
                 title="{car} punto {pun}, campaña {camp}".format(
                car =cod_campos[caracter], pun=punto, camp=data.at[0,'CAMPANA']),
                labels = dic, orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

def graf_bar_f(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Sum of NUM_IND"],
    ))
    return fig

def graf_bar_f2(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Sum of ABUND_ABS"],
    ))
    return fig

def graf_bar_v(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Average of BIOM_INDIV"],
    ))
    return fig

def graf_bar_h(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["DENS_CANTI"],
    ))
    return fig

def graf_bar_m(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["Sum of NUM_OTU"],
    ))
    return fig

#Lectura de datos: Estas son tablas resumidas y procesadas por el codigo anterior (Fauna.ipynb)

fp = r"" #Reemplazar con la ruta correpondiente

#acum_fauna_pso_esp = pd.read_csv(os.path.join(fp, "acum_fauna_pso_esp.csv"))
#acum_fauna_pto_esp = pd.read_csv(os.path.join(fp, "acum_fauna_pto_esp.csv"))
#div_fauna_pso = pd.read_csv(os.path.join(fp, "div_fauna_pso.csv"))
#div_fauna_pto = pd.read_csv(os.path.join(fp, "div_fauna_pto.csv"))
#div_fauna_tro = gpd.read_file(os.path.join(fp, "div_fauna_tro.shp")) #Ojo! Este es un GeoDataFrame

#fauna
df_raw = pd.read_csv(os.path.join(fp, "Fauna_Specie.csv"))
df1 = df_raw.sort_values(by='Sum of NUM_IND',ascending=False)
df1a = df_raw.sort_values(by='Sum of ABUND_ABS',ascending=False)

#Vegtacion
dv_raw = pd.read_csv(os.path.join(fp, "Especies_Vegetales_Kale.csv"))
dv1 = dv_raw.sort_values(by='Average of BIOM_INDIV',ascending=False)
dv1a = dv_raw.sort_values(by='Average of CARB_INDIV',ascending=False)

dv_raw2 = pd.read_csv(os.path.join(fp, "Especies_Vegetales_Platero.csv"))
dv2 = dv_raw2.sort_values(by='Average of BIOM_INDIV',ascending=False)
dv2 = dv_raw2.sort_values(by='Average of CARB_INDIV',ascending=False)

#Hidrobiota
dh1 = pd.read_csv(os.path.join(fp, "HidrobiotaKale1.csv"))

dh2 = pd.read_csv(os.path.join(fp, "HidrobiotaPlatero1.csv"))

#Metabarcoding
dmt1 = pd.read_csv(os.path.join(fp, "MetabarcodingKale1.csv"))

dmt2 = pd.read_csv(os.path.join(fp, "MetabarcodingPlatero1.csv"))

#Figuras de base

#fig1 = graf_cober_fauna(div_fauna_pto, campana='Todas')
#fig2 = graf_diver_fauna(div_fauna_pto,'2021-01')
#fig3 = info_pto_fauna(acum_fauna_pto_esp, 'PO23LL_ZP', 'NUM_IND')
#fig4 = graf_diver_fauna_slider(div_fauna_pso)
#fig5 = info_pto_fauna(acum_fauna_pso_esp, 'A14', 'NUM_IND')
#fig6 = graficar_tro_fauna(div_fauna_tro, '2021-3')
fig4 = graf_bar_f(df1)
fig4a = graf_bar_f2(df1a)


fig5 = graf_bar_v(dv1)
fig6 = graf_bar_v(dv2)

fig7 = graf_bar_h(dh1)
fig8 = graf_bar_h(dh2)
fig9 = graf_bar_m(dmt1)
fig10 = graf_bar_m(dmt2)

#Displays para Dash

display_proy = {'kale':'Proyecto Kalé','platero':'Proyecto Platero'}
#display_camp = list(div_fauna_pto.CAMPANA.drop_duplicates().sort_values())
#display_camp.append('Todas')
#display_fauna_pto = list(acum_fauna_pto_esp.ID_MUES_PT.drop_duplicates().sort_values())
#display_fauna_tro = list(div_fauna_tro.ID_MUES_TR.drop_duplicates().sort_values())
display_fauna_char = {'NUM_IND':'Abundancia'}

#Componentes de Dash

fauna_kale = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Fauna de Kalé", className="card-text"),
                html.P("Aquí debería ir un texto contando en qué consiste el componente y qué se va a mostrar, por ejemplo qué metodos se hacen en cada punto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H3("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            
            html.Div([
                dcc.Graph(figure=fig4, id = "figf1"),
                dcc.Graph(figure=fig4a, id = "figf1a")
                #dcc.Slider(0, (len(display_camp)-1), id='selector_epoca_diversidad', 
                #marks= dict(zip(range(len(display_camp)),display_camp)), step=None,
                #className="one-half column pretty-container"),

                #dcc.Graph(figure=fig2, id='diversidad_fauna',className="one-half column pretty-container",
                #style={'height':'50rem','overflow':'scroll','padding':'3rem',"margin-left": "10px","margin-right": "5px"}),

                #dcc.Graph(figure=fig3, id='pto_fauna',className="one-half column pretty-container",
                #style={'height':'50rem','overflow':'scroll','padding':'3rem',"margin-left": "10px","margin-right": "5px"})
                ])
    ]),
    className="mt-3",
)

flora_kale = dbc.Card(
    dbc.CardBody([
            html.H3("Componente flora de Kale", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig5, id = "figv1")
            ])
        ]
    ),
    className="mt-3",
)

hidrobiota_kale = dbc.Card(
    dbc.CardBody([
            html.H3("Componente Hidrobiota de Kale", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig7, id = "figh1")
            ])
        ]
    ),
    className="mt-3",
)

metabarcoding_kale = dbc.Card(
    dbc.CardBody([
            html.H3("Componente Metabarcoding de Kale", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig9, id = "figmt1")
            ])
        ]
    ),
    className="mt-3",
)

paisaje_kale = dbc.Card(
    dbc.CardBody([
            html.H3("Componente paisaje", className="card-text"),
            html.Div([
            ])
        ]
    ),
    className="mt-3",
)

tabs_kale = dcc.Tabs(
            [
                dcc.Tab(fauna_kale, label="Fauna",className = 'font_size', 
                #style=tab_style, selected_style=tab_selected_style
                ),
                dcc.Tab(flora_kale, label="Flora"),
                dcc.Tab(hidrobiota_kale, label="Hidrobiota"),
                dcc.Tab(metabarcoding_kale, label="Metabarcoding"),
                dcc.Tab(paisaje_kale, label="Paisaje")
            ]
        )

fauna_platero = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Componente Fauna de Platero", className="card-text"),
            html.Div([
                
            ])
        ]
    ),
    className="mt-3",
)

flora_platero = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Componente Flora de Platero", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig6, id = "figv2")
            ])
        ]
    ),
    className="mt-3",
)

hidrobiota_platero = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Componente Hidrobiota de Platero", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig8, id = "figh2")
            ])
        ]
    ),
    className="mt-3",
)

metabarcoding_platero = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Componente Metabarcoding de Platero", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig10, id = "figmt2")
            ])
        ]
    ),
    className="mt-3",
)

paisaje_platero = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Componente Paisaje de Platero", className="card-text"),
            html.Div([
            ])
        ]
    ),
    className="mt-3",
)

tabs_platero = dcc.Tabs(
            [
                dcc.Tab(fauna_platero, label="Fauna",className = 'font_size', 
                #style=tab_style, selected_style=tab_selected_style
                ),
                dcc.Tab(flora_platero, label="Flora"),
                dcc.Tab(hidrobiota_platero, label="Hidrobiota"),
                dcc.Tab(metabarcoding_platero, label="Metabarcoding"),
                dcc.Tab(paisaje_platero, label="Paisaje")
            ]
        )

#App de Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div(
            [html.Img(src="assets/positivo_recortado.png",id="logocdt",className="logocdt",
            style={
                                "height": "70px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            }
            )],className="control column"),
        html.Div(
            [html.H3("Estudio de Impacto Ambiental",id="titulo1",
            style={"margin-bottom": "0px", 'textAlign': 'center','font-weight':'bold'}
            ),
             html.H5("Curaduría de Ecosistemas",id="titulo2",
             style={"margin-bottom": "0px", 'textAlign': 'center'}
             )],className="map column")],id="header",className="row flex-display"),

    html.Div([
        html.H6('Este es el componente de ecosistenas asociado a los PPII... (etc etc'),
        html.H6('Por fvor selecciona un proyecto para ver la información asociada al mismo:'),
        dcc.Dropdown(style={'color':'black'}, options=display_proy, id='select_proyecto', placeholder='Seleccione Proyecto'),
        html.Div(id='info_proyecto')

    ]   
    ),

    html.Div(
            html.Img(

                            src=app.get_asset_url("Institucional_3Logos_letrasblancas.png"),

                            id="logos-image",

                            style={

                                "height": "auto",

                                "max-width": "600px",
                                "margin-top": "25px",

                                "margin-bottom": "25px",

                            }),id="footer"

    )])

@app.callback(Output('info_proyecto','children'),Input('select_proyecto','value'))
def update_info (selected_value):
    if selected_value == 'kale':
        return tabs_kale
    elif selected_value == 'platero':
        return tabs_platero

#@app.callback(Output('diversidad_fauna', 'figure'), Input('selector_epoca_diversidad', 'value'))
#def update_graf_diver_fauna(selected_value):
    #marks = dict(zip(range(len(display_camp)), display_camp))
    #fig2 = graf_diver_fauna(div_fauna_pto, marks[selected_value])
#    return 

if __name__ == "__main__":
    app.run_server(debug=True)


