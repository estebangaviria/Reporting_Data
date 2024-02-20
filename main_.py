# %% [markdown]
# ## Import Section

# %%
import pandas as pd
import numpy as np 
import time
from datetime import datetime
from datetime import date
import os
import glob
import re

# %% [markdown]
# ## Config Section

# %%
#MSC
#path = 'C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting'
path = 'C:/Users/Administrator/OneDrive - Griky/Documentos - Griky Dashboard/Reporting'


dataframes = []


# Udemy progress MSC
path_udemy_course_activity = f'{path}/Griky/Fuente/Catálogos/Udemy_msc/User_course_activity/'
# Udemy users MSC
path_udemy_user_activity = f'{path}/Griky/Fuente/Catálogos/Udemy_msc/User_activity/'


# Udemy progress OKTA
#path_udemy_course_activity = 'C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting/Griky/Fuente/Catálogos/Udemy_okta/User_course_activity/'

# Learnlight progress MSC
path_learnlight_progress_report= f'{path}/Griky/Fuente/Catálogos/Learnlight_msc/Progreso_report/'

#Netzun progress
path_netzun_report_full_students = f'{path}/Griky/Fuente/Catálogos/Netzun/report_full_students/'
#Netzun users



# %%
today = date.today()
d1 = today.strftime("%m-%d-%Y")

# %% [markdown]
# ## Functions Section

# %%
def get_concatenated_files_msc(path, folder_name = 'Learner_overview', file_name= 'learner-overview', file_type = '.csv'):
    # path = Contains the path: "C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting"
    # folder_name = Name of the folder that contains the files
    # file_name = common part of the file to search
    # file_type = extension of the file: .csv, .xls, .xlsx
    dataframes = []
    for client_folder in os.listdir(path):
        path_cliente = os.path.join(path, client_folder, folder_name)
        if os.path.isdir(path_cliente):
            files = glob.glob(os.path.join(path_cliente, f'*-{file_name}-*{file_type}'))
            if files:
                # ordenar los archivos por la fecha en su nombre
                files.sort(key=lambda x: x.split(f'-{file_name}-')[-1], reverse=True)
                # abrir el archivo más reciente y cargarlo en un dataframe
                df = pd.read_csv(files[0])
                df = df.dropna(axis=0, how='all')
                df = df.dropna(axis=1, how='all')
                df['Cliente'] = client_folder
                # extract the date from the filename
                date_str = files[0].split(f'-{file_name}-')[1].split('-')[0:3]
                date_str = '-'.join(date_str)
                date = datetime.strptime(date_str, "%Y-%m-%d")
                df['fecha_archivo'] = date.date()
                # agregar el dataframe a la lista
                dataframes.append(df)
    df_final = pd.concat(dataframes)
    return df_final

# %%
def get_last_file(path, file_name, file_type, date_format = "%Y-%m-%d"):
    # Buscar todos los archivos que coinciden con el patrón en el directorio
    files = glob.glob(os.path.join(path, f'{file_name}_*{file_type}'))
    
    if not files:
        return None     # No se encontraron archivos
    
    # Ordenar los archivos por fecha y seleccionar el último
    files.sort(key=lambda x: datetime.strptime(x.split(f'{file_name}_')[-1].split('.')[0], date_format), reverse=True)
    
    # Lee el archivo en un pandas DataFrame
    if file_type == '.csv':
        df = pd.read_csv(files[0])
    elif file_type in ['.xlsx', '.xls']:
        df = pd.read_excel(files[0])
    else:
        print('File type not supported')
        return None

    return df  # Devuelve el DataFrame
    

