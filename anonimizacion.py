import pandas as pd

def sacar_nan_del_email(df_a_limpiar):
  df_a_limpiar=df_a_limpiar.dropna(subset='Dirección de correo electrónico')
  return  df_a_limpiar

def agregar_columna_id_0(df_limpiar):
  df_limpiar['id']=0
  return df_limpiar

def actualizar_lista_emails(df_a_limpiar, lista_emails, inicio):
  for email in df_a_limpiar['Dirección de correo electrónico']:
    if email not in lista_emails:
      lista_emails.append(email)
  return lista_emails

def trabajar_dataframe(df_a_limpiar, lista_emails, inicio):
  agregar_columna_id_0(df_a_limpiar)
  sacar_nan_del_email(df_a_limpiar)
  lista_emails=actualizar_lista_emails(df_a_limpiar, lista_emails, inicio)
  return lista_emails

def actualizar_dataframe(df_a_limpiar, lista_emails):
  nro=df_a_limpiar['Dirección de correo electrónico'].count()
  count=1
  for email in lista_emails:
    i=0
    for i in range(nro):
      filtro=df_a_limpiar.loc[i, 'Dirección de correo electrónico'] == email
      if filtro:
        df_a_limpiar.loc[i, 'id']=count
    count=count+1
  return df_a_limpiar

#Crear una lista de emails vacia
#lista_emails=[]
#nro=len(lista_emails)

"""
#Listas de dataframes
dfs=[df_a, df_b,df_c,df_d,df_e,df_0,df_f,df_1, df_2]
#Arma la lista de todos los emails:
for df in dfs:
  lista_emails=trabajar_dataframe(df, lista_emails, nro)
  print(len(lista_emails))
  nro=len(lista_emails)+1


#Cambiemos el id
#Los id se crean por el email:
df_mejoradas=[]
for df in dfs:
  df_00=sacar_nan_del_email(df)
  df_00=actualizar_dataframe(df_00, lista_emails)
  df_mejoradas.append(df_00)

##Armar tabla con información sensible
# De las dataframe con el id actualizado solo me quedo con lo sensible y lo uno en una tabla sin tener encuenta los duplicados
lista_info_sensible=['id', 'Dirección de correo electrónico', 'Nombre y apellido', 'Teléfono ']
df_sensible_total=pd.DataFrame(columns=lista_info_sensible)

for df in df_mejoradas:
  df_000=df[lista_info_sensible]
  df_sensible_total=pd.merge(df_sensible_total, df_000, how='outer', indicator=False).drop_duplicates(subset='id')
"""