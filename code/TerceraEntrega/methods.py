from heapq import *
import pandas as pd
import gmplot

def createGraphComplete(data): 
    unique_origins = data.origin.unique()
    graph = {}
    for i in unique_origins:
        graph[i] = []
    for i in data.index:
        if data["oneway"][i]:
            graph[data["origin"][i]].append((data["harassmentRisk"][i],data["length"][i],data["destination"][i]))
            try:
                graph[data["destination"][i]].append((data["harassmentRisk"][i],data["length"][i],data["origin"][i]))
            except KeyError:
                destination = data["destination"][i]
                graph[destination] = [(data["harassmentRisk"][i],data["length"][i],data["origin"][i])]
        else:
            graph[data["origin"][i]].append((data["harassmentRisk"][i],data["length"][i],data["destination"][i]))
    return graph

def dijkstraLength(start, goal, graph):
    queue = []
    heappush(queue, (0,0,start))
    cost_visited = {start: 0}
    cost_length = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_length, cur_node = heappop(queue) 
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_len, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost
            new_len = cost_length[cur_node] + neigh_len

            if neigh_node not in cost_length or new_len < cost_length[neigh_node]:
                heappush(queue, (cur_cost, new_len, neigh_node))
                cost_visited[neigh_node] = new_cost
                cost_length[neigh_node] = new_len
                visited[neigh_node] = cur_node
                
    return visited, cost_visited[goal], cost_length[goal]

def dijkstraHarrasment(start, goal, graph):
    queue = []
    heappush(queue, (0,0,start))
    cost_visited = {start: 0}
    cost_length = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_length, cur_node = heappop(queue) 
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_len, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost
            new_len = cost_length[cur_node] + neigh_len

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                heappush(queue, (new_cost, new_len, neigh_node))
                cost_visited[neigh_node] = new_cost
                cost_length[neigh_node] = new_len
                visited[neigh_node] = cur_node
                
    return visited, cost_visited[goal], cost_length[goal]

def dijkstra3(start, goal, graph):
    queue = []
    heappush(queue, (0,0,0,start))
    cost_visited = {start: 0}
    cost_length = {start: 0}
    cost_mix = {start: 0}
    visited = {start: None}

    while queue:
        cur_mix, cur_cost, cur_length, cur_node = heappop(queue) 
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_len, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost
            new_len = cost_length[cur_node] + neigh_len
            new_mix = new_len*new_cost
            #new_mix = 50*(cost_length[cur_node] + neigh_len)*(100*(cost_visited[cur_node] + neigh_cost))
            #new_mix = ((cost_length[cur_node] + neigh_len)*30)+((cost_visited[cur_node] + neigh_cost)*500)

            if neigh_node not in cost_mix or new_mix < cost_mix[neigh_node]:
                heappush(queue, (new_mix, cur_cost, cur_length, neigh_node))
                cost_visited[neigh_node] = new_cost
                cost_length[neigh_node] = new_len
                cost_mix[neigh_node] = new_mix
                visited[neigh_node] = cur_node
                
    return visited, cost_visited[goal], cost_length[goal]












def createDataFrame(archivo):
    data = pd.read_csv(archivo, sep = ';')
    average = data['harassmentRisk'].mean()
    data['harassmentRisk'] = data['harassmentRisk'].fillna(average)
    return data

def convertList(start, goal, visited):
    path = list()
    cur_node = goal
    while cur_node != start:
        cur_node = visited[cur_node]
        path.append(cur_node)
    return path

def graficar(coordinaes_list, coordinates_harrasment, coordinates_length):
    latitude_1, latitude_2, latitude_3 = list(), list(), list()
    longitude_1, longitude_2, longitude_3 = list(), list(), list()

    for i in range (0, len(coordinaes_list)):
        temp = str(coordinaes_list[i])
        longitude_1.append(float(temp[1:temp.find(',')]))
        latitude_1.append(float(temp[temp.find(',')+2:len(temp)-1]))

    map = gmplot.GoogleMapPlotter(latitude_1[0],longitude_1[0],15)
    map.scatter(latitude_1,longitude_1,"blue",size = 1, marker=False)
    map.plot(latitude_1,longitude_1,'blue',edge_width = 10)

    for i in range (0, len(coordinates_harrasment)):
        temp = str(coordinates_harrasment[i])
        longitude_2.append(float(temp[1:temp.find(',')]))
        latitude_2.append(float(temp[temp.find(',')+2:len(temp)-1]))

    map.scatter(latitude_2,longitude_2,"white",size = 1, marker=False)
    map.plot(latitude_2,longitude_2,'white',edge_width = 7)

    for i in range (0, len(coordinates_length)):
        temp = str(coordinates_length[i])
        longitude_3.append(float(temp[1:temp.find(',')]))
        latitude_3.append(float(temp[temp.find(',')+2:len(temp)-1]))

    map.scatter(latitude_3,longitude_3,"yellow",size = 1, marker=False)
    map.plot(latitude_3,longitude_3,'yellow',edge_width = 7)

    map.draw('map.html')


'''def graficar(coordinates_harrasment, coordinates_length):
    latitude_2, latitude_3 = list(), list()
    longitude_2, longitude_3 = list(), list()
    

    for i in range (0, len(coordinates_harrasment)):
        temp = str(coordinates_harrasment[i])
        longitude_2.append(float(temp[1:temp.find(',')]))
        latitude_2.append(float(temp[temp.find(',')+2:len(temp)-1]))

    map = gmplot.GoogleMapPlotter(latitude_2[0],longitude_2[0],15)
    map.scatter(latitude_2,longitude_2,"white",size = 1, marker=False)
    map.plot(latitude_2,longitude_2,'white',edge_width = 3)

    for i in range (0, len(coordinates_length)):
        temp = str(coordinates_length[i])
        longitude_3.append(float(temp[1:temp.find(',')]))
        latitude_3.append(float(temp[temp.find(',')+2:len(temp)-1]))

    map.scatter(latitude_3,longitude_3,"yellow",size = 1, marker=False)
    map.plot(latitude_3,longitude_3,'yellow',edge_width = 3)

    map.draw('map.html')'''