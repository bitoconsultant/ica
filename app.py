import dash
import geojson as gpd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import brucellosis_model as bm
from urllib.request import urlopen

top_samples = pd.read_csv("https://raw.githubusercontent.com/henrycerpa/ica/main/data/top_cases.csv")
top_three = pd.read_csv("https://raw.githubusercontent.com/henrycerpa/ica/main/data/top_three.csv")
mapas = pd.read_csv("https://raw.githubusercontent.com/henrycerpa/ica/main/data/map.csv")
url = "https://raw.githubusercontent.com/henrycerpa/ica/main/data/Municipio_SpatialJoin_Fe.geojson"
response = urlopen(url)
gjson = gpd.load(response)

top_negative = top_samples[top_samples.result == 'negative'].sort_values("cases")[-10:]
top_positive = top_samples[top_samples.result == 'positive'].sort_values("cases")[-10:]

sample_number = dbc.RadioItems(
    id='sample_choose',
    className='radio',
    options=[dict(label='Positive', value=0), dict(label='Negative', value=1)],
    value=0,
    inline=True
)

dict_ = {'ANTIOQUIA': 'ANTIOQUIA', 'BOLIVAR': 'BOLIVAR', 'BOYACA': 'BOYACA', 'CALDAS': 'CALDAS', 'CAQUETA': 'CAQUETA',
         'CASANARE': 'CASANARE',
         'CAUCA': 'CAUCA', 'CESAR': 'CESAR', 'CORDOBA': 'CORDOBA', 'CUNDINAMARCA': 'CUNDINAMARCA',
         'MAGDALENA': 'MAGDALENA', 'META': 'META', 'NARINO': 'NARINO',
         'NORTE DE SANTANDER': 'NORTE DE SANTANDER', 'QUINDIO': 'QUINDIO', 'RISARALDA': 'RISARALDA',
         'SANTANDER': 'SANTANDER', 'SUCRE': 'SUCRE', 'TOLIMA': 'TOLIMA',
         'VALLE DEL CAUCA': 'VALLE DEL CAUCA'}

departamentos = ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTA', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA',
                 'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAJIRA', 'GUAVIARE',
                 'HUILA', 'MAGDALENA', 'META', 'NARINO', 'NORTE DE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA',
                 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE DEL CAUCA', 'VAUPES', 'VICHADA', 'PAIS']
departamentos.sort()

options_neg = [dict(label=key, value=dict_[key]) for key in top_negative['state'].tolist()[::-1] if key in dict_.keys()]
options_pos = [dict(label=val, value=val) for val in top_positive["state"].tolist()[::-1]]

bar_colors = ['#ebb36a', '#6dbf9c']
bar_options = [top_positive, top_negative]

drop_map = dcc.Dropdown(
    id='drop_map',
    clearable=False,
    searchable=False,
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
)

drop_pred = dcc.Dropdown(
    id='departamento',
    options=[{'label': x, 'value': x} for x in departamentos],
    value='PAIS',
    multi=False,
    disabled=False,
    clearable=True,
    searchable=True,
    placeholder='Seleccione...',
    className='form-dropdown',
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'},
    persistence='string',
    persistence_type='memory'
)

mapas_final = mapas.groupby(['CODIGO_MUNICIPIO_x', 'año_test'])['numero_muestras'].sum().reset_index()
mapas_final = mapas_final.sort_values('año_test')
mapas_final.rename(columns={'numero_muestras': 'Samples', 'año_test': 'Year'}, inplace=True)

colmap = px.choropleth_mapbox(mapas_final, geojson=gjson,
                              locations='CODIGO_MUNICIPIO_x',
                              featureidkey="properties.codigo_dane",
                              animation_frame='Year',
                              color='Samples',
                              color_continuous_scale="inferno_r",
                              center={"lat": 4.348728, "lon": -73.501690},
                              mapbox_style="carto-positron",
                              zoom=5.3,
                              opacity=0.5,
                              height=900,
                              title=f'3. Geographically Located Samples')

