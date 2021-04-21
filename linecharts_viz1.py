
import plotly.express as px
import pandas as pd
from preprocess import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#df = pd.read_csv('./assets/WORK_INSCRIPTION.csv') 


def add_etudiantes_chart(df):
    ###################################
    # Cette partie de prétraitement doit être faite au niveau du preprocess ultérieurement
    ###################################
    df['Session'] = df['Trimestre'] % 10

    # On combine les grades 'Maitrise professionnelle' et 'Maitrise recherche' dans le grade 'Maitrise'
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'

    # On garde que 4 grades : 'Bac', 'Maitrise', 'Certificat' et 'Doctorat'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]
    df_male = male_data(df)
    df_all = female_data(df)
    df_tous_grades = df_all.loc[df_all['Session'] == 1] #Récupérer tous grades confondus en automne
    df_tous_grades_male = df_male.loc[df_all['Session'] == 1]
    df_1 = df
    df = inscription_filles_grades(inscription_automne(df))
    df_male = inscription_males_grades(inscription_automne(df_1))
    
    df_male_female = all_data(df_1)
    df_tous_grades_all = df_male_female.loc[df_all['Session'] == 1]
    df_finale = inscription_all_grades(inscription_automne(df_1))

    #df_bac_male = df_male.loc[df_male['Grade'] == 'Bac'] # Pour avoir étudiantes bac seulement pour la session d'automne de chaque année
    #df_bac_male = df_bac_male.tail(10)
    #df_maitrise_male = df_male.loc[df_male['Grade'] == 'Maitrise']
    #df_maitrise_male = df_maitrise_male.tail(10)
    #df_phd_male = df_male.loc[df_male['Grade'] == 'Doctorat']
    #df_phd_male = df_phd_male.tail(10)
    #df_tous_grades_male = df_tous_grades_male.tail(10)

    df_bac = df.loc[df['Grade'] == 'Bac'] # Pour avoir étudiantes bac seulement pour la session d'automne de chaque année
    df_bac = df_bac.tail(10)
    df_maitrise = df.loc[df['Grade'] == 'Maitrise']
    df_maitrise = df_maitrise.tail(10)
    df_phd = df.loc[df['Grade'] == 'Doctorat']
    df_phd = df_phd.tail(10)
    df_tous_grades = df_tous_grades.tail(10)
    ###################################


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_bac['ANNEE'],
        y=df_bac['Pourcentage'],
        marker_color = '#fa961e',
        hovertemplate='<b>Pourcentage</b> : %{y:.2f} %<extra></extra>',
    ))

    fig.update_layout(
        updatemenus=[
            dict(
                type = "buttons",
                direction = "right",
                buttons=list([
                    dict(
                        label="  Baccalauréat  ",
                        method="update",
                        args=[{'y':[df_bac['Pourcentage']]},
                            {'title': 'Pourcentage d\'étudiantes inscrites au baccalauréat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,30]}},
                        
                        ]),
                    dict(
                        label="  Maîtrise  ",
                        method="update",
                        args=[{
                            'y':[df_maitrise['Pourcentage']]},
                            {'title': 'Pourcentage d\'étudiantes inscrites en maîtrise au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,75]}},
                        ]),
                    dict(
                        label="  PhD  ",
                        method="update",
                        args=[{'y':[df_phd['Pourcentage']]},
                            {'title': 'Pourcentage d\'étudiantes inscrites en doctorat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,95]}},
                        
                        ]),
                    dict(
                        label="  Tous les grades  ",
                        method="update",
                        args=[{'y':[df_tous_grades['Pourcentage']]},
                            {'title': 'Pourcentage d\'étudiantes inscrites en tous les grades au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,30]}},
                        
                        ]),
                ]),
                bgcolor='White',
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                font={'size':18, 'color':'firebrick'},
                bordercolor='lightgreen'
            ),
        ]
    )
    
    fig.update_traces(mode="markers+lines")
    fig.update_layout(hovermode="x")
    fig.update_layout(plot_bgcolor = '#f1f1f1',
                    paper_bgcolor='#f1f1f1',
                    yaxis_range=[0,30],
                    yaxis_title='Pourcentage')
    fig.update_layout(title = 'Pourcentage d\'étudiantes inscrites au baccalauréat au semestre d\'automne de chaque année',title_font_family = "Times New Roman",
                      title_font_color = "black",
                      title_font_size = 18,
                      xaxis_title_font_size = 14,
                      yaxis_title_font_size = 14,)
    fig.update_xaxes(tickangle=-45, tickfont = {'size': 10})
    return fig


def add_etudiants_etrangers_chart(df):
    df['Session'] = df['Trimestre'] % 10

    # On combine les grades 'Maitrise professionnelle' et 'Maitrise recherche' dans le grade 'Maitrise'
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'

    # On garde que 4 grades : 'Bac', 'Maitrise', 'Certificat' et 'Doctorat'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]
    df_test = df

    df_etranger = internationals_data(df_test)
    df_local = local_data(df_test)

    df_etranger_bac = df_etranger.loc[df_etranger['Grade'] == 'Bac']
    df_etranger_bac = df_etranger_bac.tail(10)

    df_etranger_maitrise = df_etranger.loc[df_etranger['Grade'] == 'Maitrise']
    df_etranger_maitrise = df_etranger_maitrise.tail(10)

    df_etranger_phd = df_etranger.loc[df_etranger['Grade'] == 'Doctorat']
    df_etranger_phd = df_etranger_phd.tail(10)

    df_local_maitrise = df_local.loc[df_local['Grade'] == 'Maitrise']
    df_local_maitrise = df_local_maitrise.tail(10)

    df_local_phd = df_local.loc[df_local['Grade'] == 'Doctorat']
    df_local_phd = df_local_phd.tail(10)

    df_local_bac = df_local.loc[df_local['Grade'] == 'Bac']
    df_local_bac = df_local_bac.tail(10)


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_etranger_bac['ANNEE'],
        y=df_etranger_bac['Pourcentage'],
        marker_color = '#fa961e',
        hovertemplate='<b>Pourcentage</b> : %{y:.2f}  <extra></extra>',
        name = 'Etudiants étrangers', # Style name/legend entry with html tags
    ))
    fig.add_trace(go.Scatter(
        x=df_local_bac['ANNEE'],
        y=df_local_bac['Pourcentage'],
        marker_color = '#8cc83c',
        hovertemplate='<b>Pourcentage</b> : %{y:.2f} %<extra></extra>',
        name='Etudiants canadiens ou résidents',
    ))

    fig.update_layout(
        updatemenus=[
            dict(
                type = "buttons",
                direction = "right",
                buttons=list([
                    dict(
                        label="  Baccalauréat  ",
                        method="update",
                        args=[{'y':[df_etranger_bac['Pourcentage'], df_local_bac['Pourcentage']]},
                            {'title': 'Évolution du pourcentage d\'étudiants Canadiens et étrangers  inscrits au baccalauréat au semestre d\'automne',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,100]}},
                        
                        ]),
                    dict(
                        label="  Maîtrise  ",
                        method="update",
                        args=[{
                            'y':[df_etranger_maitrise['Pourcentage'], df_local_maitrise['Pourcentage']]},
                            {'title': 'Évolution du pourcentage d\'étudiants Canadiens et étrangers inscrits en maîtrise au semestre d\'automne ',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,100]}},
                        ]),
                    dict(
                        label="   PhD   ",
                        method="update",
                        args=[{'y':[df_etranger_phd['Pourcentage'], df_local_phd['Pourcentage']]},
                            {'title': 'Évolution du pourcentage d\'étudiants Canadiens et étrangers inscrits en doctorat au semestre d\'automne ',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,100]}},
                        
                        ]),
                ]),
                bgcolor='White',
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                font={'size':18, 'color':'firebrick'},
                bordercolor='lightgreen'
            ),
        ]
    )

    fig.update_traces(mode="markers+lines")
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title= 'Statut légal')
    fig.update_layout(plot_bgcolor = '#f1f1f1',
                        paper_bgcolor='#f1f1f1',
                        yaxis_range=[0,100],
                        yaxis_title='Pourcentage')
    fig.update_layout(title = 'Évolution du pourcentage d\'étudiants Canadiens et étrangers inscrits au baccalauréat au semestre d\'automne ',title_font_family = "Times New Roman",
                      title_font_color = "black",
                      title_font_size = 18,
                      xaxis_title_font_size = 14,
                      yaxis_title_font_size = 14,)
    fig.update_xaxes(tickangle=-45, tickfont = {'size': 10})
    return fig

