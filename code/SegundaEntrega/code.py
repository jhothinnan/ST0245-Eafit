import pandas as pd
import sys
import time
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt
import gmplot

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
    # ---------------------------------------------------------------------------------------------------#
    #Distance and risk weighting
    # ---------------------------------------------------------------------------------------------------#
    graph[data["origin"][i]][data["destination"][i]] = (((data["length"][i]*100)*(0.25*data["harassmentRisk"][i]))/10)
    # ---------------------------------------------------------------------------------------------------#

    # If the value at oneway is true means that the destinations is also an origin, so create that origin in the graph
    if data['oneway'][i] == True:
        # ---------------------------------------------------------------------------------------------------#
        #Distance and risk weighting
        # ---------------------------------------------------------------------------------------------------#
        graph[data['destination'][i]] = {data["origin"][i]: (((data["length"][i]*100)*(0.25*data["harassmentRisk"][i]))/10)}

# ---------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------#
# Dijkstra approach implementation
def dijkstra(graph, start, goal):
    shortest_distance = {}                                  # Stores the cost of reaching the node. It changes as we move in the graph
    track_predecesor = {}                                   # Preserve the path that has taken us to that node
    unseenNodes = graph                                     # To iterate through the graph
    infinity = sys.maxsize                                  # A very large number
    track_path = []                                         # Store the optimal path

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
        return track_path


# ---------------------------------------------------------------------------------------------------#
# Execution and time register
inicio = time.time()
ruta = (dijkstra(graph, '(-75.7161351, 6.3424055)', '(-75.7025278, 6.3425976)'))
fin = time.time()
# ---------------------------------------------------------------------------------------------------#


#Make the route in the map

area = pd.read_csv('poligono_de_medellin.csv',sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

#Load streets
edges = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
edges['harassmentRisk'] = edges['harassmentRisk'].fillna(edges['harassmentRisk'].mean())
edges.loc[edges.harassmentRisk<50,'harassmentRisk']=0
for i in range(len(ruta)-2):
    edges.loc[(edges['origin'] == ruta[i]) & (edges['destination'] == ruta[i+1]),'harassmentRisk']=100
edges = edges.loc[edges['harassmentRisk']>0]
edges['geometry'] = edges['geometry'].apply(wkt.loads)
edges = gpd.GeoDataFrame(edges)

#Create plot
fig, ax = plt.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor='black')

# Plot street edges
edges.plot(ax=ax, linewidth=1, column='harassmentRisk', color='white')

plt.title("Riesgo de acoso en las calles de Medellín")
plt.tight_layout()
plt.savefig("mapa-de-la-ruta.png")

#Another way to create the path

latitud = []
longitud = []

for i in range (0, len(ruta)):
    temp = str(ruta[i])
    longitud.append(float(temp[1:temp.find(',')]))
    latitud.append(float(temp[temp.find(',')+2:len(temp)-1]))

map = gmplot.GoogleMapPlotter(latitud[0],longitud[0],15)
map.scatter(latitud,longitud,"# FF0000",size = 1, marker=False)
map.plot(latitud,longitud,'white',edge_width = 3)
map.draw('map.html')


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