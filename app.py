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
def graf_bar_f1(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Sum of NUM_IND"],
    ))
    fig.update_layout(legend_title_text = "Fauna")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Numero de Individuos")
    return fig
def graf_bar_f2(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Sum of ABUND_ABS"],
    ))
    fig.update_layout(legend_title_text = "Fauna")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Abundancia Absoluta")
    return fig
def graf_bar_f3(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Sum of ABUND_REL"],
    ))
    fig.update_layout(legend_title_text = "Fauna")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Abundancia Relativa")
    return fig
def graf_bar_v(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Average of BIOM_INDIV"],
    ))
    fig.update_layout(legend_title_text = "Vegetacion")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Promedio de Biomasa Individual")
    return fig
def graf_bar_v2(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Average of CARB_INDIV"],
    ))
    fig.update_layout(legend_title_text = "Vegetacion")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Promedio de Carbono Capturado")
    return fig
def graf_bar_v3(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Species"],
    y=DataFrame["Count of ID_INDV_MU"],
    ))
    fig.update_layout(legend_title_text = "Vegetacion")
    fig.update_xaxes(title_text="Especies")
    fig.update_yaxes(title_text="Numero de Individuos")
    return fig 
def graf_scatt(DataFrame):
    fig = go.Figure()
    fig = px.scatter(DataFrame, x="Average of BIOM_INDIV", y="Average of CARB_INDIV",
                     size="Count of ID_INDV_MU", color="Species", hover_name="Species", size_max=55)
    fig.update_layout(transition_duration=500)
    return fig
def graf_bar_h(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["DENS_CANTI"],
    ))
    fig.update_layout(legend_title_text = "Hidrobiologico")
    fig.update_xaxes(title_text="Puntos de Muestreo")
    fig.update_yaxes(title_text="Densidad Cantidad")
    return fig
def graf_bar_h2(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["UNIDAD_DEN"],
    ))
    fig.update_layout(legend_title_text = "Hidrobiologico")
    fig.update_xaxes(title_text="Puntos de Muestreo")
    fig.update_yaxes(title_text="Unidad de Densidad")
    return fig
def graf_bar_h3(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["ABUND_REL"],
    ))
    fig.update_layout(legend_title_text = "Hidrobiologico")
    fig.update_xaxes(title_text="Puntos de Muestreo")
    fig.update_yaxes(title_text="Abundancia Relativa")
    return fig
def graf_bar_m(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["Sum of NUM_OTU"],
    ))
    fig.update_layout(legend_title_text = "Metabarcoding")
    fig.update_xaxes(title_text="Punto de Muestreo")
    fig.update_yaxes(title_text="Cantidad de Especies (OTU)")
    return fig
def graf_bar_m1(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["Sum of NUM_REP"],
    ))
    fig.update_layout(legend_title_text = "Metabarcoding")
    fig.update_xaxes(title_text="Punto de Muestreo")
    fig.update_yaxes(title_text="Cantidad de Especies (OTU)")
    return fig
def graf_bar_m2(DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=DataFrame["Punto"],
    y=DataFrame["Sum of N_LECT_TOT"],
    ))
    fig.update_layout(legend_title_text = "Metabarcoding")
    fig.update_xaxes(title_text="Punto de Muestreo")
    fig.update_yaxes(title_text="Cantidad de Especies (OTU)")
    return fig


#Lectura de datos: Estas son tablas resumidas y procesadas por el codigo anterior (Fauna.ipynb)

fp = r"" #Reemplazar con la ruta correpondiente

#acum_fauna_pso_esp = pd.read_csv(os.path.join(fp, "acum_fauna_pso_esp.csv"))
#acum_fauna_pto_esp = pd.read_csv(os.path.join(fp, "acum_fauna_pto_esp.csv"))
#div_fauna_pso = pd.read_csv(os.path.join(fp, "div_fauna_pso.csv"))
#div_fauna_pto = pd.read_csv(os.path.join(fp, "div_fauna_pto.csv"))
#div_fauna_tro = gpd.read_file(os.path.join(fp, "div_fauna_tro.shp")) #Ojo! Este es un GeoDataFrame

#fauna
df_raw = pd.read_csv(os.path.join(fp, "Fauna_Specie_Kale_ Trayecto.csv"))
df1 = df_raw.sort_values(by='Sum of NUM_IND',ascending=False)
df1a = df_raw.sort_values(by='Sum of ABUND_ABS',ascending=False)
df1b = df_raw.sort_values(by='Sum of ABUND_REL',ascending=False)

