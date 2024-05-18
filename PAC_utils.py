from datetime import timedelta
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import anonimizacion
import funcion_diccionarios
from dict_productos_por_fecha import lista_terminos_presentes_en_nombres, diccionario_productos, diccionario_2, diccionario_3,diccionario_4,diccionario_5,diccionario_6,diccionario_7,diccionario_8,diccionario_9
#import tablas_Yami

#Nos ponemos a unificar todos los diccionarios de productos. Fecha: 4/5/2024

lista_diccionarios_por_fecha = [diccionario_productos,
                                diccionario_2,
                                diccionario_3,
                                diccionario_4,
                                diccionario_5,
                                diccionario_6,
                                diccionario_7,
                                diccionario_8,
                                diccionario_9]

unificacion_diccionarios_productos = {}
unificacion_diccionarios_productos = lista_terminos_presentes_en_nombres
for lista_productos in lista_diccionarios_por_fecha:
  unificacion_diccionarios_productos = funcion_diccionarios.agregar_a_diccionario_original(unificacion_diccionarios_productos,lista_productos)

print(unificacion_diccionarios_productos)

#unificar los diccionarios funcionó. Fecha: 4/5/2024

def diccionario_nombres_a_unificar(df):
  dict_nombres_nuevos = {}
  for columna in df.columns.values:
    for termino_presente in unificacion_diccionarios_productos.keys():
      if columna.find(termino_presente) >= 0: #es decir, si está #termino_presente.is_in(columna):
        dict_nombres_nuevos[columna] = unificacion_diccionarios_productos[termino_presente]
  return dict_nombres_nuevos

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

#hay que limpiar del excel las filas que ya no tienen productos. Fecha: 6/4/2024

def tomar_pedidos_de_tabla(df_original,cantidad_pedidos):
  df_pedidos = df_original.drop(df_original.index[cantidad_pedidos:],inplace=False)
  return df_pedidos

#tomar_pedidos_del_excel funciona

def transformar_df(df_original,cantidad_pedidos):
  df = tomar_pedidos_de_tabla(df_original,cantidad_pedidos)
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
  #cambiar Nans por ceros en los productos
  df.fillna(value=0,inplace=True)
  #anonimizo
  lista_emails = []
  lista_emails = anonimizacion.trabajar_dataframe(df,lista_emails)
  df = anonimizacion.actualizar_dataframe(df,lista_emails)
  return df

#transformar_df funciona, falta agregarle la anonimización. Fecha: 6/4/2024
#Nans cambiados exitosamente por ceros. Fecha: 4/5/2024

#df_original = pd.read_excel('1 - Entrega 20_5_2023.xlsx')
#print(transformar_df(df_original,64).columns)
#anonimización completada. Fecha: 4/5/2024

#Es posible que haya que corregir algún otro nombre de producto para que no sea falsamente encontrado como parte de otros nombres
#(como pasó con 'sal'). Falta chequear qué ocurre con productos del mismo tipo pero distintas marcas que se ofrecen en una MISMA FECHA
#Fecha: 4/5/2024


