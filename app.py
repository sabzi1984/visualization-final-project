# -*- coding: utf-8 -*-


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from dash.exceptions import PreventUpdate

import preprocess as preproc
import linecharts_viz1
import Viz2
import viz3

app = dash.Dash(__name__)
app.title = 'Polytechnique Montréal'

df = pd.read_csv('./assets/WORK_INSCRIPTION.csv', encoding = "ISO-8859-1")
df_vis2 = Viz2.modifier(df)
years = Viz2.get_years(df_vis2)
df_vis3 = viz3.modifier(df)

fig_bar  = go.Figure()
fig_map = go.Figure()
fig_line = go.Figure()
fig_one_pays = go.Figure()

app.layout = html.Div(className='content', children=[
         html.Div(html.Img(src=app.get_asset_url('Polytechnique_Montréal.png')),
        #  style={ 'width' :'500px', 'height':'200px'},
                    id='logo'),

        html.Header(children=[
            html.H1('Égalité & Diversité'),
            html.H2('L\'evolutions du nombre d\'étudiantes et d\'étudiants Internationaux')
        ]),
            html.Div(className='vis1-container', children=[
                html.Div([
                    html.Span(["Category d'etudiants:"],style={'float':'left','fontSize':'18px', }),
                    dcc.RadioItems(
                        id='rd-etudiant',
                        options=[
                            dict(
                                label='Etudiantes',
                                value='Etudiantes'),
                            dict(
                                label='Etudiants Internatinaux',
                                value='Etudiants-Inter'),
                        ],
                        value='Etudiantes', style={'float':'left','fontSize':'24px', 'color':'firebrick','padding-left' : '100px'})]),
                html.Div([
                    html.Span(['Type d\'Inscription:'],style={'float':'left','fontSize':'18px', 'padding-top' : '20px'}),
                    dcc.RadioItems(
                        id='rd-inscription',
                        options=[
                            dict(
                                label='Nouvel Inscription',
                                value='Nouvel'),
                            dict(
                                label='Toutes Inscriptions',
                                value='toutes-Ins'),
                        ],
                        value='toutes-Ins', style={'float':'left','fontSize':'24px', 'color':'firebrick','padding-left' : '100px', 'padding-top' : '20px'})]),
            
                html.Div(children=[
                    dcc.Graph(
                        figure=linecharts_viz1.add_etudiantes_chart(df),
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                    style={'width' :'900px', 'height':'600px'},
                    id='vis1_line-chart'
                ),
                ] ),
            ]),
         html.Header(children=[
            html.H1('Milieu International'),
            html.H2('Quels sont les 10 à 20 pays qui envoient le plus d\'étudiants à Polytechnique')
            
        ]),
        html.Div(className='vis2-container', children=[
                    html.H3("Sélectionnez l'année",style={'fontSize': '18px'}),
                    html.Div(
                    dcc.Dropdown(
                id='vis2_year_dropdown',
                options=[{'label':name, 'value':name} for name in years],
                value = years[21],
                clearable=False,
                searchable=False,
                style={'width': '220px', 
                     'background-color': 'white',
                     #'display': 'inline-block',
                     'color':'black',
                     #'padding-left' : '10px' 
                     }),
                    ),
            
            html.Div([
                    dcc.Graph(id = 'vis2_bar_gragh', 
                          figure = fig_bar,
                          config=dict(
                                      scrollZoom=False,
                                      showTips=False,
                                      showAxisDragHandles=False,
                                      doubleClick=False,
                                      displayModeBar=False
                          ),
                        style={"float":"left"}
                        ),

            html.Div([
                     dcc.Graph(id='vis2_map_graph',
                          figure = fig_map,  
                          config=dict(
                                      scrollZoom=True,
                                      showTips=False,
                                      showAxisDragHandles=False,
                                      doubleClick=False,
                                      displayModeBar=False
                          ), 
                          style={"float":"right"},
                     ),
                dcc.Graph(
                    id = 'vis2_line_one_pays',
                    figure = fig_one_pays, 
                    style ={'visibility': 'hidden'},
                    config=dict(
                                      scrollZoom=False,
                                      showTips=False,
                                      showAxisDragHandles=False,
                                      doubleClick=False,
                                      displayModeBar=False
                                )
                        )
            ],    
                    style = {'display' : 'flex'}
            ),
            ],

                    ),
                html.Div(children=[
                    html.H3("Comparer l'évolution des pays", style={'padding': '25px','fontSize': '18px'}),
                            dcc.Graph(id = 'vis2_line_chart',
                                figure = fig_line,
                                config=dict(
                                      scrollZoom=False,
                                      showTips=False,
                                      showAxisDragHandles=False,
                                      doubleClick=False,
                                      displayModeBar=False
                                    )
                       
                        ),
            ]),
    ]),
           
    
        html.Header(children=[
            html.H1('L\'évolution des Inscriptions dans les Programmes'),
            html.H2('10 programmess plus populair dans chaque niveau d\'etude')
        ]),
       html.Div(className='vis3-container', children=[
       html.H3("Sélectionnez le niveau d'étude", style={'padding': '10px','fontSize': '18px'}),
       html.Div(
        dcc.Dropdown(
            id='vis3_niveau_etude',
            options=[{'label':'Certificat', 'value':'Certificat'},
                     {'label':'Bac', 'value':'Bac'},
                     {'label':'Maitrise', 'value':'Maitrise'},
                     {'label':'Doctorat', 'value':'Doctorat'}
        ],
            clearable=False,
            searchable=False,
            value = 'Bac',
            style={'width': '220px', 
                     'background-color': 'white',
                     #'display': 'inline-block',
                     'color':'black',
                     #'padding-left' : '10px' 
                     })
            ),
            html.Pre(),
            html.Div([
                       html.Button('Tous programmes confondus', 
                                    id='btn-tous', 
                                    n_clicks=0,
                                    className="btn active"
                       ),
                       html.Button('Programmes les plus populaires', 
                                    id='btn-populaire', 
                                    n_clicks=0,
                                    className="btn"

                       ),
            ]),
            html.Div([
                html.Pre(),
                dcc.Graph(id = 'vis3_gragh', 
                            figure = viz3.les_12_programmes(df, 2),
                            config=dict(
                                      scrollZoom=False,
                                      showTips=False,
                                      showAxisDragHandles=False,
                                      doubleClick=False,
                                      displayModeBar=False
                          ),
                          style = {'background-color': '#f1f1f1'}
                          ), 
                
            ]),
          
          ]),
            
])

