def claves_diccionario_a_listas(diccionario:dict)->list:
  lista_de_valores_del_diccionario = []
  for clave in diccionario:
    lista_de_valores_del_diccionario.append(diccionario[clave])
  return lista_de_valores_del_diccionario

def agregar_a_diccionario_original(diccionario_original:dict, diccionario_a_chequear:dict) -> dict:
    lista_con_valores_a_chequear = claves_diccionario_a_listas(diccionario_a_chequear)
    lista_con_valores_faltantes = claves_diccionario_a_listas(diccionario_a_chequear).copy()
    lista_de_valores_originales = claves_diccionario_a_listas(diccionario_original)

    for i in range(len(lista_de_valores_originales)):
      for j in range(len(lista_con_valores_a_chequear)):
        if lista_de_valores_originales[i] == lista_con_valores_a_chequear[j]:
          lista_con_valores_faltantes.remove(lista_con_valores_a_chequear[j])

    for i in range(len(lista_con_valores_faltantes)):
        diccionario_original[lista_con_valores_faltantes[i].capitalize()]= lista_con_valores_faltantes[i]

    return diccionario_original
    
# Aca tenemos dos funciones que nos permiten actualizar las instancias del diccionario, 
#pasandole como parametro dos diccionarios: el primero que queremos actualizar y el segundo con el diccionario que tiene terminos a actualizar
# nos filtra los repetidos y aquellos terminos que no estan, son agregados con el valor actual que tienen como key y con valor igual al actual