df_raw2 = pd.read_csv(os.path.join(fp, "Fauna_Specie_Platero_ Trayecto.csv"))
df2 = df_raw.sort_values(by='Sum of NUM_IND',ascending=False)
df2a = df_raw.sort_values(by='Sum of ABUND_ABS',ascending=False)
df2b = df_raw.sort_values(by='Sum of ABUND_REL',ascending=False)

#Vegtacion
dv_raw = pd.read_csv(os.path.join(fp, "Especies_Vegetales_Kale.csv"))
dv1 = dv_raw.sort_values(by='Average of BIOM_INDIV',ascending=False)
dv1a = dv_raw.sort_values(by='Average of CARB_INDIV',ascending=False)
dv1b = dv_raw.sort_values(by='Count of ID_INDV_MU',ascending=False)

dv_raw2 = pd.read_csv(os.path.join(fp, "Especies_Vegetales_Platero.csv"))
dv2 = dv_raw2.sort_values(by='Average of BIOM_INDIV',ascending=False)
dv2a = dv_raw2.sort_values(by='Average of CARB_INDIV',ascending=False)
dv2b = dv_raw.sort_values(by='Count of ID_INDV_MU',ascending=False)

#Hidrobiota
dh_raw = pd.read_csv(os.path.join(fp, "HidrobiotaKale1.csv"))
dh1 = dh_raw.sort_values(by='DENS_CANTI',ascending=False)
dh1a = dh_raw.sort_values(by='UNIDAD_DEN',ascending=False)
dh1b = dh_raw.sort_values(by='ABUND_REL',ascending=False)

dh_raw2 = pd.read_csv(os.path.join(fp, "HidrobiotaPlatero1.csv"))
dh2 = dh_raw.sort_values(by='DENS_CANTI',ascending=False)
dh2a = dh_raw.sort_values(by='UNIDAD_DEN',ascending=False)
dh2b = dh_raw.sort_values(by='ABUND_REL',ascending=False)

#Metabarcoding
dmt_raw1 = pd.read_csv(os.path.join(fp, "MetabarcodingKale1.csv"))
dmt = dmt_raw1.sort_values(by='Sum of NUM_OTU',ascending=False)
dmta = dmt_raw1.sort_values(by='Sum of NUM_REP',ascending=False)
dmtb = dmt_raw1.sort_values(by='Sum of N_LECT_TOT',ascending=False)

dmt_raw2 = pd.read_csv(os.path.join(fp, "MetabarcodingPlatero1.csv"))
dmt2 = dmt_raw1.sort_values(by='Sum of NUM_OTU',ascending=False)
dmt2a = dmt_raw2.sort_values(by='Sum of NUM_REP',ascending=False)
dmt2b = dmt_raw2.sort_values(by='Sum of N_LECT_TOT',ascending=False)

dmt_raw3 = pd.read_csv(os.path.join(fp, "MetabarcodingKale2.csv"))
dmt3 = dmt_raw3.sort_values(by='Sum of NUM_OTU',ascending=False)
dmt3a = dmt_raw3.sort_values(by='Sum of NUM_REP',ascending=False)
dmt3b = dmt_raw3.sort_values(by='Sum of N_LECT_TOT',ascending=False)

dmt_raw4 = pd.read_csv(os.path.join(fp, "MetabarcodingPlatero2.csv"))
dmt4 = dmt_raw4.sort_values(by='Sum of NUM_OTU',ascending=False)
dmt4a = dmt_raw4.sort_values(by='Sum of NUM_REP',ascending=False)
dmt4b = dmt_raw4.sort_values(by='Sum of N_LECT_TOT',ascending=False)


#Figuras de base

#fig1 = graf_cober_fauna(div_fauna_pto, campana='Todas')
#fig2 = graf_diver_fauna(div_fauna_pto,'2021-01')
#fig3 = info_pto_fauna(acum_fauna_pto_esp, 'PO23LL_ZP', 'NUM_IND')
#fig1 = graf_diver_fauna_slider(div_fauna_pso)
#fig2 = info_pto_fauna(acum_fauna_pso_esp, 'A14', 'NUM_IND')
#fig2 = graficar_tro_fauna(div_fauna_tro, '2021-3')

