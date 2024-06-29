import numpy as np
import pandas as pd
import re
from datetime import timedelta
import dict_productos_por_fecha

def crear_lista_dataframes_entregas(lista_entregas):
  dfs=[]
  for entrega in lista_entregas:
    df= pd.read_excel(entrega)
    dfs.append(df)
  return dfs

def de_nombre_archivo_a_fecha_fea(lista_entregas):
  fechas_feas=[]
  for entrega in lista_entregas:
    palabras=entrega.split()
    fecha=palabras[-1].split('.')
    fechas_feas.append(fecha[0])
  return fechas_feas

def transformar_fechas(fecha_fea):
  separacion=fecha_fea.split("_")
  dia=separacion[0]
  mes=separacion[1]
  anio=separacion[2]
  fecha_limpia=anio+'-'+mes+'-' +dia
  return fecha_limpia

def dar_formato_fechas(lista_fechas_feas):
  lista_fechas_lindas=[]
  for fecha in lista_fechas_feas:
    fecha_renovada=transformar_fechas(fecha)
    fecha=pd.to_datetime(fecha_renovada,format='%Y/%m/%d')
    lista_fechas_lindas.append(fecha)
  return lista_fechas_lindas

def parsear_precios(lista_encabezados,fecha):
    lista_columnas = lista_encabezados.copy()
    lista_fecha = [fecha]
    signo_peso = "$"
    for columna in lista_columnas:
        if signo_peso in columna:
            separacion = columna.split("$")
            nombre_producto=separacion[0]
            precio = separacion[1]
            precio = re.sub('\.','',precio)
            producto=[nombre_producto, int(precio)]
            lista_fecha.append(producto)
    return lista_fecha

def sacar_precios_encabezados(df):
    lista_columnas = df.columns.to_list()
    signo_peso = "$"
    diccionario = {}
    for columna in lista_columnas:
        if signo_peso in columna:
            separacion = columna.split("$")
            nombre_producto=separacion[0]
            diccionario[columna]=nombre_producto
        else:
            diccionario[columna]=columna
    return diccionario

def hacer_lista_precios(lista_precios_fecha_nueva,N):
  lista_precios=[]
  for i in range(1, N):
    lista_precios.append(lista_precios_fecha_nueva[i][1])
  return lista_precios

def hacer_lista_nombres(lista_precios_fecha_nueva,N):
  lista_nombres=[]
  for i in range(1, N):
    lista_nombres.append(lista_precios_fecha_nueva[i][0])
  return lista_nombres

#tenemos que armar la tabla de precios con los nombres simplificados (y que sean iguales a los de las tablas de pedidos transformadas)
#fecha: 15/6/2024

def armar_tabla_precios_una_fecha(df_pedido,fecha_pedido):
  lista_encabezados = df_pedido.columns.to_list()
  lista_fecha = parsear_precios(lista_encabezados,fecha_pedido)
  nombres_columnas = ['fecha_entrega']
  valores = [fecha_pedido]
  for producto in lista_fecha[1:]:
    nombres_columnas.append(producto[0])
    valores.append(producto[1])
  tabla_precios_fecha = pd.DataFrame([valores],columns=nombres_columnas)
  return tabla_precios_fecha

#ahora queremos convertir los nombres complicados de los productos a los simples. Fecha: 15/6/2024