# %%
def get_last_file_new(path, file_type='.xlsx', date_format="%Y-%m-%d", regex_pattern=None):
    all_files = glob.glob(os.path.join(path, f'*{file_type}'))
    
    # Check if any files were found
    if not all_files:
        return None
    
    if regex_pattern:
        date_files = []
        for file in all_files:
            dates = re.findall(regex_pattern, file)
            if dates:
                last_date = max(datetime.strptime(date, date_format) for date in dates)
                date_files.append((last_date, file))
        
        # Sort the files by date
        date_files.sort(reverse=True)
        latest_file = date_files[0][1]
        print("Latest file date is: ", date_files[0][0])
    else:
        latest_file = max(all_files, key=os.path.getctime)

    # Read the file into a DataFrame
    if file_type == '.csv':
        df = pd.read_csv(latest_file)
    elif file_type in ['.xlsx', '.xls']:
        df = pd.read_excel(latest_file)
    else:
        print('File type not supported')
        return None

    return df

# %% [markdown]
# ## Get Dataframes

# %% [markdown]
# ### Progreso dataframes

# %%
df_progreso_msc = get_concatenated_files_msc(path = path, folder_name = 'Learner_engagement', file_name= 'learner-engagement')
df_progreso_msc.head(1)

# %%
#df_progreso_udemy = get_last_file(path_udemy_course_activity, file_name= 'user_course_activity_report_griky-myskillcamp', file_type='.csv')
df_progreso_udemy = get_last_file_new(path_udemy_course_activity, file_type='.csv', date_format= "%Y-%m-%d", regex_pattern= r'\d{4}-\d{2}-\d{2}')
df_progreso_udemy.sample(10).head(1)

# %%
df_progreso_netzun = get_last_file_new(path_netzun_report_full_students, file_type='.xlsx', 
                               date_format="%m-%d-%Y", 
                               regex_pattern=r'\d{2}-\d{2}-\d{4}')
df_progreso_netzun.sample(10).head(1)

# %%
df_progreso_learnlight = get_last_file_new(path_learnlight_progress_report, file_type='.xlsx', 
    date_format= "%Y-%m-%d", 
    regex_pattern=r'\d{4}-\d{2}-\d{2}')
df_progreso_learnlight = df_progreso_learnlight.drop([0,1])
df_progreso_learnlight.columns = df_progreso_learnlight.iloc[0]
df_progreso_learnlight =df_progreso_learnlight[1:]
df_progreso_learnlight = df_progreso_learnlight.reset_index(drop=True)
df_progreso_learnlight.head(5)

# %% [markdown]
# ### Usuarios Dataframes

# %%
df_usuarios_msc = get_concatenated_files_msc(path = path, folder_name = 'Learner_overview', file_name= 'learner-overview')
df_usuarios_msc.sample(1).head(1)

# %%
df_usuarios_udemy = get_last_file(path_udemy_user_activity, file_name= 'user_activity_report_griky-myskillcamp', file_type='.csv')
df_usuarios_udemy.sample(3)

# %% [markdown]
# ## Modify Data Frames

# %% [markdown]
# ### Config dict

# %%
rename_dic_progreso_udemy = {
    #“old_column_name” : “new_column_name”
    'User First Name' : 'First Name', 
    'User Last Name' : 'Last Name', 
    'User Email' : 'Email Address', 
    #'External ID' : '',
    #'User Groups', 
    'Course ID' : 'Content ID' , 
    'Course Title' : 'Content Title', 
    #'Course Locale',
    'Course Duration' : 'Estimated course duration (min)', #revisar unidades
    '% Marked Completed' : 'Progress (%)', #modify units
    'Minutes Video Consumed' : 'Learning Time (min)', #modify units
    'Date Enrolled' : 'Enrolment Date', #Modify dates format
    'Date Started' : 'Start Date',  #Modify dates format
    #'First Date Completed',
    'Date Completed' : 'Completion Date',  #Modify dates format
    #'Date Last Active', 
    'Course Category' : 'Categories',  
    #'Assigned',
    #'Assigned By', 
    #'User Is Deactivated'


}