@app.callback(
    Output('vis1_line-chart','figure'),
    [Input('rd-etudiant','value'),
    Input('rd-inscription','value'),
   ]
)
def update_vis1(student_categ, insc_type):
    
    
    if student_categ=='Etudiantes' and insc_type=='toutes-Ins':
        fig=linecharts_viz1.add_etudiantes_chart(df)
        return fig
    if student_categ=='Etudiantes' and insc_type=='Nouvel':
        fig=linecharts_viz1.add_nouvelles_etudiantes_chart(df)
        return fig
    if student_categ=='Etudiants-Inter' and insc_type=='Nouvel':
        fig=linecharts_viz1.add_nouveaux_etrangers_chart(df)
        return fig
    if student_categ=='Etudiants-Inter' and insc_type=='toutes-Ins':
        fig=linecharts_viz1.add_etudiants_etrangers_chart(df)
        return fig
# ------------------------------------------------------------------------------------
@app.callback(
    [Output('vis2_bar_gragh','figure'),
     Output('vis2_map_graph','figure'),
     Output('vis2_line_chart','figure'),
    ],
    [Input('vis2_year_dropdown','value')]
)
def update_charts(year):  
    df1 = preproc.filtrer_pays(df_vis2, year)
    df1.sort_values(by = ['Pourcentage'], ascending=False, inplace=True)
    df1['Pourcentage'] = df1['Pourcentage'].round(3)
    df2 = df1.head(20)
    #print('*************')
    list_pays=df2['Pays_Citoyennete_ang'].to_list()
    
    fig_bar = Viz2.get_figbar(df2, year)
    fig_map = Viz2.get_figmap(df2)

    df_line = preproc.evolution_pays(df_vis2, year, False)
    
    fig_line = Viz2.get_figline(df_line,list_pays)
   
    return fig_bar , fig_map, fig_line
   
