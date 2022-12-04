from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import app
from _map import *
from _histogram import *
from _controllers import *

#============================
#Limpeza dos dados

df_data = pd.read_csv('https://dadosabertos.poa.br/dataset/d6cfbe48-ee1f-450f-87f5-9426f6a09328/resource/b56f8123-716a-4893-9348-23945f1ea1b9/download/cat_acidentes.csv', sep=';')

df_data = df_data[['data', 'feridos','feridos_gr',
                   'mortes', 'morte_post', 'fatais',
                   'auto', 'taxi','lotacao', 'onibus_urb',
                   'caminhao', 'moto',
                   'carroca', 'bicicleta', 'outro', 'cont_vit',
                   'ups', 'patinete','idacidente', 'longitude',
                   'latitude', 'tipo_acid',
                   'dia_sem', 'hora', 'noite_dia', 'regiao']]

df_data['data'] = pd.to_datetime(df_data['data'], errors='coerce')
df_data.dropna(subset=['data'], inplace=True)
df_data['ano'] = df_data['data'].dt.year
df_data['mes'] = df_data['data'].dt.month
df_data['regiao'] = df_data['regiao'].fillna('-')
limites_lat = [-30.32, -29.95]
limites_lon = [-51.28, -50.97]
df_data = df_data[(df_data['latitude'] > min(limites_lat)) & (df_data['latitude'] < max(limites_lat))]
df_data = df_data[(df_data['longitude'] > min(limites_lon)) & (df_data['longitude'] < max(limites_lon))]
df_data = df_data.sort_values('feridos')

#=============================
#Layout
app.layout = dbc.Container(
        children=[
                dbc.Row([
                        dbc.Col([controllers], md=3),
                        dbc.Col([map, hist], md=9),
                ])

        ], fluid=True, )

#=============================
#Callbacks
@app.callback([Output('hist-graph', 'figure'),
                Output('map-graph', 'figure')],
                [Input('location-dropdown', 'value'),
                Input('slider-ano', 'value')])

def update_hist(location, ano):
        if location is None:
                df_intermediate = df_data.copy()
        
        else:
                df_intermediate = df_data[df_data['tipo_acid']==location] if location != 'Todas' else df_data.copy()
                year_limit = ano if ano is not None else df_data['ano'].max()
                df_intermediate = df_intermediate[df_intermediate['ano'] <= year_limit]

        hist_fig = px.histogram(df_intermediate, x='data', opacity=0.75,
                                 nbins=(df_intermediate['data'].max() - df_intermediate['data'].min()).days)
        hist_layout = go.Layout(
                margin=go.layout.Margin(l=10, r=0, t=0, b=50),
                showlegend=False,
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)'
        )
        hist_fig.layout = hist_layout

        

        map_fig = px.scatter_mapbox(df_intermediate, lat='latitude', lon='longitude',
                       center=dict(lat=-30.11201465940859, lon=-51.11035138053364), zoom=10,
                        mapbox_style="carto-darkmatter", color='feridos',size='feridos', opacity=0.7,
                        color_continuous_scale=px.colors.sequential.Reds)
        
        map_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
                                margin=go.layout.Margin(l=10, r=10, t=10, b=10))

        return hist_fig, map_fig


if __name__ == '__main__':
    app.run_server(debug=True)