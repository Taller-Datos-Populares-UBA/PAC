import PAC_utils
import pandas as pd
import numpy as np

df_sin_transformar = pd.read_excel('1 - Entrega 20_5_2023.xlsx')
df_sin_transformar2 = pd.read_excel('2 - Entrega 3_6_2023.xlsx')
df_sin_transformar3 = pd.read_excel('3 - Entrega 17_6_2023.xlsx')

#nuevo_df = PAC_utils.transformar_df(df_sin_transformar,64)
lista = [df_sin_transformar, df_sin_transformar2, df_sin_transformar3]

for i in range(len(lista)):
    lista[i] = PAC_utils.transformar_df(lista[i],20)

for i in range(len(lista)):
    #df_mergeado = Empty DataFrame
    df_mergeado = pd.merge(df_mergeado, lista[i])
    
df_mergeado
    



    
    