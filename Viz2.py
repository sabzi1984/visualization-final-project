from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import preprocess as preproc
#with open('assets/data/WORK_INSCRIPTION.csv') as data_file:
#    df = pd.read_csv(data_file)

def modifier(df):
    df['Session'] = df['Trimestre'] % 10
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]
    df= preproc.inscription_automne(df)
    df= preproc.filtrer_dataframe(df)


    return df
def get_years(df):
    years = []
    years = df['ANNEE'].unique()
    years.sort()
    return years

def get_figbar(df, year):

    fig_bar  = go.Figure()
    fig_bar = px.bar(df,
                 x = df['Pourcentage'],
                 y=df['Pays_Citoyennete'],
                 color=df['Pourcentage'],
                 template='simple_white',
                 text = df['Pourcentage'],
                 title = "Les 20 pays qui envoient le plus d'étudiant(e)s à Polytechnique en " + year
     )
    fig_bar.update_traces(marker_color='#fa961e')
    fig_bar.update_xaxes(range=[0,max(df['Pourcentage'])+5], fixedrange = True)
    fig_bar.update_yaxes(fixedrange = True, tickfont = dict(size=10))
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
                        plot_bgcolor = '#f1f1f1',
                        paper_bgcolor='#f1f1f1',
                      coloraxis_showscale=False, 
                      uniformtext_minsize=10,
                      title_font_family = "Times New Roman",
                      title_font_color = "black",
                      title_font_size = 18,
                      xaxis_title_font_size = 14,
                      yaxis_title_font_size = 14,
                      
                      )
   
    return fig_bar

def get_figline(df,listp):
    fig_line = go.Figure()
    fig_line = make_subplots(rows = 4, 
                             cols = 5, 
                             
                             subplot_titles=([listp[i] for i in range(20)]),
                             vertical_spacing = 0.1)
    r = 1
    c = 1    
    copy_df = df 
    #print(listp)
     
  
    #print('***********')
    #print('***********')
    #print('***********')


    df = df.reindex(columns=listp)
    #print(df)
    pays = [ ]
    for column in df.columns.values:
         pays.append (df[column].tolist ())
         
    for i in range(0,20):
        
        fig_line.add_trace(go.Scatter(
                         x = df.index,  
                         y = pays[i],
                         mode='lines+markers',
                         line=dict(color='#808080',shape='linear', width=2),
                         marker = dict(size = 5,
                                       color = '#ff941c', 
                                       symbol = 'circle'
                         ),
                         hovertemplate = "<b>ANNEE: %{x}</b><br><b>Nombre: %{y} </b></br><extra></extra>"
                         ), row=r, col=c
             )
        if c < 5:
           c+=1
        else:
           r+=1
           c=1
        df_line = copy_df
    
    fig_line.update_layout(plot_bgcolor = '#f1f1f1',
                            paper_bgcolor='#f1f1f1', 
                           showlegend=False, 
                           height = 1200, 
                           width=1400,
                           title = 'Les nombres des étudiants de chaque pays pendant les 10 dernières années',
                           title_font_color = "black",
                           title_font_size = 18,
                           title_font_family = "Times New Roman",
                           )
   
    
    fig_line.update_xaxes(tickangle=-45, tickfont = {'size': 10,'color':'blue'})
    fig_line.update_yaxes(showgrid = True, rangemode='tozero')
    return fig_line

def get_figmap(df):
    fig_map = go.Figure()
    fig_map = px.choropleth(data_frame=df,
                       locations=df['Pays_Citoyennete_ang'],
                       locationmode='country names',
                       color = df['Nombre'],
                       color_continuous_scale = px.colors.sequential.Sunsetdark,
                       hover_name = df['Pays_Citoyennete'],
                       projection='natural earth',
                       hover_data={'Pays_Citoyennete_ang':False}
    )
    fig_map.update(layout_coloraxis_showscale=True)
    fig_map.update_layout(plot_bgcolor = '#f1f1f1',
                        paper_bgcolor='#f1f1f1',dragmode =False, coloraxis_colorbar_x = -0.15, margin={"r":0,"t":0,"l":50,"b":0})
    fig_map.update_geos(resolution = 50,
                        showocean=False,
                        showframe=True
                        


    )
    
    return fig_map

def get_fig_pays(df, country):
    fig_pays = go.Figure()
    fig_pays = px.line(data_frame = df,
                            x = df.index,  
                            y = df[country].tolist(),
    )
    
    fig_pays.update_xaxes(tickangle = -45, tickfont = {'size': 10,'color':'blue'})
    fig_pays.update_yaxes(title = 'Nombre', rangemode='tozero')
    fig_pays.update_layout(title = country, hovermode="x unified",plot_bgcolor = '#f1f1f1',paper_bgcolor='#f1f1f1',
                                                                                  hoverlabel=dict(
                                                                                     bgcolor="white",
                                                                                     font_size=12,
                                                                                     font_family="Rockwell"
    ))
    fig_pays.update_traces(mode="markers+lines", 
                           hovertemplate = "<b>ANNEE: %{x}</b><br><b>Nombre: %{y} </b></br><extra></extra>" )

    return fig_pays