rename_dic_progreso_netzun = {
    #“old_column_name” : “new_column_name”
    
    "ID" : "ID Learner",
    'Nombres y Apellidos' : 'Name',
    'Email' : 'Email Address', 
    #'Función' : '', 
    'Curso' : 'Content Title',
    'Inscripción del curso' :  'Enrolment Date', 
    'Estado de curso' : 'Status',
    #'Lecciones Tomadas/Total Lecciones', 
    'Porcentaje de Progreso' : 'Progress (%)' ,  #Modificar unidades
    'Tiempo total' : 'Learning Time (min)' ,    # Pasar a minutos
    #'Puntaje Porcentaje', 
    'Fecha última lección' : 'Date Last Active',
    #'Fecha Deadline', 
    #'Áreas' : 'Cliente',  #Modificar nombres para que coincida 
    #'Código Interno', 
    #'Filtro'
}

rename_dic_progreso_learnlight = {
    #“old_column_name” : “new_column_name”

    'Nombre': 'First Name' , 
    'Apellido' : 'Last Name', 
    'Correo electrónico' : 'Email Address' , 
    'Asignatura' : 'Content Title', 
    #'Servicio', 
    #'Complementos', 
    'Curso actual' : 'Content Title_',
    'Progreso del curso actual' : 'Progress (%)', 
    #'Tiempo de conexión',
    'Tiempo de estudio total (HH:mm)' : 'Learning Time (min)',
    # 'Tiempo actividades interactivas',
    # 'Total de actividades completadas',
    # 'Total de actividades - puntuación media', 
    # 'Examen de progreso 1',
    # 'Examen de progreso 2', 'Examen de progreso 3',
    # 'Examen de progreso - puntuación media',
    # 'Actividades autoestudio del itinerario pedagógico',
    # 'Actividades autoestudio del itinerario pedagógico - puntuación media',
    # 'Actividades autoestudio personalizadas',
    # 'Actividades autoestudio personalizadas - puntuación media',
    # 'Actividades de la Revista',
    # 'Actividades de la Revista - puntuación media',
    # 'Actividades realizadas en sesiones con formador',
    # 'Actividades sesiones Café', 'Prueba final', 'Socio', 'Empresa',
    # 'Puesto de trabajo', 'Director', 'Departamento', 'Entidad operativa',
    #'Entidad de facturación' : 'Cliente', 
    # 'País', 'Ciudad',
    'Fecha de inicio del programa' : 'Enrolment Date', 
    #'Fecha de fin del programa',
    #'Estado del Perfil'
}

final_feautres_dic_progreso_udemy = [

    'Email Address', 
    'Content ID' , 
    'Content Title', 
    'Estimated course duration (min)', #revisar unidades
    'Progress (%)', #modify units
    'Status',
    'Learning Time (min)', #modify units
    'Enrolment Date', #Modify dates format
    'Start Date',  #Modify dates format
    'Completion Date',
    'Date Last Active',
    'Categories',
    'Cliente',
    'Catalogo'
]

final_feautres_dic_progreso_netzun = [
    #“old_column_name” : “new_column_name”
    
    "ID Learner",
    'Name',
    'Email Address', 
    'Content Title',
    'Enrolment Date', 
    'Completion Date',
    'Date Last Active',
    'Status',
    'Progress (%)' ,  #Modificar unidades
    'Learning Time (min)' ,    # Pasar a minutos
    'Cliente',  #Modificar nombres para que coincida 
    'Catalogo'
]

final_feautres_dic_progreso_learnlight = [
    #“old_column_name” : “new_column_name”

    'Name',
    'Email Address', 
    'Content Title',
    'Enrolment Date', 
    #'Completion Date',
    #'Date Last Active',
    'Status',
    'Progress (%)' ,  #Modificar unidades
    'Learning Time (min)' ,    # Pasar a minutos
    'Cliente',  #Modificar nombres para que coincida 
    'Catalogo'
]

final_feautres_dic_progreso_msc = [
    #'ID Learner',
    'Email Address',
    'Content ID', 
    'Content Type',
    #'Training Type', 
    'Content Title', 
    #'Session Title', 
    'Categories', 
    'Camps Published',
    'Content Provider', 
    'Creator', 
    'Trainer(s)', 
    'Creation date',  #Course creation date
    'Last update',    #Course last update
    'Skills', 
    'Language', 
    'Estimated course duration (min)',
    'Status', 
    'Progress (%)', 
    'Learning Time (min)', 
    'Score (%)',
    'Enrolment Date', 
    'Start Date', 
    'Completion Date', 
    'Cliente',
    'Name',
    'Catalogo',
    'Certified',
    'Certificate URL'
    
]
    
    

