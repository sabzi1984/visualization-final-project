from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import preprocess as preproc
#----------------------------------------------------------------------
#with open('assets/data/WORK_INSCRIPTION.csv', encoding='latin1') as data_file:
#    df = pd.read_csv(data_file)
#----------------------------------------------------------------------
def modifier(df):
    df['Session'] = df['Trimestre'] % 10
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]
    df = preproc.inscription_automne(df)
    return df

def inscription_grades(df):
    
    df1 = df.groupby(['Grade', 'ANNEE'], as_index = False).size()
    nombre_grade = df1.groupby(['Grade']).sum()
    nombre_grade.rename(columns={'size': 'total'}, inplace = True)
    merged = df1.merge(nombre_grade, on='Grade')
    merged['Pourcentage'] = (merged['size'] /  merged['total']) * 100
    merged.drop(columns = 'total', axis=1, inplace =  True)
    return merged      

def get_niveau(flag):
    if flag == 1:
        niveau ="Certificat"
    elif flag == 2:
        niveau ="Bac"
    elif flag == 3:
        niveau ="Maitrise"
    else:
        niveau ="Doctorat"
    return niveau

def tous_programmes(df, flag):
    #####################################
    df = inscription_grades(df)
    #####################################
    niveau = get_niveau(flag)

    df_bac = df.loc[df['Grade'] == 'Bac']
    df_bac = df_bac.tail(10)
    
    df_certificat = df.loc[df['Grade'] == 'Certificat']
    df_certificat = df_certificat.tail(10)

    df_maitrise = df.loc[df['Grade'] == 'Maitrise']
    df_maitrise = df_maitrise.tail(10)

    df_phd = df.loc[df['Grade'] == 'Doctorat']
    df_phd = df_phd.tail(10)
    switcher = {
        1: df_certificat,
        2: df_bac,
        3: df_maitrise,
        4: df_phd,
    }
    df = switcher.get(flag)
    df['Pourcentage'] = df['Pourcentage'].round(2)
    

    fig = px.line(data_frame = df,
                            x='ANNEE', 
                            y='size', 
                        title="Nombre  d'étudiant(e)s inscrit(e)s au <b>"+ niveau +"</b> au semestre d'automne de chaque année", 
                      labels = {'size' : 'Nombre', 'ANNEE' : 'Année' }, 
                    
                       )
    
    fig.update_layout(
        plot_bgcolor = '#f1f1f1',
        paper_bgcolor='#f1f1f1',
    )
    fig.update_traces(mode="markers+lines",
                      line=dict(color='#808080',shape='linear', width=4),
                      marker = dict(size = 10,
                                    color = '#42aae6',
                                    symbol = 'pentagon'

                      ),
                      hovertemplate = "<b>Année =  %{x}</b><br><b>Nombre =  %{y} </b></br><extra></extra>"
    )
    fig.update_layout(height = 800, 
                      width=1000,
                      hovermode="x",
                      title_font_color = "black",
                      title_font_size = 18,
                      title_font_family = "Times New Roman",
                      )
    #print(fig)
    return fig
####################################################################################################
def les_12_programmes(df, flag):
    niveau = get_niveau(flag)

    df_certificat = preproc.evolution_programmes(df, 'Certificat', False, False)
    df_bac = preproc.evolution_programmes(df, 'Bac', False, False)
    df_maitrise = preproc.evolution_programmes(df, 'Maitrise', False, False)
    df_phd = preproc.evolution_programmes(df, 'Doctorat', False, False)
   
    switcher = {
        1: df_certificat,
        2: df_bac,
        3: df_maitrise,
        4: df_phd,
    }
    # df final
    df = switcher.get(flag)
    
    
    # **********************************************************
    fig_line = make_subplots(rows = 4, 
                             cols = 3, 
                             subplot_titles=([df.columns[i] for i in range(12)]),
                             vertical_spacing = 0.1)
    r = 1
    c = 1    
    copy_df = df 
    
    programmes = [ ]
    for column in df.columns.values:
         programmes.append (df[column].tolist ())

    
    for i in range(0,12):
        
        fig_line.add_trace(go.Scatter(
                         x = df.index,  
                         y = programmes[i],
                         mode='lines+markers',
                         line=dict(color='#808080',shape='linear', width=2),
                         marker = dict(size = 5,
                                       color = '#42aae6',
                                       symbol = 'circle'
                         ),
                         hovertemplate = "<b>Année =  %{x}</b><br><b>Nombre =  %{y} </b></br><extra></extra>"
                         ), row=r, col=c
             )
        if c < 3:
           c+=1
        else:
           r+=1
           c=1
        df_line = copy_df
    
    fig_line.update_layout(plot_bgcolor = '#f1f1f1',
                            paper_bgcolor='#f1f1f1', 
                            dragmode=False,
                           showlegend=False, 
                           height = 1200, 
                           width=1400,
                           title = 'Programmes les plus populaires pendant les 10 dernières années au niveau <b>'+ niveau +"</b>",
                           title_font_color = "black",
                           title_font_size = 18,
                           title_font_family = "Times New Roman",
                           )
    fig_line.update_xaxes(tickangle=-45, tickfont = {'size': 10,'color':'blue'})
    fig_line.update_yaxes(showgrid = True, rangemode='tozero')
  
    return fig_line