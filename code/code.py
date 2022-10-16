import pandas as pd
import sys
import time

# ---------------------------------------------------------------------------------------------------#
# Dataframe
data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';')
# ---------------------------------------------------------------------------------------------------#
# Change all the empty cells in the harassment risk column with the average of the harassment risk column
average = data['harassmentRisk'].mean()
data['harassmentRisk'] = data['harassmentRisk'].fillna(average)
# ---------------------------------------------------------------------------------------------------#
# Locate al the unique origins
unique = data["origin"].unique()
# ---------------------------------------------------------------------------------------------------#
# Create the graph
graph = {}
# fill the graph with the keys as the unique origins
for i in unique:
    graph[i] = {}
# ---------------------------------------------------------------------------------------------------#
# fill the values of the graph
for i in data.index:
    graph[data["origin"][i]][data["destination"][i]] = (data["length"][i])
    # graph[data["origin"][i]][data["destination"][i]] = (data["harassmentRisk"][i])
    # graph[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])
    # ---------------------------------------------------------------------------------------------------#
    # If the value at oneway is true means that the destinations is also an origin, so create that origin in the graph
    if data['oneway'][i] == True:
        graph[data['destination'][i]] = {data["origin"][i]: (data["length"][i])}
        # graph[data['destination'][i]] = {data["origin"][i]: (data["harassmentRisk"][i])}
        # graph[data['destination'][i]] = {data["origin"][i]: (data["length"][i], data["harassmentRisk"][i])}


# ---------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------#
# Dijkstra approach implementation
def dijkstra(graph, start, goal):
    shortest_distance = {}  # Almacena el costo de alcanzar el nodo. Se va cambiando mientras nos movemos en el grafo
    track_predecesor = {}  # Conserva el camino que nos ha llevado hasta ese nodo
    unseenNodes = graph  # Para iterar a traves del grafo
    infinity = sys.maxsize  # Un numero muy grande
    track_path = []  # Almacena el camino optimo

    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseenNodes:
        min_distance_node = None

        for node in unseenNodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node
        path_options = graph[min_distance_node].items()
        for child_node, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecesor[child_node] = min_distance_node

        unseenNodes.pop(min_distance_node)

    currentNode = goal
    while currentNode is not start:
        try:
            track_path.insert(0, currentNode)
            currentNode = track_predecesor[currentNode]
        except KeyError:
            break
    track_path.insert(0, start)

    if shortest_distance[goal] != infinity:
        print('Shortest distance is', str(shortest_distance[goal]))
        print('optimal path:', str(track_path))


# ---------------------------------------------------------------------------------------------------#
# Execution and time register
inicio = time.time()
dijkstra(graph, '(-75.5937506, 6.2433334)', '(-75.6067194, 6.2053265)')
fin = time.time()
# ---------------------------------------------------------------------------------------------------#
# tests
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
print(fin - inicio)
