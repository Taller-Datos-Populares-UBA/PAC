import pandas as pd
import tablas_Yami
import PAC_utils as pac
import funcion_diccionarios
from dict_productos_por_fecha import lista_terminos_presentes_en_nombres, diccionario_productos, diccionario_2, diccionario_3,diccionario_4,diccionario_5,diccionario_6,diccionario_7,diccionario_8,diccionario_9

def unificar_nombres_productos_en_tabla_precios(tabla_precios,diccionario_nombres_nuevos):
  tabla_precios = tabla_precios.rename(columns=diccionario_nombres_nuevos)
  return tabla_precios

def crear_tabla_precios_nombres_nuevos(df_pedido,fecha_pedido):
  tabla_precios_fecha = tablas_Yami.armar_tabla_precios_una_fecha(df_pedido,fecha_pedido)
  nombres_nuevos_dict = pac.diccionario_nombres_a_unificar(tabla_precios_fecha)
  tabla_precios_nombres_nuevos = unificar_nombres_productos_en_tabla_precios(tabla_precios_fecha,nombres_nuevos_dict)
  return tabla_precios_nombres_nuevos

def construir_lista_tablas_precios(lista_entregas):
  dfs_entregas = tablas_Yami.crear_lista_dataframes_entregas(lista_entregas)
  lista_fechas_feas = tablas_Yami.de_nombre_archivo_a_fecha_fea(lista_entregas)
  lista_fechas_lindas = tablas_Yami.dar_formato_fechas(lista_fechas_feas)
  lista_tablas_precios = []
  for k in range(len(lista_entregas)):
    lista_tablas_precios.append(crear_tabla_precios_nombres_nuevos(dfs_entregas[k],lista_fechas_lindas[k]))
  return lista_tablas_precios

def unificar_tablas_precios(tabla_precios_acumulada,tabla_precios_nueva):
  tabla_unificada = pd.concat([tabla_precios_acumulada,tabla_precios_nueva],ignore_index=True)
  return tabla_unificada

def incorporar_nueva_lista_pedidos(df_pedidos_acumulados,excel_pedidos_nuevos):
  df_nuevo_pedido = pd.read_excel(excel_pedidos_nuevos)
  df_agregar = pac.transformar_df(df_nuevo_pedido)
  pedidos_unificados = pd.concat([df_pedidos_acumulados,df_agregar],ignore_index=True)
  return pedidos_unificados

"""
lista_entregas = ['1 - Entrega 20_5_2023.xlsx','2 - Entrega 3_6_2023.xlsx']
lista_tablas_precios = construir_lista_tablas_precios(lista_entregas)
print(unificar_tablas_precios(lista_tablas_precios[0],lista_tablas_precios[1]))
primer_pedido = pd.read_excel('1 - Entrega 20_5_2023.xlsx')
df_primer_pedido = pac.transformar_df(primer_pedido)
df_pedidos_acumulados = incorporar_nueva_lista_pedidos(df_primer_pedido,'2 - Entrega 3_6_2023.xlsx')
print(df_pedidos_acumulados)
"""

lista_entregas = ['2 - Entrega 3_6_2023.xlsx',
                  '3 - Entrega 17_6_2023.xlsx',
                  '4 - Entrega 1_7_2023.xlsx',
                  '5 - Entrega 15_7_2023.xlsx',
                  '6 - Entrega 29_7_2023.xlsx',
                  '7 - Entrega 12_8_2023.xlsx',
                  '8 - Entrega 26_8_2023.xlsx',
                  '9 - Entrega 9_9_2023.xlsx']
lista_tablas_precios = construir_lista_tablas_precios(lista_entregas)
tabla_precios_acumulada = construir_lista_tablas_precios(['1 - Entrega 20_5_2023.xlsx'])[0]
for precios_entrega in lista_tablas_precios:
  tabla_precios_acumulada = unificar_tablas_precios(tabla_precios_acumulada,precios_entrega)
print(tabla_precios_acumulada)

"""
lista_entregas = ['2 - Entrega 3_6_2023.xlsx',
                  '3 - Entrega 17_6_2023.xlsx',
                  '4 - Entrega 1_7_2023.xlsx',
                  '5 - Entrega 15_7_2023.xlsx',
                  '6 - Entrega 29_7_2023.xlsx',
                  '7 - Entrega 12_8_2023.xlsx',
                  '8 - Entrega 26_8_2023.xlsx',
                  '9 - Entrega 9_9_2023.xlsx']


primer_pedido = pd.read_excel('1 - Entrega 20_5_2023.xlsx')
df_pedidos_acumulados = pac.transformar_df(primer_pedido)
for entrega in lista_entregas:
  df_pedidos_acumulados = incorporar_nueva_lista_pedidos(df_pedidos_acumulados,entrega)
print(df_pedidos_acumulados)



#cuarto_pedido = pd.read_excel('4 - Entrega 1_7_2023.xlsx')
#df_cuarto_pedido = pac.transformar_df(cuarto_pedido)
#print(df_cuarto_pedido.columns.duplicated())
"""