# ------------------------------------------------------ APP ------------------------------------------------------

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.Div([
        html.Img(src='https://raw.githubusercontent.com/henrycerpa/dash-ica/main/assets/images.png',
                 style={'position': 'relative', 'width': '90%', 'left': '5px', 'top': '1px'}),
        html.Div([
            html.H2('TEAM', style={'font-weight': 'BOLD'}),
            html.H3('Karen Martinez Mendoza', style={'font-weight': 'BOLD'}),
            html.H3('Ingeniera Quimica', style={'font-weight': 'normal'}),
            html.H3('lightsoul093@gmail.com', style={'font-weight': 'normal'}),
            html.H3('Alberto Mario Castillo', style={'font-weight': 'BOLD'}),
            html.H3('Ingeniero Industrial', style={'font-weight': 'normal'}),
            html.H3('albertomcastillo@outlook.com', style={'font-weight': 'normal'}),
            html.H3('Henry Cerpa Marquez', style={'font-weight': 'BOLD'}),
            html.H3('Ingeniero Industrial', style={'font-weight': 'normal'}),
            html.H3('henrycerpa@gmail.com', style={'font-weight': 'normal'}),
            html.H3('Cristian Gantiva Castiblanco', style={'font-weight': 'BOLD'}),
            html.H3('Politologo', style={'font-weight': 'normal'}),
            html.H3('cg_cia@hotmail.com', style={'font-weight': 'normal'}),
            html.H3('Jose Garzon Gomez', style={'font-weight': 'BOLD'}),
            html.H3('Ingeniero Electricista', style={'font-weight': 'normal'}),
            html.H3('correo@correo.com', style={'font-weight': 'normal'}),
            html.H3('Eugenio Millan Sarmiento', style={'font-weight': 'BOLD'}),
            html.H3('Ingeniero de Sistemas', style={'font-weight': 'normal'}),
            html.H3('eumillan@hotmail.com', style={'font-weight': 'normal'}),
            html.H3('Ricardo Torres Noack', style={'font-weight': 'BOLD'}),
            html.H3('Administrador de Empresas', style={'font-weight': 'normal'}),
            html.H3('ricardomarble@hotmail.com', style={'font-weight': 'normal'}),
        ], className='box'),

    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.P([
                               'Contributing to the sustainable development of the agriculture, fisheries and aquaculture sectors, to control the brucellosis is fundamental due the profound effect not only on animal health but the production as well. In order to implement public measures, it is necessary to know the conditions that affect the onset and spread of brucellosis.'],
                           style={'color': 'BLACK', 'font-size': '15px', 'font-weight': 'bold'})
                ], style={'width': '180%'}),
            ], className='footer', style={'display': 'flex'}),

            html.Div([
                html.Label("Choose the sample result:"),
                html.Br(),
                html.Br(),
                sample_number
            ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

            html.Div([
                html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        dcc.Graph(id='bar_fig'),
                        html.Div([
                            html.P(id='comment')
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom': '15px'}),

                    html.Div([
                        html.Img(src='https://raw.githubusercontent.com/henrycerpa/dash-ica/main/assets/vaca.png',
                                 style={'width': '100%', 'position': 'relative', 'opacity': '80%'}),
                    ]),

                ], style={'width': '40%'}),

                html.Div([

                    html.Div([
                        html.Label(id='choose_state', style={'margin': '10px'}),
                        drop_map,
                    ], className='box'),

                    html.Div([
                        html.Div([
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.Div([
                                    html.H4(id='city_one', style={'font-weight': 'normal'}),
                                    html.H3(id='pos_one')
                                ], className='box_emissions'),

                                html.Div([
                                    html.H4(id='city_two', style={'font-weight': 'normal'}),
                                    html.H3(id='pos_two')
                                ], className='box_emissions'),

                                html.Div([
                                    html.H4(id='city_three', style={'font-weight': 'normal'}),
                                    html.H3(id='pos_three')
                                ], className='box_emissions'),

                            ], style={'display': 'flex'}),

                        ], className='box', style={'heigth': '10%'}),

                        html.Div([
                            html.Div([

                                dcc.Graph(figure=colmap)], style={'position': 'relative', 'top': '0px'}),

                        ], className='box', style={'padding-bottom': '0px'}),
                    ]),
                ], style={'width': '60%'}),
            ], className='row'),

            html.Div([
                html.Br(),
                html.Br(),
                html.Label([
                               '4. Choose a State for a model prediction (Susceptible, Vaccinated, Infected or Infectious not slaughtered) with cutoff as of December 31, 2021:'],
                           style={"text-align": "center"}),
                drop_pred,
            ], className='one column'),

            html.Div([
                dcc.Graph(id='our_graph')
            ], className='two columns'),

            html.Div([
                html.Label(['With Year 0 being January 1, 2022, choose the final year for your prediction.'],
                           style={}),
                html.P(),
                dcc.RangeSlider(
                    id='years',  # any name you'd like to give it
                    marks={
                        0: '0',  # key=position, value=what you see
                        1: '2022',
                        2: '2023',
                        3: '2024',
                        4: '2025',
                        5: '2026',
                        6: '2027',
                        7: '2028',
                        8: '2029',
                        9: '2030',
                        10: '2031',
                    },
                    step=1,  # number of steps between values
                    min=1,
                    max=10,
                    value=[1],  # default value initially chosen
                    dots=True,  # True, False - insert dots, only when step>1
                    allowCross=False,  # True,False - Manage handle crossover
                    disabled=False,  # True,False - disable handle
                    pushable=2,  # any number, or True with multiple handles
                    updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                    included=True,  # True, False - highlight handle
                    vertical=False,  # True, False - vertical, horizontal slider
                    verticalHeight=900,  # hight of slider (pixels) when vertical=True
                    className='None',
                    tooltip={'always_visible': False,  # show current slider values
                             'placement': 'bottom'},
                ),
            ]),

        ], className='main'),
    ]),
])


