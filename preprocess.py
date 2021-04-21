'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

# Importation de la dataframe 
df = pd.read_csv('assets/WORK_INSCRIPTION.csv',  encoding='latin1') 

# On crée une nouvelle colonne qui contiendra la session (1: Hiver, 2: Eté, 3: Automne)
df['Session'] = df['Trimestre'] % 10

# On combine les grades 'Maitrise professionnelle' et 'Maitrise recherche' dans le grade 'Maitrise'
df.loc[df.Grade.isin(['Maitrise professionnelle', 'Maitrise recherche']), 'Grade'] = 'Maitrise'

# On garde que 4 grades : 'Bac', 'Maitrise', 'Certificat' et 'Doctorat'
df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Certificat', 'Maitrise'])]

def inscription_automne(df):
    '''
    Une fonction qui ne garde que les inscriptions de la session de l'automne
    '''
    df = df.loc[df['Session'] == 3]
    return df

def filtrer_dataframe(df):
    '''
    On filtre les données pour supprimer les inscriptions redondantes 
    '''
    df.drop_duplicates(subset = ['STUDID'], inplace = True)
    return df

###################################################################
               ###### Visualisation 1 ######
###################################################################

def all_data(df):
    df_female = df.groupby(['ANNEE', 'Session'], as_index =  False).size()
    df_female.rename(columns={'size': 'Nombre'}, inplace = True)
    df_female['Pourcentage'] = (df_female['Nombre'] /  df.groupby(['ANNEE', 'Session'], as_index = False).size()['size']) * 100
    return df_female

def male_data(df):
    df1 = df.loc[df['Sexe'] == 'M']
    df_female = df1.groupby(['ANNEE', 'Session'], as_index =  False).size()
    df_female.rename(columns={'size': 'Nombre'}, inplace = True)
    df_female['Pourcentage'] = (df_female['Nombre'] /  df.groupby(['ANNEE', 'Session'], as_index = False).size()['size']) * 100
    return df_female

def female_data(df):
    '''
    Une fonction qui retourne une dataframe qui contient le nombre et le pourcentage des filles dans chaque session de chaque année
    '''
    df1 = df.loc[df['Sexe'] == 'F']
    df_female = df1.groupby(['ANNEE', 'Session'], as_index =  False).size()
    df_female.rename(columns={'size': 'Nombre'}, inplace = True)
    df_female['Pourcentage'] = (df_female['Nombre'] /  df.groupby(['ANNEE', 'Session'], as_index = False).size()['size']) * 100
    return df_female