# ------------------------------------------------------------------------------------
@app.callback(
    [Output('vis2_line_one_pays', 'figure'),
    Output('vis2_line_one_pays', 'style')],
    [ Input('vis2_year_dropdown','value'),
      Input('vis2_map_graph', 'clickData')])
def map_clicked(year, click_data):

    df3 = preproc.evolution_pays(df_vis2, year, False)
    
    if click_data is None:
        raise PreventUpdate
    else:
         country = click_data['points'][0]['location']
         fig_pays = Viz2.get_fig_pays(df3, country)
   
    style={'padding-top': '150px','width' :'300px', 'height':'300px','visibility': 'visible'}
    
    return fig_pays, style
#---------------------------------------------------------------------------------------@app.callback(

@app.callback(
    Output('vis3_gragh','figure'),
    [Input('vis3_niveau_etude','value'),
     Input('btn-tous','n_clicks'),
     Input('btn-populaire','n_clicks')]
)
def update_fig(niveau_edude, n_clicks1, n_clicks2):
    # -----------------------------------------------
    select_btn=0
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if (n_clicks1==0 and n_clicks2==0):
       
        if (niveau_edude == 'Certificat'):
            flag = 1
        elif (niveau_edude == 'Bac'):
            flag = 2
        elif (niveau_edude == 'Maitrise'):
            flag = 3
        elif (niveau_edude == 'Doctorat'):
            flag = 4
        fig = viz3.les_12_programmes(df_vis3, flag)
    
    if (button_id == 'btn-tous'):
        select_btn = 1
        if (niveau_edude == 'Certificat'):
            flag = 1
        elif (niveau_edude == 'Bac'):
            flag = 2
        elif (niveau_edude == 'Maitrise'):
            flag = 3
        elif (niveau_edude == 'Doctorat'):
            flag = 4
        fig = viz3.tous_programmes(df_vis3, flag)
    elif (button_id =='btn-populaire'):
        select_btn = 2
        if (niveau_edude == 'Certificat'):
            flag = 1
        elif (niveau_edude == 'Bac'):
            flag = 2
        elif (niveau_edude == 'Maitrise'):
            flag = 3
        elif (niveau_edude == 'Doctorat'):
            flag = 4
        fig = viz3.les_12_programmes(df_vis3, flag)

    elif (button_id =='vis3_niveau_etude'):
        
        if (select_btn == 1):      # Button 'btn-tous' has been clicked recently!

            if (niveau_edude == 'Certificat'):
                flag = 1
            elif (niveau_edude == 'Bac'):
                flag = 2
            elif (niveau_edude == 'Maitrise'):
                flag = 3
            elif (niveau_edude == 'Doctorat'):
                flag = 4
            fig = viz3.tous_programmes(df_vis3, flag)

        elif (select_btn == 2):    # Button 'btn-populaire' has been clicked recently!
            if (niveau_edude == 'Certificat'):
                flag = 1
            elif (niveau_edude == 'Bac'):
                flag = 2
            elif (niveau_edude == 'Maitrise'):
                flag = 3
            elif (niveau_edude == 'Doctorat'):
                flag = 4
            fig = viz3.les_12_programmes(df_vis3, flag)

        else:                      # Neither 'btn-tous' nor 'btn-populaire' has been clicked!
            if (niveau_edude == 'Certificat'):
               flag = 1
            elif (niveau_edude == 'Bac'):
               flag = 2
            elif (niveau_edude == 'Maitrise'):
                flag = 3
            elif (niveau_edude == 'Doctorat'):
                flag = 4
            fig = viz3.les_12_programmes(df_vis3, flag)

    return fig             
#---------------------------------------------------------------------------------------@app.callback(

@app.callback(
    [Output('btn-tous','style'), 
     Output('btn-populaire','style')],
    [Input('btn-tous','n_clicks'),
     Input('btn-populaire','n_clicks')]
)
def set_active(n_clicks1, n_clicks2):
    style_blue={'background-color':'skyblue'}
    style_white={'background-color':'white'}
    ctx = dash.callback_context

    if not ctx.triggered:
        
        return  style_white, style_blue
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id=='btn-tous':
        return style_blue, style_white
    else:
        return  style_white, style_blue
    