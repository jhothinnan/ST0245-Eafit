import pandas as pd
import pprint

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

pprint.pprint(graph)
pprint.pprint(data)