def add_nouvelles_etudiantes_chart(df):
    # On crée une nouvelle colonne qui contiendra la session (1: Hiver, 2: Eté, 3: Automne)
    df['Session'] = df['Trimestre'] % 10

    # On combine les grades 'Maitrise professionnelle' et 'Maitrise recherche' dans le grade 'Maitrise'
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'

    # On garde que 4 grades : 'Bac', 'Maitrise', 'Certificat' et 'Doctorat'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]

    df_new_F_inscriptions = nouvelle_inscription_fille_bac(df) # Nouvelles inscriptions en automne au Bac
    df3 = df.loc[df['Sexe'] == 'F']
    df4 = df3.loc[df3['Grade'] == 'Bac']
    df_new_F_inscriptions_combinees = df4.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees['Pourcentage']  = (df_new_F_inscriptions_combinees['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100

    df_new_F_inscriptions_combinees = df_new_F_inscriptions_combinees.tail(10)
    df_new_F_inscriptions = df_new_F_inscriptions.tail(10)

    df_new_F_inscriptions_msc = nouvelle_inscription_fille_msc(df)
    df_maitrise_inter = df3.loc[df3['Grade'] == 'Maitrise']
    df_new_F_inscriptions_combinees_msc = df_maitrise_inter.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees_msc['Pourcentage']  = (df_new_F_inscriptions_combinees_msc['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    df_new_F_inscriptions_combinees_msc = df_new_F_inscriptions_combinees_msc.tail(10)

    df_new_F_inscriptions_phd = nouvelle_inscription_fille_phd(df)
    df_phd_inter = df3.loc[df3['Grade'] == 'Doctorat']
    df_new_F_inscriptions_combinees_phd = df_phd_inter.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees_phd['Pourcentage']  = (df_new_F_inscriptions_combinees_phd['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    df_new_F_inscriptions_combinees_phd = df_new_F_inscriptions_combinees_phd.tail(10)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_new_F_inscriptions['ANNEE'],
        y=df_new_F_inscriptions['Pourcentage'],
        marker_color = '#fa961e',
        hovertemplate='<b>Pourcentage : %{y:.2f} % <extra></extra>',
        name = 'Semestre d\'automne', # Style name/legend entry with html tags
    ))
    fig.add_trace(go.Scatter(
        x=df_new_F_inscriptions_combinees['ANNEE'],
        y=df_new_F_inscriptions_combinees['Pourcentage'],
        marker_color = '#8cc83c',
        hovertemplate='<b>Pourcentage : %{y:.2f} % <extra></extra>',
        name='Tous semestres confondus',
    ))


    fig.update_layout(
        updatemenus=[
            dict(
                type = "buttons",
                direction = "right",
                buttons=list([
                    dict(
                        label="  Baccalauréat  ",
                        method="update",
                        args=[{'y':[df_new_F_inscriptions['Pourcentage'], df_new_F_inscriptions_combinees['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiantes nouvellement inscrites au baccalauréat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        
                        ]),
                    dict(
                        label="  Maîtrise  ",
                        method="update",
                        args=[{
                            'y':[df_new_F_inscriptions_msc['Pourcentage'], df_new_F_inscriptions_combinees_msc['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiantes nouvellement inscrites en maîtrise au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        ]),
                    dict(
                        label="  PhD  ",
                        method="update",
                        args=[{'y':[df_new_F_inscriptions_phd['Pourcentage'], df_new_F_inscriptions_combinees_phd['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiantes nouvellement inscrites en doctorat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        
                        ]),
                ]),
               bgcolor='White',
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                font={'size':18, 'color':'firebrick'},
                bordercolor='lightgreen'
            ),
        ]
    )

    
    fig.update_traces(mode="markers+lines")
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title= 'Semestre')
    fig.update_layout(plot_bgcolor = '#f1f1f1',
                        paper_bgcolor='#f1f1f1',
                        yaxis_range=[0,35],
                        yaxis_title='Pourcentage')
    fig.update_layout(title = 'Évolution du nombre d\'étudiantes nouvellement inscrites au baccalauréat au semestre d\'automne de chaque année',title_font_family = "Times New Roman",
                      title_font_color = "black",
                      title_font_size = 18,
                      xaxis_title_font_size = 14,
                      yaxis_title_font_size = 14,)
    fig.update_xaxes(tickangle=-45, tickfont = {'size': 10})
    return fig

def add_nouveaux_etrangers_chart(df):
    # On crée une nouvelle colonne qui contiendra la session (1: Hiver, 2: Eté, 3: Automne)
    df['Session'] = df['Trimestre'] % 10

    # On combine les grades 'Maitrise professionnelle' et 'Maitrise recherche' dans le grade 'Maitrise'
    df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'

    # On garde que 4 grades : 'Bac', 'Maitrise', 'Certificat' et 'Doctorat'
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]

    df_new_F_inscriptions = nouvelle_inscription_etrangers_bac(df) # Nouvelles inscriptions en automne au Bac
    df3 = df.loc[df['Statut_legal'] == 'Etranger']
    df4 = df3.loc[df3['Grade'] == 'Bac']
    df_new_F_inscriptions_combinees = df4.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees['Pourcentage']  = (df_new_F_inscriptions_combinees['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100

    df_new_F_inscriptions_combinees = df_new_F_inscriptions_combinees.tail(10)
    df_new_F_inscriptions = df_new_F_inscriptions.tail(10)
 
    df_new_F_inscriptions_msc = nouvelle_inscription_etrangers_msc(df)
    df_maitrise_inter = df3.loc[df3['Grade'] == 'Maitrise']
    df_new_F_inscriptions_combinees_msc = df_maitrise_inter.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees_msc['Pourcentage']  = (df_new_F_inscriptions_combinees_msc['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    df_new_F_inscriptions_combinees_msc = df_new_F_inscriptions_combinees_msc.tail(10)

    df_new_F_inscriptions_phd = nouvelle_inscription_etrangers_phd(df) 
    df_phd_inter = df3.loc[df3['Grade'] == 'Doctorat']
    df_new_F_inscriptions_combinees_phd = df_phd_inter.groupby('ANNEE', as_index = False).size()
    df2 = filtrer_dataframe(df)
    df_new_F_inscriptions_combinees_phd['Pourcentage']  = (df_new_F_inscriptions_combinees_phd['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    df_new_F_inscriptions_combinees_phd = df_new_F_inscriptions_combinees_phd.tail(10)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_new_F_inscriptions['ANNEE'],
        y=df_new_F_inscriptions['Pourcentage'],
        marker_color = '#fa961e',
        hovertemplate='<b>Pourcentage : %{y:.2f} % <extra></extra>',
        name = 'Semestre d\'automne', # Style name/legend entry with html tags
    ))
    fig.add_trace(go.Scatter(
        x=df_new_F_inscriptions_combinees['ANNEE'],
        y=df_new_F_inscriptions_combinees['Pourcentage'],
        marker_color = '#8cc83c',
        hovertemplate='<b>Pourcentage : %{y:.2f} % <extra></extra>',
        name='Tous semestres confondus',
    ))


    fig.update_layout(
        updatemenus=[
            dict(
                type = "buttons",
                direction = "right",
                buttons=list([
                    dict(
                        label="   Baccalauréat   ",
                        method="update",
                        args=[{'y':[df_new_F_inscriptions['Pourcentage'], df_new_F_inscriptions_combinees['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiants étrangers nouvellement inscrits au baccalauréat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        
                        ]),
                    dict(
                        label="   Maîtrise   ",
                        method="update",
                        args=[{
                            'y':[df_new_F_inscriptions_msc['Pourcentage'], df_new_F_inscriptions_combinees_msc['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiants étrangers nouvellement inscrits en maîtrise au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        ]),
                    dict(
                        label="   PhD   ",
                        method="update",
                        args=[{'y':[df_new_F_inscriptions_phd['Pourcentage'], df_new_F_inscriptions_combinees_phd['Pourcentage']]},
                            {'title': 'Évolution du nombre d\'étudiants étrangers nouvellement inscrits en doctorat au semestre d\'automne de chaque année',
                            'yaxis': {'title': 'Pourcentage', 'range' : [0,35]}},
                        
                        ]),
                ]),
                bgcolor='White',
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                font={'size':18, 'color':'firebrick'},
                bordercolor='lightgreen'
            ),
        ]
    )

    
    fig.update_traces(mode="markers+lines")
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title= 'Semestre')
    fig.update_layout(plot_bgcolor = '#f1f1f1',
                        paper_bgcolor='#f1f1f1',
                        yaxis_range=[0,35],
                        yaxis_title='Pourcentage')
    fig.update_layout(title = 'Évolution du nombre d\'étudiants étrangers nouvellement inscrits au baccalauréat au semestre d\'automne de chaque année',title_font_family = "Times New Roman",
                      title_font_color = "black",
                      title_font_size = 18,
                      xaxis_title_font_size = 14,
                      yaxis_title_font_size = 14,)
    #fig.show()
    fig.update_xaxes(tickangle=-45, tickfont = {'size': 10})
    return fig

