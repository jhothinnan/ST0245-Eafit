import pandas as pd
import pprint

#data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')

#promedio = data['harassmentRisk'].mean()
#data['harassmentRisk'] = data['harassmentRisk'].fillna(promedio)

#unicas = data["origin"].unique()

#grafo = {}
#for i in unicas:
#    grafo[i] = {}

#for i in data.index:
#    grafo[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])
#    if data['oneway'][i] == True:
#        grafo[data['destination'][i]] = {data["origin"][i]: (data["length"][i], data["harassmentRisk"][i])}

data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')

average = data['harassmentRisk'].mean()
data['harassmentRisk'] = data['harassmentRisk'].fillna(average)

unique = data["origin"].unique()
graph = {}
for i in unique:
    graph[i] = {}

for i in data.index:
    graph[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])
    if data['oneway'][i] == True:
        graph[data['destination'][i]] = {data["origin"][i]: (data["length"][i], data["harassmentRisk"][i])}




# and data["destination"][i] not in grafo
# print(graph)
# print(len(graph))
# pprint.pprint(graph)
# print(data['origin'])
# print(unicas)
# print(data.columns.values)
# print(data['harassmentRisk'])
# print(data.loc[[1]])
# print(data[['harassmentRisk']].to_string(index=False))
# print(len(data["origin"].unique()))