# %%
rename_dic_progreso_netzun_cliente = {
    'ALATA' : 'Alata',
    'Anahuac' : 'Anahuac',
    'Autónoma' : 'Autonoma',
    'BD Guidance' : 'Bdguidance',
    'Buencafé' : 'Buencafe',
    'CCB' : 'Ccb',
    'CEIPA' : 'Ceipa',
    'Class-run' : 'Classrun', 
    'Colsubsidio' :  'Colsubsidio',   #REVISAR
    'Corona' : 'Corona',
    'DALTA' : 'Dalta',
    'EANX' : 'Eanx', 
    'EDP' : 'Edp',
    'Eficacia' : 'Eficacia',
    'EIG' : 'Globali',
    'FinT Coach' : 'FinT Coach',   #REVISAR
    'Fundación Neón' : 'Holastaff',
    'Griky' : 'Griky',
    'INCAP' : 'Incap',
    'Incurso' : 'Incurso',
    'INMED' : 'Inmed',
    'Insurgentes' : 'Uinsurgentes',
    'ISTEONLINE' : 'ISTE',        #REVISAR
    'Jerarquicos' : 'Jerarquicos',
    'POLI' : 'Poli',
    'RDITS' : 'RD_ITS',
    'SECORSE' : 'Secorse',
    'Streaming Learning' : 'Streaminglearning',
    'SURA' : 'Sura',
    'Sysneo' : 'Central+',
    'Teleperformance' : 'Teleperformance',
    'UCPx' : 'Ucpx',
    'UDES' : 'Udes',
    'UGB' : 'Ugb',
    'UGC' : 'Ugc',
    'UMA' : 'Uma',
    'UMB' : 'Umb',
    'UNE' : 'Une',
    'Uniagustiniana' : 'UniAgustiniana',
    'UNIBE' : 'Unibe',
    'UNIR' : 'Unir', 
    'UPARSISTEM' : 'Uparsistem',
    'USAP' : 'Usap',
    'UST Plus' : 'SantoTomas',
    'UTESA' : 'Utesa', 
    'UTMA' : 'Utma',
    'WURTH' : 'Wurth'
    
    
}

# %% [markdown]
# ### Usuarios MSC

# %%
df_usuarios_msc = df_usuarios_msc[~((df_usuarios_msc['Cliente'] != "Griky" )  & (df_usuarios_msc['Email Address'].str.contains('griky')))]


# %%
usuarios_griky = df_usuarios_msc[df_usuarios_msc['Cliente'] == 'Griky']['Email Address']
not_griky = df_usuarios_msc['Cliente'] != 'Griky'
in_list = df_usuarios_msc['Email Address'].isin(usuarios_griky)
filter_ = not_griky & in_list
df_usuarios_msc = df_usuarios_msc[~filter_]
duplicated_df = df_usuarios_msc[df_usuarios_msc.duplicated(subset='Email Address', keep=False)]
df_usuarios_msc = df_usuarios_msc.drop_duplicates(subset='Email Address', keep='last')
#df_usuarios_msc[ 'Email Address'] = df_usuarios_msc['Email Address'].str.lower().str.strip()
df_usuarios_msc['Email Address'] = df_usuarios_msc['Email Address'].str.lower().str.strip()  #.str.replace('[^a-zA-Z@.]', '', regex=True)
df_usuarios_msc['Activation Date'] = pd.to_datetime(df_usuarios_msc['Activation Date']).dt.normalize()
df_usuarios_msc['Last connection date'] = pd.to_datetime(df_usuarios_msc['Last connection date']).dt.normalize()

# %% [markdown]
# ### Usuarios Udemy MSC

# %%
df_usuarios_udemy.head(1)

# %%
df_usuarios_udemy.shape