#fauna kale
fig1 = graf_bar_f1(df1)
fig1a = graf_bar_f2(df1a)
fig1b = graf_bar_f3(df1b)
#fauna platero
fig1c = graf_bar_f1(df2)
fig1d = graf_bar_f2(df2a)
fig1e = graf_bar_f3(df2b)

#vegetacion kale
fig2 = graf_bar_v(dv1)
fig2a = graf_bar_v2(dv1a)
fig2b = graf_bar_v3(dv1b)
figsc_v = graf_scatt(dv_raw)
#vegetacion platero
fig2c = graf_bar_v(dv2)
fig2d = graf_bar_v2(dv2a)
fig2e = graf_bar_v3(dv2b)
figsc_v2 = graf_scatt(dv_raw2)

#hidro kale
fig3 = graf_bar_h(dh1)
fig3a = graf_bar_h2(dh1a)
fig3b = graf_bar_h3(dh1b)
#hidro platero
fig3c = graf_bar_h(dh2)
fig3d = graf_bar_h2(dh2a)
fig3e = graf_bar_h3(dh2b)

#meta kale
fig4 = graf_bar_m(dmt)
fig4a = graf_bar_m1(dmt)
fig4b = graf_bar_m2(dmt)
fig4c = graf_bar_m(dmt)
fig4d = graf_bar_m1(dmt)
fig4e = graf_bar_m2(dmt)
#meta platero
fig5 = graf_bar_m(dmt2)
fig5a = graf_bar_m1(dmt2)
fig5b = graf_bar_m2(dmt2)
fig5c = graf_bar_m(dmt2)
fig5d = graf_bar_m1(dmt2)
fig5e = graf_bar_m2(dmt2)

#Displays para Dash

display_proy = {'kale':'Proyecto Kalé','platero':'Proyecto Platero'}
#display_camp = list(div_fauna_pto.CAMPANA.drop_duplicates().sort_values())
#display_camp.append('Todas')
#display_fauna_pto = list(acum_fauna_pto_esp.ID_MUES_PT.drop_duplicates().sort_values())
#display_fauna_tro = list(div_fauna_tro.ID_MUES_TR.drop_duplicates().sort_values())
#display_fauna_char = {'NUM_IND':'Abundancia'}

#Componentes de Dash

fauna_kale = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Fauna de Kale", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H5("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                dcc.Tabs(id="tabsgraph_f_kale", value='tab-1graph', children=[
                    dcc.Tab(label='Numero de Individuos', value='tab-1graph-f'),
                    dcc.Tab(label='Abundancia Absoluta', value='tab-2graph-f'),
                    dcc.Tab(label='Abundancia Relativa', value='tab-3graph-f'),                       
                #dcc.Graph(figure=fig1, id = "figf1"),
                #dcc.Graph(figure=fig1a, id = "figf1a")
                #dcc.Slider(0, (len(display_camp)-1), id='selector_epoca_diversidad', 
                #marks= dict(zip(range(len(display_camp)),display_camp)), step=None,
                #className="one-half column pretty-container"),
                #dcc.Graph(figure=fig2, id='diversidad_fauna',className="one-half column pretty-container",
                #style={'height':'50rem','overflow':'scroll','padding':'3rem',"margin-left": "10px","margin-right": "5px"}),
                #dcc.Graph(figure=fig3, id='pto_fauna',className="one-half column pretty-container",
                #style={'height':'50rem','overflow':'scroll','padding':'3rem',"margin-left": "10px","margin-right": "5px"})
                ]),
                html.Div(id='tabs-contentgraph_kale_f') 
            ])
        ]
    ),className="mt-3",
    )
