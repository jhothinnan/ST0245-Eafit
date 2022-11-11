from methods import *
import time

TelefericoPalmaitas = '(-75.7161351, 6.3424055)'
Eafit = "(-75.5778046, 6.2029412)"
U_Medellin = "(-75.6101004, 6.2312125)"
U_Antioquia = "(-75.5694416, 6.2650137)"
U_Nacional = "(-75.5762232, 6.266327)"
LuisAmigo = "(-75.5832559, 6.2601878)"  

data = createDataFrame('calles_de_medellin_con_acoso.csv')
inicio = time.time()
graph = createGraphComplete(data)
fin = time.time()
print(f'El tiempo necesario para crear el grafo fue de: {fin-inicio}')

inicio = time.time()
pathShortest, riskShortest, lengthShortest = dijkstraLength(U_Nacional,Eafit,graph)
fin = time.time()
listShortest = convertList(U_Nacional,Eafit,pathShortest)
lengthShortest = lengthShortest
riskShortest = riskShortest/len(listShortest)
print(f'La ruta mas corta tiene una distancia de: {lengthShortest} y el riesgo medio es de: {riskShortest}')
print(f'El tiempo de ejecucion del algorimo fue: {fin-inicio}')

inicio = time.time()
pathSafest, riskSafest, lengthSafest = dijkstraHarrasment(U_Nacional,Eafit,graph)
fin = time.time()
listSafest = convertList(U_Nacional,Eafit,pathSafest)
lengthSafest = lengthSafest
riskSafest = riskSafest/len(listSafest)
print(f'La ruta mas segura tiene una distancia de: {lengthSafest} y el riesgo medio es de: {riskSafest}')
print(f'El tiempo de ejecucion del algorimo fue: {fin-inicio}')

inicio = time.time()
path, risk, length = dijkstraMixed(U_Nacional,Eafit,graph)
fin = time.time()
lista = convertList(U_Nacional,Eafit,path)
length = length
risk = risk/len(lista)
print(f'La ruta promediada tiene una distancia de: {length} y el riesgo medio es de: {risk}')
print(f'El tiempo de ejecucion del algorimo fue: {fin-inicio}')

graficar(lista,listSafest,listShortest)