# %%
df_usuarios_udemy = df_usuarios_udemy.merge(df_usuarios_msc[['Email Address', 'Cliente']], left_on='User Email', right_on= 'Email Address' ,how='left')


# %% [markdown]
# ### Progreso_msc

# %%
df_progreso_msc['Name'] = df_progreso_msc['First Name'] + " " + df_progreso_msc['Last Name']
df_progreso_msc['Camps Published'] = df_progreso_msc['Camps Published'].str.lower()
df_progreso_msc = df_progreso_msc[df_progreso_msc['Content Type'] != 'External content']
condition_external_catalog = (
        (df_progreso_msc['Content Type'] == 'Pinned content') 
        & 
        (
            (df_progreso_msc['Camps Published'].str.contains('netzun')) | (df_progreso_msc['Camps Published'].str.contains('udemy'))
        )
    )

df_progreso_msc = df_progreso_msc[ ~condition_external_catalog]
df_progreso_msc['Catalogo'] = 'MSC'
df_progreso_msc['Status'] = df_progreso_msc['Status'].replace({
                                                                'Not started' : 'Not Started',
                                                                'In progress' : 'In Progress'
                                                               })
df_progreso_msc['Email Address'] = df_progreso_msc['Email Address'].str.lower().str.strip() #.str.replace('[^a-zA-Z@.]', '', regex=True)
df_progreso_msc['Progress (%)'] = df_progreso_msc['Progress (%)'].fillna(np.nan).astype('Int16')
df_progreso_msc['Enrolment Date'] = pd.to_datetime(df_progreso_msc['Enrolment Date']).dt.normalize()
df_progreso_msc['Completion Date'] = pd.to_datetime(df_progreso_msc['Completion Date']).dt.normalize()
df_progreso_msc['Start Date'] = pd.to_datetime(df_progreso_msc['Start Date']).dt.normalize()
df_progreso_msc['Creation date'] = pd.to_datetime(df_progreso_msc['Creation date']).dt.normalize()
df_progreso_msc['Last update'] = pd.to_datetime(df_progreso_msc['Last update']).dt.normalize()
df_progreso_msc = df_progreso_msc[final_feautres_dic_progreso_msc]

# %% [markdown]
# ### Progreso_udemy

# %%
df_progreso_udemy.rename(columns=rename_dic_progreso_udemy, inplace=True)
df_progreso_udemy['Name'] = df_progreso_udemy['First Name'] + " " + df_progreso_udemy['Last Name'] 
df_progreso_udemy['Email Address'] = df_progreso_udemy['Email Address'].str.lower().str.strip() #.str.replace('[^a-zA-Z@.]', '', regex=True)
df_progreso_udemy = df_progreso_udemy.merge(df_usuarios_msc[['Email Address', 'Cliente']], on='Email Address', how='left')
df_progreso_udemy['Catalogo'] = 'Udemy'
#df['Status'] = df['Progress (%)'].apply(lambda x: 'Completed' if x == 100 else ('Not Started' if pd.isnull(x) or x==0 else 'In Progress'))
df_progreso_udemy['Status'] = df_progreso_udemy['Progress (%)'].apply( lambda x: 'Completed' if x == 100 else ('Not Started' if pd.isnull(x) or x == 0 else 'In Progress'))
df_progreso_udemy['Progress (%)'] = df_progreso_udemy['Progress (%)'].fillna(np.nan).astype('Int16')
df_progreso_udemy['Enrolment Date'] = pd.to_datetime(df_progreso_udemy['Enrolment Date'], utc=True).dt.tz_localize(None).dt.normalize()
df_progreso_udemy['Start Date'] = pd.to_datetime(df_progreso_udemy['Start Date'], utc=True).dt.tz_localize(None).dt.normalize()
df_progreso_udemy['Completion Date'] = pd.to_datetime(df_progreso_udemy['Completion Date'], utc=True).dt.tz_localize(None).dt.normalize()
df_progreso_udemy['Date Last Active'] = pd.to_datetime(df_progreso_udemy['Date Last Active'], utc=True).dt.tz_localize(None).dt.normalize()
df_progreso_udemy = df_progreso_udemy[final_feautres_dic_progreso_udemy]