flora_kale = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Flora de Kale", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H5("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                dcc.Tabs(id="tabsgraph_v_kale", value='tab-graph2', children=[
                    dcc.Tab(label='Biomasa Individuos', value='tab-1graph-v'),
                    dcc.Tab(label='Carbono Capturado', value='tab-2graph-v'),
                    dcc.Tab(label='Numero de Invidiuos', value='tab-3graph-v'),
                    dcc.Tab(label='Comparacion', value='tab-4graph-v'),
            
                ]),
                html.Div(id='tabs-contentgraph_kale_v') 
            ])
        ]
    ),
    className="mt-3",
)
hidrobiota_kale = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Hidrobiota de Kale", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H5("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            
            html.Div([
                dcc.Tabs(id="tabsgraph_h_kale", value='tab-graph3', children=[
                    dcc.Tab(label='Densidad de Individuos', value='tab-1graph-h'),
                    dcc.Tab(label='Unidad de Densidad', value='tab-2graph-h'),
                    dcc.Tab(label='Abundancia Relativa', value='tab-3graph-h'),
                ]),
                html.Div(id='tabs-contentgraph_kale_h') 
            ])
        ]
    ),
    className="mt-3",
)
metabarcoding_kale = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Metabarcoding de Kale", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H5("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            
            html.Div([
                dcc.Tabs(id="tabsgraph_m_kale", value='tab-graph4', children=[
                    dcc.Tab(label='Numero de OTU', value='tab-1graph-m'),
                    dcc.Tab(label='Numero de Repeticiones', value='tab-2graph-m'),
                    dcc.Tab(label='Numero de Lecturas', value='tab-3graph-m'),
                ]),
                html.Div(id='tabs-contentgraph_kale_m') 
            ])
        ]
    ),
    className="mt-3",
)
paisaje_kale = dbc.Card(
    dbc.CardBody([
            html.H3("Componente paisaje", className="card-text"),
            html.Div([
                dcc.Graph(figure=fig1, id = "figv2")
            ])
        ]
    ),
    className="mt-3",
)
tabs_kale = html.Div([
                dcc.Tabs(id="tabs_kale", value='tab', children=[
                    dcc.Tab(fauna_kale, label="Fauna",className = 'font_size', ),
                    dcc.Tab(flora_kale, label="Flora"),
                    dcc.Tab(hidrobiota_kale, label="Hidrobiota"),
                    dcc.Tab(metabarcoding_kale, label="Metabarcoding"),
                    dcc.Tab(paisaje_kale, label="Paisaje")
                ]),
                html.Div(id='tab_content_kale')
            ])
