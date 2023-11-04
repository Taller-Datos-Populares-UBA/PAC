from datetime import timedelta
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import tablas_Yami

def transformar_df(df_original):
  df = df_original.copy()
  #genero el diccionario para unificar nombres
  nombres_nuevos_dict = diccionario_nombres_a_unificar(df)
  # filtro columnas y las renombro
  df = filtrar_renombrar_columnas(df,nombres_nuevos_dict)
  #cambio fecha a string para continuar operando
  df['marca_temporal'] = df['marca_temporal'].apply(cambiar_fecha_a_string)
  # agrego fecha_entrega
  df = agregar_fecha_entrega(df)
  # unifico atributo casa_popular
  df['casa_popular'] = df['casa_popular'].apply(parsear_casa_popular)

  return df

def filtrar_renombrar_columnas(df_original,nombres_nuevos_dict):
  df = df_original.copy()
  # me quedo con las columnas que defini en el diccionario
  df = df[nombres_nuevos_dict.keys()]
  # las renombro por comodidad con el mismo diccionario
  df = df.rename(columns=nombres_nuevos_dict)

  return df

def cambiar_fecha_a_string(fecha_completa):
  return fecha_completa.__str__()

def cambiar_string_a_fecha(string):
  fecha = datetime.strptime(string,'%Y-%m-%d')
  print(fecha)
  return fecha

def agregar_fecha_entrega(df_original):
  df = df_original.copy()
  # me quedo solo con la fecha de la marca temporal
  df['marca_temporal'] = df['marca_temporal'].apply(lambda x: x.split(' ')[0])
  df['marca_temporal'] = df['marca_temporal'].apply(cambiar_string_a_fecha)
  # la transformo al sabado de esa semana
  df['fecha_entrega'] = df['marca_temporal'].apply(sabado_posterior)

  return df

def sabado_posterior(fecha):
  sabado = fecha
  while(sabado.weekday() != 5):
    sabado = sabado + timedelta(days = 1)

  return sabado

def parsear_casa_popular(casa_popular):
  try:
    if 'Palermo' in casa_popular:
      return 'palermo'
    elif 'Villa Urquiza' in casa_popular:
      return 'villa urquiza'
    elif 'Villa Crespo' in casa_popular:
      return 'villa crespo'
    elif 'Almagro' in casa_popular:
      return 'almagro'
  except:
      return np.nan

#Acá empezamos a filtrar lo que nos interesa de la tabla transformada

def filtrar_cliente(df,cliente): #se da las fechas como strings
  df_filtrado = df.loc[df["id"] == cliente]
  return df_filtrado

def aplicar_filtros(df, clientes=None, fecha=None, fecha_inicial=None, fecha_final=None, barrios=None):
    df_filtrado = df.copy()

    if clientes:
      df_filtrado = df_filtrado[df_filtrado['id'].isin(clientes)]

    if fecha:
      if fecha_inicial or fecha_final:
        print('Esta mal usada la funcion de filtros (escribir solo fecha, o solo fecha inicial y fecha final)')
      else:
        fecha_inicial = fecha
        fecha_final = fecha
    if fecha_inicial and fecha_final:
      fecha_inicial = pd.to_datetime(fecha_inicial,format='%Y/%m/%d')
      fecha_final = pd.to_datetime(fecha_final,format='%Y/%m/%d')
      df_filtrado = df_filtrado[(df_filtrado['fecha_entrega'] >= fecha_inicial) & (df_filtrado['fecha_entrega'] <= fecha_final)]

    if barrios:
      df_filtrado = df_filtrado[df_filtrado['casa_popular'].isin(barrios)]

    return df_filtrado

#empezamos a cambiar los nombres que incluyen precios por nombres genéricos

lista_terminos_presentes_en_nombres = {'Marca temporal':'marca_temporal',
                                       'Dirección de correo':'email',
                                       'Nombre y apellido':'nombre',
                                       'Bolsón de verduras verdes':'bolson_verdes',
                                       'Bolsón de pesadas':'bolson_pesadas',
                                       'bolsón de verdes + pesadas + maple':'combo_verdes_pesadas_maple',
                                       'bolsón de verdes + bolsón de pesadas':'combo_verdes_pesadas',
                                       'Peras':'pera',
                                       'Huevos':'huevo',
                                       'Bananas':'banana',
                                       'Paltas':'palta',
                                       'Berenjenas':'berenjena',
                                       'Cebollas':'cebolla',
                                       'Limones':'limon',
                                       'Papa blanca':'papa_blanca',
                                       'Manzana roja':'manzana_roja',
                                       'Zapallo':'zapallo',
                                       'Mandarina':'mandarina',
                                       'Naranja de':'naranja',
                                       'Pomelo rosado':'pomelo_rosado',
                                       'Batata morada':'batata_morada',
                                       'Repollo blanco':'repollo_blanco',
                                       'Zapallo anco':'zapallo_anco',
                                       'Zanahoria':'zanahoria',
                                       'Bolsón de frutas':'bolson_frutas',
                                       'Ajo':'ajo',
                                       'Lechuga morada':'lechuga_morada',
                                       'Lechuga francesa':'lechuga_francesa',
                                       'Naranja sanguínea':'naranja_sanguinea',
                                       'Tomate de':'tomate',
                                       'Tomate cherry':'tomate_cherry',
                                       'Manzana verde':'manzana_verde',
                                       'Frutilla':'frutilla',
                                       'Morrón verde':'morron_verde',
                                       '¿Dónde':'casa_popular'}

def diccionario_nombres_a_unificar(df):
  dict_nombres_nuevos = {}
  for columna in df.columns.values:
    for termino_presente in lista_terminos_presentes_en_nombres.keys():
      if columna.find(termino_presente) >= 0: #es decir, si está #termino_presente.is_in(columna):
        dict_nombres_nuevos[columna] = lista_terminos_presentes_en_nombres[termino_presente]
  return dict_nombres_nuevos