# %% [markdown]
# ### Progreso_netzun

# %%
def convert_to_minutes(time_string):
    h, m, s = map(int, time_string.split(':'))
    return h*60 + m + s/60

# %%
df_progreso_netzun = df_progreso_netzun.merge(df_usuarios_msc[['Email Address','Cliente']], 
                                              left_on='Email', right_on='Email Address', how='left')
df_progreso_netzun['Áreas'] = df_progreso_netzun['Áreas'].replace(rename_dic_progreso_netzun_cliente)
df_progreso_netzun['Cliente'] = df_progreso_netzun['Áreas'].fillna(df_progreso_netzun['Cliente'])
df_progreso_netzun = df_progreso_netzun.drop(['Email Address', 'Áreas'], axis=1)
df_progreso_netzun.rename(columns=rename_dic_progreso_netzun, inplace=True)

df_progreso_netzun['Catalogo'] = 'Netzun'
#df_progreso_netzun['Status'] = df_progreso_netzun['Status'].apply(lambda x: 'Completed' if x == 'Completado con Certificado' or x == 'Completado' else ('Not Started' if x == 'No Iniciado' else 'In Progress' if x == 'En Progreso' else "") )
df_progreso_netzun['Status'] = df_progreso_netzun['Status'].replace({
                                                                        'Completado con Certificado' : 'Completed',
                                                                        'Completado' : 'Completed',
                                                                        'No Iniciado' : 'Not Started',
                                                                        'En Progreso' : 'In Progress' })
df_progreso_netzun['Progress (%)'] = df_progreso_netzun['Progress (%)'].str.replace('%', '').astype('Int16') 
#df_progreso_netzun['Progress (%)'] = df_progreso_netzun['Progress (%)'].str.replace('%', '').str.strip().replace('', np.nan).astype('Int16')
df_progreso_netzun['Learning Time (min)'] = df_progreso_netzun['Learning Time (min)'].apply(convert_to_minutes)
df_progreso_netzun['Date Last Active'] = df_progreso_netzun['Date Last Active'].replace('-', np.nan)
df_progreso_netzun['Completion Date'] = df_progreso_netzun.apply(
    lambda row: row['Date Last Active'] if row['Progress (%)'] == 100 else '', axis=1)
df_progreso_netzun['Email Address'] = df_progreso_netzun['Email Address'].str.lower().str.strip() #.str.replace('[^a-zA-Z@.]', '', regex=True)
df_progreso_netzun['Enrolment Date'] = pd.to_datetime(df_progreso_netzun['Enrolment Date'], format='%d/%m/%Y')
df_progreso_netzun['Completion Date'] = pd.to_datetime(df_progreso_netzun['Completion Date'], format='%d/%m/%Y', errors='coerce')
                                        # pd.to_datetime(df_progreso_consolidado['Date Last Active'], format='%Y/%m/%d', errors='coerce')
# df_progreso_netzun['Completion Date'] = np.where(df_progreso_netzun['Status'] == 'Completed', 
#                                                  pd.to_datetime(df_progreso_netzun['Date Last Active'], format='%d/%m/%Y'), 
#                                                  np.nan)
df_progreso_netzun = df_progreso_netzun[final_feautres_dic_progreso_netzun]


# %% [markdown]
# ### Progreso Learlight

# %%
def convert_to_minutes_(time_string):
    if isinstance(time_string, str):
        h, m = map(int, time_string.split(':'))
        return h*60 + m
    else:
        return time_string  # o cualquier otro valor por defecto para datos no válidos

# %%