fauna_platero = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Fauna de Platero", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H3("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                html.H1('Puntos de Muestreo Fauna'),
                dcc.Tabs(id="tabsgraph_f_platero", value='tab-graph6', children=[
                    dcc.Tab(label='Numero de Individuos', value='tab-1graph-f2'),
                    dcc.Tab(label='Abundancia Absoluta', value='tab-2graph-f2'),
                    dcc.Tab(label='Abundancia Relativa', value='tab-3graph-f2'),
            
                ]),
                html.Div(id='tabs-contentgraph_platero_f') 
            ])
        ]
    ),
    className="mt-3",
)
flora_platero = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Flora de Platero", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H3("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                html.H1('Puntos de Muestreo Flora'),
                dcc.Tabs(id="tabsgraph_v_platero", value='tab-graph7', children=[
                    dcc.Tab(label='Biomasa Individuos', value='tab-1graph-v2'),
                    dcc.Tab(label='Carbono Capturado', value='tab-2graph-v2'),
                    dcc.Tab(label='Numero de Invidiuos', value='tab-3graph-v2'),
                    dcc.Tab(label='Comparacion', value='tab-4graph-v2'),
                ]),
                html.Div(id='tabs-contentgraph_platero_v') 
            ])
        ]
    ),
    className="mt-3",
)
hidrobiota_platero = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Hidrobiotico de Platero", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H3("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                html.H1('Puntos de Muestreo Hidrobiotico'),
                dcc.Tabs(id="tabsgraph_h_platero", value='tab-graph8', children=[
                    dcc.Tab(label='Densidad de Individuos', value='tab-1graph-h2'),
                    dcc.Tab(label='Unidad de Densidad', value='tab-2graph-h2'),
                    dcc.Tab(label='Abundancia Relativa', value='tab-3graph-h2'),
                ]),
                html.Div(id='tabs-contentgraph_platero_h') 
            ])
        ]
    ),
    className="mt-3",
)
metabarcoding_platero = dbc.Card(
    dbc.CardBody([
            html.Div([
                html.H3("Componente Metabarcoding de Platero", className="card-text"),
                html.P("Aquí debería ir un texto etc etc etc etc et"),
                html.P("")
            ]),
            html.Div([
                html.H3("Puntos de monitoreo", className="card-text"),
                html.P("Se realizaron X número de monitoreos durante X tiempo..."),
            ]),
            html.Div([
                html.H1('Puntos de Muestreo Metabarcoding'),
                dcc.Tabs(id="tabsgraph_m_platero", value='tab-graph9', children=[
                    dcc.Tab(label='Numero de OTU', value='tab-1graph-m2'),
                    dcc.Tab(label='Numero de Repeticiones', value='tab-2graph-m2'),
                    dcc.Tab(label='Numero de Lecturas', value='tab-3graph-m2'),
                ]),
                html.Div(id='tabs-contentgraph_platero_m') 
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
tabs_platero = html.Div([
                dcc.Tabs(id="tabs_platero", value='tab', children=[
                    dcc.Tab(fauna_platero, label="Fauna",className = 'font_size', ),
                    dcc.Tab(flora_platero, label="Flora"),
                    dcc.Tab(hidrobiota_platero, label="Hidrobiota"),
                    dcc.Tab(metabarcoding_platero, label="Metabarcoding"),
                    dcc.Tab(paisaje_platero, label="Paisaje")
                ]),
                html.Div(id='tab_content_platero')
            ])

#App de Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

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
        html.H6('Por favor selecciona un proyecto para ver la información asociada al mismo:'),
        
        dcc.Tabs(persistence= True, id="select_proyecto", value='tab', parent_className='custom-tabs',
                    className='custom-tabs-container',children=[
                    dcc.Tab(label='Kale', value='Kale'),
                    dcc.Tab(label='Platero', value='Platero'),
                ],
                colors={
                    "border": "white",
                    "primary": "gold",
                    "background": "white"
                        }),
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

@app.callback(Output('info_proyecto','children'),
                Input('select_proyecto','value'))
def update_info (selected_value):
    if selected_value == 'Kale':
        return tabs_kale
    elif selected_value == 'Platero':
        return tabs_platero

#@app.callback(Output('diversidad_fauna', 'figure'), Input('selector_epoca_diversidad', 'value'))
#def update_graf_diver_fauna(selected_value):
    #marks = dict(zip(range(len(display_camp)), display_camp))
    #fig2 = graf_diver_fauna(div_fauna_pto, marks[selected_value])
#    return 
@app.callback(Output('tabs-contentgraph_kale_f', 'children'), Input('tabsgraph_f_kale', 'value'))
def render_content_f(tab):
    if tab == 'tab-1graph-f':
        return html.Div([
            html.H3('Numero de Individuos'),
            dcc.Graph(figure= fig1)
        ])
    elif tab == 'tab-2graph-f':
        return html.Div([
            html.H3('Abundancia Absoluta'),
            dcc.Graph(
                id='graph-2-tabs-dcc-f',
                figure=fig1a
            )
        ])
    elif tab == 'tab-3graph-f':
        return html.Div([
            html.H3('Abundancia Relativa'),
            dcc.Graph(
                id='graph-3-tabs-dcc-f',
                figure=fig1b
            )
        ])

@app.callback(Output('tabs-contentgraph_kale_v', 'children'), Input('tabsgraph_v_kale', 'value'))
def render_content_v(tab):
    if tab == 'tab-1graph-v':
        return html.Div([
            html.H3('Biomasa'),
            dcc.Graph(
                id='graph-1-tabs-dcc-v',
                figure= fig2
            )
        ])
    elif tab == 'tab-2graph-v':
        return html.Div([
            html.H3('Carbono Capturado'),
            dcc.Graph(
                id='graph-2-tabs-dcc-v',
                figure=fig2a
            )
        ])
    elif tab == 'tab-3graph-v':
        return html.Div([
            html.H3('Numero de Individuos'),
            dcc.Graph(
                id='graph-3-tabs-dcc-v',
                figure=fig2b
            )
        ])
    elif tab == 'tab-4graph-v':
        return html.Div([
            html.H3('Comparacion'),
            dcc.Graph(
                id='graph-4-tabs-dcc-v',
                figure=figsc_v
            )
        ])

@app.callback(Output('tabs-contentgraph_kale_h', 'children'), Input('tabsgraph_h_kale', 'value'))
def render_content_h(tab):
    if tab == 'tab-1graph-h':
        return html.Div([
            html.H3('Densidad Individual'),
            dcc.Graph(
                id='graph-1-tabs-dcc-h',
                figure= fig3
            )
        ])
    elif tab == 'tab-2graph-h':
        return html.Div([
            html.H3('Unidad Densidad'),
            dcc.Graph(
                id='graph-2-tabs-dcc-h',
                figure=fig3a
            )
        ])
    elif tab == 'tab-3graph-h':
        return html.Div([
            html.H3('Abundancia Relativa'),
            dcc.Graph(
                id='graph-3-tabs-dcc-h',
                figure=fig3b
            )
        ])

@app.callback(Output('tabs-contentgraph_kale_m', 'children'), Input('tabsgraph_m_kale', 'value'))
def render_content_m(tab):
    if tab == 'tab-1graph-m':
        return html.Div([
            html.H3('Numero de OTU'),
            dcc.Graph(
                id='graph-1-tabs-dcc-m',
                figure= fig4c
            )
        ])
    elif tab == 'tab-2graph-m':
        return html.Div([
            html.H3('Numero de Repeticiones'),
            dcc.Graph(
                id='graph-2-tabs-dcc-m',
                figure=fig4d
            )
        ])
    elif tab == 'tab-3graph-m':
        return html.Div([
            html.H3('Numero de Lecturas'),
            dcc.Graph(
                id='graph-3-tabs-dcc-m',
                figure=fig4e
            )
        ])       

@app.callback(Output('tabs-contentgraph_platero_f', 'children'), Input('tabsgraph_f_platero', 'value'))
def render_content_f2(tab):
    if tab == 'tab-1graph-f2':
        return html.Div([
            html.H3('Numero de Individuos'),
            dcc.Graph(
                id='graph-4-tabs-dcc',
                figure= fig1c
            )
        ])
    elif tab == 'tab-2graph-f2':
        return html.Div([
            html.H3('Abundancia Absoluta'),
            dcc.Graph(
                id='graph-5-tabs-dcc',
                figure=fig1d
            )
        ])
    elif tab == 'tab-3graph-f2':
        return html.Div([
            html.H3('Abundancia Relativa'),
            dcc.Graph(
                id='graph-6-tabs-dcc',
                figure=fig1e
            )
        ])

@app.callback(Output('tabs-contentgraph_platero_v', 'children'), Input('tabsgraph_v_platero', 'value'))
def render_content_v2(tab):
    if tab == 'tab-1graph-v2':
        return html.Div([
            html.H3('Biomasa'),
            dcc.Graph(
                id='graph-1-tabs-dcc-v2',
                figure= fig2c
            )
        ])
    elif tab == 'tab-2graph-v2':
        return html.Div([
            html.H3('Carbono Capturado'),
            dcc.Graph(
                id='graph-2-tabs-dcc-v2',
                figure=fig2d
            )
        ])
    elif tab == 'tab-3graph-v2':
        return html.Div([
            html.H3('Numero de Individuos'),
            dcc.Graph(
                id='graph-3-tabs-dcc-v2',
                figure=fig2e
            )
        ])  
    elif tab == 'tab-4graph-v2':
        return html.Div([
            html.H3('Comparacion'),
            dcc.Graph(
                id='graph-4-tabs-dcc-v',
                figure=figsc_v2
            )
        ])

@app.callback(Output('tabs-contentgraph_platero_h', 'children'), Input('tabsgraph_h_platero', 'value'))
def render_content_h2(tab):
    if tab == 'tab-1graph-h2':
        return html.Div([
            html.H3('Densidad Individual'),
            dcc.Graph(
                id='graph-1-tabs-dcc-h2',
                figure= fig3c
            )
        ])
    elif tab == 'tab-2graph-h2':
        return html.Div([
            html.H3('Unidad Densidad'),
            dcc.Graph(
                id='graph-2-tabs-dcc-h2',
                figure=fig3d
            )
        ])
    elif tab == 'tab-3graph-h2':
        return html.Div([
            html.H3('Abundancia Relativa'),
            dcc.Graph(
                id='graph-3-tabs-dcc-h2',
                figure=fig3e
            )
        ])

@app.callback(Output('tabs-contentgraph_platero_m', 'children'), Input('tabsgraph_m_platero', 'value'))
def render_content_m2(tab):
    if tab == 'tab-1graph-m2':
        return html.Div([
            html.H3('Numero de OTU'),
            dcc.Graph(
                id='graph-1-tabs-dcc-m2',
                figure= fig4c
            )
        ])
    elif tab == 'tab-2graph-m2':
        return html.Div([
            html.H3('Numero de Repeticiones'),
            dcc.Graph(
                id='graph-2-tabs-dcc-m2',
                figure=fig4d
            )
        ])
    elif tab == 'tab-3graph-m2':
        return html.Div([
            html.H3('Numero de Lecturas'),
            dcc.Graph(
                id='graph-3-tabs-dcc-m2',
                figure=fig4e
            )
        ])       

if __name__ == "__main__":
    app.run_server(debug=True)


