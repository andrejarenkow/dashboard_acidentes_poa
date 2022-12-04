from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app


slider_size=[2017, 2018, 2019, 2020, 2021, 2022]
list_of_locations = {
    'Todas':'Todas',
    'Abalroamento':'ABALROAMENTO',
     'Atropelamento':'ATROPELAMENTO',
     'Choque':'CHOQUE',
     'Colisão':'COLISÃO',
     'Queda':'QUEDA',
     'tombamento':'TOMBAMENTO',
     'Eventual':'EVENTUAL',
     'Capotagem':'CAPOTAGEM',
     'Incêndio':'INCÊNDIO',
     'Não cadastrado':'NAO CADASTRADO'
}

controllers = dbc.Row([
    html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), style={'width':'50%'}),
    html.H3('Acidentes de trânsito - POA', style={'margin-top':'30px'}),
    html.P('Utilize este dashboard para analisar os acidentes de trânsito em Porto Alegre'),
    html.H4('Tipo de acidente', style={'margin-top':'50px', 'margin-bottom':'50px'}),
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label':i, 'value':j} for i, j in list_of_locations.items()],
        value='Todas',
        placeholder='Selecione uma região'
    ),
    html.H4('Selecione o ano', style={'margin-top':'50px', 'margin-bottom':'50px'}),

    dcc.Slider(
        min=min(slider_size),
        max=max(slider_size),
        marks={i: '{}'.format(i) for i in range(min(slider_size),max(slider_size)+1,1)},
        step=1,
        value=max(slider_size),
        id='slider-ano',


    )
])