def inscription_males_grades(df):
    df1 = inscription_automne(df)
    df2 = df1.loc[df1['Sexe'] == 'M']
    df3 = df2.groupby(['Grade', 'ANNEE'], as_index = False).size()
    df3['Pourcentage'] = (df3['size'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df3

def inscription_all_grades(df):
    df1 = inscription_automne(df)
    df3 = df1.groupby(['Grade', 'ANNEE'], as_index = False).size()
    df3['Pourcentage'] = (df3['size'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df3

def inscription_filles_grades(df):
    '''
    Une fonction qui retourne une dataframe qui contient le nombre et le pourcentage des filles dans chaque grade pendant la session de l'automne
    '''
    df1 = inscription_automne(df)
    df2 = df1.loc[df1['Sexe'] == 'F']
    df3 = df2.groupby(['Grade', 'ANNEE'], as_index = False).size()
    df3['Pourcentage'] = (df3['size'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df3

def nouvelle_inscription_fille_bac(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1)
    df3 = df2.loc[df2['Sexe'] == 'F']
    df4 = df3.loc[df3['Grade'] == 'Bac']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def nouvelle_inscription_etrangers_bac(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1) 
    df3 = df2.loc[df2['Statut_legal'] == 'Etranger']
    df4 = df3.loc[df3['Grade'] == 'Bac']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def nouvelle_inscription_etrangers_msc(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1)
    df3 = df2.loc[df2['Statut_legal'] == 'Etranger']
    df4 = df3.loc[df3['Grade'] == 'Maitrise']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def nouvelle_inscription_fille_msc(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1)
    df3 = df2.loc[df2['Sexe'] == 'F']
    df4 = df3.loc[df3['Grade'] == 'Maitrise']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def nouvelle_inscription_etrangers_phd(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1)
    df3 = df2.loc[df2['Statut_legal'] == 'Etranger']
    df4 = df3.loc[df3['Grade'] == 'Doctorat']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def nouvelle_inscription_fille_phd(df):
    '''
    Une fonction qui retourne une dataframe qui contient les nouvelles inscriptions des filles au bac pendant
    la session de l'automne de chaque année
    '''
    df1 = filtrer_dataframe(df)
    df2 = inscription_automne(df1)
    df3 = df2.loc[df2['Sexe'] == 'F']
    df4 = df3.loc[df3['Grade'] == 'Doctorat']
    df5 = df4.groupby('ANNEE', as_index = False).size()
    df5['Pourcentage']  = (df5['size'] /  df2.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5

def internationals_data(df):
    '''
    Une fonction qui retourne une dataframe qui contient le nombre et le pourcentage des étudiants étrangers pendant la session de l'automne 
    dans chaque année
    '''
    
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Maitrise'])]
    df1 = inscription_automne(df)
    df2 = df1.loc[df1['Statut_legal'] == 'Etranger']
    df_internationals = df2.groupby(['Grade', 'ANNEE'], as_index =  False).size()
    df_internationals.rename(columns={'size': 'Nombre'}, inplace = True)
    df_internationals['Pourcentage'] = (df_internationals['Nombre'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df_internationals

def local_data(df):
    df = df.loc[df.Grade.isin(['Bac', 'Doctorat', 'Maitrise'])]
    df = inscription_automne(df)
    df1 = df.loc[df['Statut_legal'] == 'Resident']
    df2 = df.loc[df['Statut_legal'] == 'Canadien']
    df3 = df1.append(df2)
    df_internationals = df3.groupby(['Grade', 'ANNEE'], as_index =  False).size()
    df_internationals.rename(columns={'size': 'Nombre'}, inplace = True)
    df_internationals['Pourcentage'] = (df_internationals['Nombre'] /  df.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df_internationals



def inscription_all_grades_etrangers(df):
    df1 = inscription_automne(df)
    df2 = df1.loc[df['Statut_legal'] == 'Etranger']
    df3 = df2.groupby(['Grade', 'ANNEE'], as_index = False).size()
    df3['Pourcentage'] = (df3['size'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df3

def inscription_all_grades_locals(df):
    df1 = inscription_automne(df)
    df2 = df.loc[df['Statut_legal'] == 'Resident']
    df3 = df.loc[df['Statut_legal'] == 'Canadien']
    df4 = df2.append(df3)
    df5 = df4.groupby(['Grade', 'ANNEE'], as_index = False).size()
    df5['Pourcentage'] = (df5['size'] /  df1.groupby(['Grade', 'ANNEE'], as_index = False).size()['size']) * 100
    return df5
###################################################################
               ###### Visualisation 2 ######
###################################################################
def filtrer_pays(df, year):
    '''
    Une fonction qui retourne une dataframe contenant le nombre et le pourcentage de étudiants de chaque pays étranger pour une année donnée
    '''
    df.drop(df[df.Statut_legal=="Canadien"].index, inplace = True)
    # ******************************

    df_pays = df.groupby(['ANNEE', 'Pays_Citoyennete','Pays_Citoyennete_ang'], as_index=False).size()

    # ******************************
    df_pays.rename(columns={'size': 'Nombre'}, inplace = True)
    df_annee_total = df.groupby('ANNEE', as_index = False).size()
    df_pays_merged = pd.merge(df_pays, df_annee_total, on='ANNEE')
    df_pays_merged['Pourcentage'] = (df_pays_merged['Nombre'] / df_pays_merged['size']) * 100
    return df_pays_merged.loc[df_pays_merged['ANNEE'] == year]


def meilleurs_pays(df, year):
    '''
    Une fonction qui retourne une liste qui contient les 20 permiers pays qui envoient le plus d'étudiants dans une année donnée
    '''
    df1 = filtrer_pays(df, year)
    df1.sort_values(by = ['Pourcentage'], ascending=False, inplace=True)
    #list_pays =  list(df1['Pays_Citoyennete'])
    list_pays =  list(df1['Pays_Citoyennete_ang'])
    return list_pays[:20]


def evolution_pays(df, year, all_countries):
    '''
    Une fonction qui retourne une dataframe qui contient les nombre des étudiants de chaque pays pendant les 10 dernières années
    N.B : Si le paramètre all_countries = False, la fonction retourne le nombre des étudiants des 20 premiers pays, dans l'année 'year', 
    pendant les 10 dernières années
    '''
    # *******************************************************************************************

    df1 = df.groupby(['Pays_Citoyennete','Pays_Citoyennete_ang', 'ANNEE'], as_index=False).size()

    # *******************************************************************************************
    #  I changed columns with :"Pays_Citoyennete_ang"
    # *******************************************************************************************
    df1_pivot = df1.pivot(index = 'ANNEE', columns = 'Pays_Citoyennete_ang', values = 'size')
    if all_countries == True : 
        return df1_pivot.loc['2011/12':, :]
    else:
        list_pays = meilleurs_pays(df, year)
        df3 = df1.loc[df1['Pays_Citoyennete_ang'].isin(list_pays)]
        df3_pivot = df3.pivot(index = 'ANNEE', columns = 'Pays_Citoyennete_ang', values = 'size')
        return df3_pivot.loc['2011/12':, :]

#df = inscription_automne(df)
#df = evolution_pays(df, '2020/21', False)
#df11 = pd.DataFrame(df.to_records())
#df.to_csv('new_evolution_2020.csv')
###################################################################
               ###### Visualisation 3 ######
###################################################################

def meilleurs_programmes(df):
    '''
    Une fonction qui retourne une liste des 12 programmes les plus populaires dans un grade donné, ici df contient seulement les données du grade donné.
    On rappelle que les programmes les plus populaires sont les programmes ayant le plus grand nombre d'inscrits durant les 23 dernières années
    '''
    df2 = df.groupby('Programme', as_index = False).size()
    df2.sort_values(by = ['size'], ascending=False, inplace=True)
    list_programmes = list(df2['Programme'])[:12]
    return list_programmes

def evolution_programmes(df, grade, all_programs, internationals):
    '''
    Une fonction qui retourne une dataframe qui contient le nombre des inscriptions des différents programmes dans un grade donné
    N.B: Si all_programms = True, la fonction retourne tous les progammes dans ce grade, sinon, elle retourne les 12 programmes les plus populaires
    N.B: Si internationals = True, la fonction retourne le nombre des étudiants internationaux dans les programmes du grade donné, sinon elle retourne
    le nombre de tous les étudiants dans les programmes du grade donné, et ce pour les 10 dernières années.

    '''
    df_grade = df.loc[df['Grade'] == grade]
    list1 = meilleurs_programmes(df_grade)
    if internationals == True:
        df1 = df_grade.loc[df_grade['Statut_legal'] == 'Etranger']
        df_programme_etranger = df1.groupby(['Programme', 'ANNEE'], as_index =  False).size()
        if all_programs == True:
            df_allprog_internationals = df_programme_etranger.pivot(index = 'ANNEE', columns = 'Programme', values = 'size').loc['2011/12':, :]
            df_allprog_internationals['Total'] = df_allprog_internationals.sum(axis = 1, skipna = True)
            return df_allprog_internationals[['Total']]
        else:
            df2 = df_programme_etranger.loc[df_programme_etranger['Programme'].isin(list1)]
            return df2.pivot(index = 'ANNEE', columns = 'Programme', values = 'size').loc['2011/12':, :]
    else:  
        df_programme = df_grade.groupby(['Programme', 'ANNEE'], as_index =  False).size()
        if all_programs == True:
            df_allprog_everyone = df_programme.pivot(index = 'ANNEE', columns = 'Programme', values = 'size').loc['2011/12':, :]
            df_allprog_everyone['Total'] = df_allprog_everyone.sum(axis = 1, skipna = True)
            return df_allprog_everyone[['Total']]
        else:
            df3 = df_programme.loc[df_programme['Programme'].isin(list1)]
            return df3.pivot(index = 'ANNEE', columns = 'Programme', values = 'size').loc['2011/12':, :]