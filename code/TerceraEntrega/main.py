from methods import *

TelefericoPalmaitas = '(-75.7161351, 6.3424055)'
Eafit = "(-75.5778046, 6.2029412)"
U_Medellin = "(-75.6101004, 6.2312125)"
U_Antioquia = "(-75.5694416, 6.2650137)"
U_Nacional = "(-75.5762232, 6.266327)"
LuisAmigo = "(-75.5832559, 6.2601878)"  

data = createDataFrame('calles_de_medellin_con_acoso.csv')
graph = createGraphComplete(data)

pathShortest, riskShortest, lengthShortest = dijkstraLength(U_Nacional,Eafit,graph)
listShortest = convertList(U_Nacional,Eafit,pathShortest)
lengthShortest = lengthShortest/1000
riskShortest = riskShortest/len(listShortest)
print(f'La ruta mas corta tiene una distancia de: {lengthShortest} y el riesgo medio es de: {riskShortest}')

pathSafest, riskSafest, lengthSafest = dijkstraHarrasment(U_Nacional,Eafit,graph)
listSafest = convertList(U_Nacional,Eafit,pathSafest)
lengthSafest = lengthSafest/1000
riskSafest = riskSafest/len(listSafest)
print(f'La ruta mas segura tiene una distancia de: {lengthSafest} y el riesgo medio es de: {riskSafest}')

graficar(listSafest,listShortest)