df_progreso_learnlight.rename(columns=rename_dic_progreso_learnlight, inplace=True)
df_progreso_learnlight['Name'] = df_progreso_learnlight['First Name'] + " " + df_progreso_learnlight['Last Name'] 
df_progreso_learnlight['Content Title'] = df_progreso_learnlight['Content Title'] + "-" + df_progreso_learnlight['Content Title_'] 
df_progreso_learnlight['Email Address'] = df_progreso_learnlight['Email Address'].str.lower().str.strip() #.str.replace('[^a-zA-Z@.]', '', regex=True)
df_progreso_learnlight = df_progreso_learnlight.merge(df_usuarios_msc[['Email Address', 'Cliente']], on='Email Address', how='left')
df_progreso_learnlight['Catalogo'] = 'Learnlight'
df_progreso_learnlight['Progress (%)'] = df_progreso_learnlight['Progress (%)'].replace([np.inf, -np.inf], np.nan).fillna(0)
df_progreso_learnlight['Progress (%)'] = (df_progreso_learnlight['Progress (%)']*100).round().astype(int)
df_progreso_learnlight['Status'] = df_progreso_learnlight['Progress (%)'].apply( lambda x: 'Completed' if x == 100 else ('Not Started' if pd.isnull(x) or x == 0 else 'In Progress'))
df_progreso_learnlight['Learning Time (min)'] = df_progreso_learnlight['Learning Time (min)'].replace([np.inf, -np.inf, '-'], np.nan).fillna(0)
df_progreso_learnlight['Learning Time (min)'] = df_progreso_learnlight['Learning Time (min)'].apply(convert_to_minutes_)
df_progreso_learnlight['Enrolment Date'] = pd.to_datetime(df_progreso_learnlight['Enrolment Date'], format='%d-%m-%Y')
df_progreso_learnlight = df_progreso_learnlight[final_feautres_dic_progreso_learnlight]


# %% [markdown]
# ## Create Progress DataFrame

# %%
df_progreso_consolidado = pd.concat([df_progreso_msc, df_progreso_udemy,df_progreso_netzun, df_progreso_learnlight], ignore_index=True)
df_progreso_consolidado['Date Last Active'] = pd.to_datetime(df_progreso_consolidado['Date Last Active'], format='%Y/%m/%d', errors='coerce')
df_progreso_consolidado['Date Last Active'] = df_progreso_consolidado['Date Last Active'].dt.date
df_progreso_consolidado['Creation date'] =df_progreso_consolidado['Creation date'].dt.date
df_progreso_consolidado['Last update'] =df_progreso_consolidado['Last update'].dt.date
df_progreso_consolidado['Enrolment Date'] =df_progreso_consolidado['Enrolment Date'].dt.date
df_progreso_consolidado['Start Date'] =df_progreso_consolidado['Start Date'].dt.date
#df_progreso_consolidado['Completion Date'] = pd.to_datetime(df_progreso_consolidado['Completion Date'], format='%Y/%m/%d', errors='coerce')
df_progreso_consolidado['Completion Date'] =df_progreso_consolidado['Completion Date'].dt.date
df_progreso_consolidado.head(1)

# %% [markdown]
# ## Save 

# %%
#df_usuarios_udemy.to_excel('usuarios_udemy.xlsx', index=False)
#df_progreso_msc.to_excel(f'C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting/Griky/Fuente/Consolidado_Learner_Engagement/Progreso_MSC_{d1}.xlsx', index=False)

df_progreso_consolidado.to_excel(f'{path}/Griky/Fuente/Catálogos/4.0 - Consolidado/Historico_Progreso/Progreso_MSC_{d1}.xlsx', index=False)
df_usuarios_msc.to_excel(f'{path}/Griky/Fuente/Catálogos/4.0 - Consolidado/Historico_Usuarios/Usuarios_MSC_{d1}.xlsx', index=False)
# df_progreso_consolidado.to_excel(f'C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting/Griky/Fuente/Catálogos/4.0 - Consolidado/Progreso_MSC.xlsx', index=False)
# df_usuarios_msc.to_excel(f'C:/Users/evanm/Documents/Griky_data/OneDrive - Griky/Documentos - Griky Dashboard/Reporting/Griky/Fuente/Catálogos/4.0 - Consolidado/Usuarios_MSC.xlsx', index=False)



