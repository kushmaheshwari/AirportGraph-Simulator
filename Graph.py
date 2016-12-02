import json
#Graph class

#Holds the entire graph data structure(edges and nodes)
class Graph:
    def __init__(self):
        self.nodes = {}

    #@param metros: List of metros jsons from the file (takes a list of json metros)
    #builds nodes and maps city code to city node
    def build_nodes(self, metros):
        for metro in metros:
            self.nodes[metro['code']] = Node(metro)

    def add_node(self, metro):
        self.nodes[metro['code']] = Node(metro)


    #@param routes: List of routes jsons from the file (takes a list of json routes)
    #builds edges for cities
    def build_edges(self, routes):
        for route in routes:
            list_keys = route.keys()
            if len(list_keys) == 2:
                self.add_bidirectional_edge(route)
            elif route['bidirectional']:
                self.add_bidirectional_edge(route)
            else:
                self.add_unidirectional_edge(route)


    #@param route: A single route json from the file (a single json route)
    #Adds edges to both nodes
    def add_bidirectional_edge(self, route):
        #Add edge from airport 1 to airport 2
        node1 = self.nodes.get(route['ports'][0])
        node1.add_edge(route['ports'][1], route['distance'])

        # Add edge from airport 2 to airport 1
        node2 = self.nodes.get(route['ports'][1])
        node2.add_edge(route['ports'][0], route['distance'])

    # @param route: A single route json from the file (a single json route)
    # Adds edge from first to second node
    def add_unidirectional_edge(self, route):
        # Add edge from airport 1 to airport 2
        node1 = self.nodes.get(route['ports'][0])
        node1.add_edge(route['ports'][1], route['distance'])



    # @param route: A single route json from the file (a single json route)
    # Adds edge from first to second node from user input not from file
    def add_edge_userinput(self,route):
        # Add edge from airport 1 to airport 2
        node1 = self.nodes.get(route['ports'][0])
        node1.add_edge(route['ports'][1], route['distance'])

        print('Is this route bidirectional?(Y/N)')
        # Add edge from airport 2 to airport 1
        ans = raw_input()
        if ans == 'Y':
            node2 = self.nodes.get(route['ports'][1])
            node2.add_edge(route['ports'][0], route['distance'])


    # @param route: A single city_code string
    #returns city object based on airport code
    def get_city(self, city_code):
        keys = self.nodes.keys()
        if(city_code in keys):
            return self.nodes[city_code]

    # returns list of city codes
    def get_cities(self):
        return self.nodes.keys()

    # @param route: A single city_code string
    # deletes city from the graph
    def remove_city(self, city_code):
        keys = self.nodes.keys()
        if city_code not in keys:
            return False
        node = self.nodes[city_code]
        edges = node.get_destinations()
        for edge in edges:
            destination = edge.destination
            city = self.nodes[destination]
            city.remove_edge(node)

        del self.nodes[city_code]
        return True

    # @param route: A single route string
    # deletes route from the graph
    def remove_route(self, route):
        if ':' not in route:
            return False
        routeList = route.split(':')

        keys = self.nodes.keys()
        if routeList[0] not in keys or routeList[1] not in keys:
            return False

        cityA = self.nodes[routeList[0]]
        cityB = self.nodes[routeList[1]]
        cityA.remove_edge(cityB)

        print('Do you want to remove the complimentary route?(Y/N)')
        ans = raw_input()
        if ans == 'Y':
            cityB.remove_edge(cityA)

        return True


    #Saves the new graph library as a JSON doc. Basically serialization
    def save_to_disk(self):
        disk = {}

        routes_added = []
        disk["data sources"]= [
		    "http://www.gcmap.com/" ,
		    "http://www.theodora.com/country_digraphs.html" ,
		    "http://www.citypopulation.de/world/Agglomerations.html" ,
		    "http://www.mongabay.com/cities_urban_01.htm" ,
		    "http://en.wikipedia.org/wiki/Urban_agglomeration" ,
		    "http://www.worldtimezone.com/standard.html"
	    ]

        disk['metros'] = []
        disk['routes'] = []

        for key, value in self.nodes.iteritems():
            disk['metros'].append(
                {'code': value.code, 'name': value.name, 'country': value.country, 'continent': value.continent,
                 'timezone': value.timezone, 'coordinates': value.coordinates, 'population': value.population,
                 'region': value.region})

        for key, value in self.nodes.iteritems():
            for edge in value.edges:
                if self.is_bidirectional(key,edge.destination):
                    if [key,edge.destination] not in routes_added and [edge.destination,key] not in routes_added:
                        disk['routes'].append({
                            'ports':[key,edge.destination],
                            'distance':edge.distance,
                            'bidirectional': True
                        })
                        routes_added.append([key,edge.destination])
                else:
                    if [key,edge.destination] not in routes_added and [edge.destination,key] not in routes_added:
                        disk['routes'].append({
                            'ports': [key, edge.destination],
                            'distance': edge.distance,
                            'bidirectional': False
                        })
                        routes_added.append([key, edge.destination])

        with open ('/Users/kushmaheshwari/cs242/Assignment2/map_data_written.json','w') as outfile:
            json.dump(disk,outfile,indent=4,sort_keys=False)

        return

    #@param key: is the first city
    #@param edge: is teh second city
    #returns true if bidirectional else returns false
    def is_bidirectional(self,key,edge):
        node = self.nodes[edge]
        edges = node.edges

        edgeNames = []
        for edge in edges:
            edgeNames.append(edge.destination)
        if key in edgeNames:
            return True
        else:
            return False






#Node/Vertex class that holds airport information
class Node:
    #takes in a metro JSON to construct the Node
    def __init__(self, metro):
        self.code = metro['code']
        self.name = metro['name']
        self.country = metro['country']
        self.continent = metro['continent']
        self.timezone = metro['timezone']
        self.coordinates = metro['coordinates']
        self.population = metro['population']
        self.region = metro['region']
        self.edges = []


    #@param code: A destination code of an airport
    #@param distance: Distance to the code destination
    #add edge to a Node
    def add_edge(self, code, distance):
        self.edges.append(Edge(code,distance))

    #returns all destinations/ edges for a Node
    def get_destinations(self):
        return self.edges


    # @param node: A node of the edge to remove
    def remove_edge(self,node):
        for edge in self.edges:
            if edge.destination == node.code:
                self.edges.remove(edge)
                return


#Edge class which represents a route from one city to another
class Edge:
    #takes in a destination and a distance to construct an edge
    def __init__(self, destination, distance):
        self.destination = destination
        self.distance = distance