# ------------------------------------------------------ Callbacks ------------------------------------------------------

@app.callback(
    [
        Output('title_bar', 'children'),
        Output('bar_fig', 'figure'),
        Output('comment', 'children'),
        Output('drop_map', 'options'),
        Output('drop_map', 'value'),
        Output('choose_state', 'children')
    ],
    [
        Input('sample_choose', 'value')
    ],
)
def bar_chart(top10_select):
    ################## Top10 Plot ##################
    title = '1. Top #10 cases in 2021:'
    df = bar_options[top10_select]

    if top10_select == 2:
        bar_fig = dict(type='bar',
                       x=df.cases,
                       y=df["state"],
                       orientation='h',
                       marker_color=['#ebb36a' if x == 'Animal' else '#6dbf9c' for x in df.result])
    else:
        bar_fig = dict(type='bar',
                       x=df.cases,
                       y=df["state"],
                       orientation='h',
                       marker_color=bar_colors[top10_select])

    ################## Dropdown Bar ##################
    if top10_select == 0:
        options_return = options_pos
        state_chosen = "2. Choose a state for top #3 of towns with cases in 2021:"
        comment = ["3 out of 4 positive cases are from Antioquia, Cundinamarca and Nariño", html.Br(), html.Br()]
    elif top10_select == 1:
        options_return = options_neg
        state_chosen = "2. Choose a state for top #3 of towns with cases in 2021:"
        comment = [
            "Comparing with the positives, 5 of 100 samples in Nariño are positive, the highest percentage among the states",
            html.Br(), html.Br()]

    return title, \
           go.Figure(data=bar_fig, layout=dict(height=300, font_color='#363535', paper_bgcolor='rgba(0,0,0,0)',
                                               plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                                               margin_pad=10)), \
           comment, \
           options_return, \
           options_return[0]['value'], \
           state_chosen


@app.callback(
    [
        Output('pos_one', 'children'),
        Output('pos_two', 'children'),
        Output('pos_three', 'children'),
        Output('city_one', 'children'),
        Output('city_two', 'children'),
        Output('city_three', 'children'),
    ],
    [
        Input('drop_map', 'value'),

    ],
    [State("drop_map", "options")]
)
def update_map(drop_map_value, opt):
    ################## Top Three datset ##################

    the_label = [x['label'] for x in opt if x['value'] == drop_map_value]

    state_option_chosen = top_three[top_three["state"] == the_label[0]]
    pos_one_str = str(state_option_chosen["pos_one"].values[0])
    pos_two_str = str(state_option_chosen["pos_two"].values[0])
    pos_three_str = str(state_option_chosen["pos_three"].values[0])
    city_one_str = str(state_option_chosen["city_one"].values[0])
    city_two_str = str(state_option_chosen["city_two"].values[0])
    city_three_str = str(state_option_chosen["city_three"].values[0])

    return pos_one_str, \
           pos_two_str, \
           pos_three_str, \
           city_one_str, \
           city_two_str, \
           city_three_str\

@app.callback(
    [
    Output('our_graph', 'figure'),
    ],
    [
    Input('years', 'value'),
    Input('departamento', 'value')
        ],
    )

def caller(jahren, dpto):
    s, v, i, i2 = bm.get_model_results(int(jahren[0]))
    plotbx = bm.plot_results(s, v, i, i2, [dpto])
    return plotbx


if __name__ == '__main__':
    app.run_server(debug=False)