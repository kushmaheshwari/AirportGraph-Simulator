import sys
import math
from Queue import PriorityQueue


#this class provides all statistics that require calculation for a certain graph



class GraphStatistics:
    def __init__(self):
        return

    #@param graph: the graph from which should be analyzed
    #@return: returns the longest flight in the network
    def get_longest_flight(self, graph):
        longestFlight = -1
        for key in graph.nodes:#O(n) solution that checks all flights and returns the longest one
            city = graph.nodes[key]
            edges = city.get_destinations()
            for edge in edges:
                if edge.distance > longestFlight:
                    longestFlight = edge.distance
                    startCity = city.name
                    endCity = edge.destination

        return startCity, endCity, longestFlight


    # @param graph: the graph from which should be analyzed
    # @return: returns the shortest flight in the network
    def get_shortest_flight(self, graph):
        shortestFlight = sys.maxint
        for key in graph.nodes:#O(n) solution that checks all flights and returns the shortest one
            city = graph.nodes[key]
            edges = city.get_destinations()
            for edge in edges:
                if edge.distance < shortestFlight:
                    shortestFlight = edge.distance
                    startCity = city.name
                    endCity = edge.destination

        return startCity, endCity, shortestFlight

    # @param graph: the graph from which should be analyzed
    # @return: returns the average distance of all flights
    def get_average_distance(self, graph):
        sumDistances = 0;
        numDistances = 0;
        for key in graph.nodes:#O(n) solution that adds all distances and divides by the count
            city = graph.nodes[key]
            edges = city.get_destinations()
            for edge in edges:
                sumDistances += edge.distance
                numDistances += 1

        average = sumDistances/numDistances
        return average

    # @param graph: the graph from which should be analyzed
    # @return: returns the biggest city by population
    def get_biggest_city(self, graph):
        biggestCity = -1
        for key in graph.nodes: #O(n) solution that checks all cities and returns the biggest one
            city = graph.nodes[key]
            if city.population > biggestCity:
                biggestCity = city.population
                cityName = city.name

        return cityName, biggestCity

    # @param graph: the graph from which should be analyzed
    # @return: returns the smallest city by population
    def get_smallest_city(self, graph):
        smallestCity = sys.maxint
        for key in graph.nodes:#O(n) solution that checks all cities and returns the smallest one
            city = graph.nodes[key]
            if city.population < smallestCity:
                smallestCity = city.population
                cityName = city.name

        return cityName,smallestCity

    # @param graph: the graph from which should be analyzed
    # @return: returns the average population of all cities
    def get_average_size(self, graph):
        sumSizes = 0;
        numCities = 0;
        for key in graph.nodes:#O(n) solution that checks all cities and returns the average population of them
            city = graph.nodes[key]
            sumSizes += city.population
            numCities += 1

        average = sumSizes / numCities
        return average

    # @param graph: the graph from which should be analyzed
    # @return: returns a dictionary of continents to their respective cities in the graph
    def get_continets(self, graph):
        continents = {}
        for key in graph.nodes: # adds city to existing continent else it makes a new continent for which to add a city too
            city = graph.nodes[key]
            continent = city.continent
            if continents.has_key(continent) is False:
                continents[continent] = [city.name]
            else:
                countryList = continents.get(continent)
                countryList.append(city.name)

        return continents

    # @param graph: the graph from which should be analyzed
    # @return: returns a sorted list of cities and their respective edges. Sorts by edges. View class determines how many to show
    def get_hub_cities(self, graph):
        cities = []
        for key in graph.nodes:
            city = graph.nodes[key]
            edges = len(city.edges)
            cities.append((city.name,edges))
        sortedCities = sorted(cities,key=lambda tup: tup[1])#sorts by the second part of a tuuple
        sortedCities.reverse()
        return sortedCities


    # @param graph: the graph from which should be analyzed
    # @return: returns a url to be opened in the web browser
    def generate_url(self, graph):
        mapString = ''
        for key in graph.nodes:
            city = graph.nodes[key]
            edges = city.edges
            for edge in edges:
                if (len(mapString) == 0):#makes url based on edges of cities
                    mapString += city.code + '-' + edge.destination
                else:
                    mapString += ',+' + city.code + '-' + edge.destination

        return 'http://www.gcmap.com/mapui?P=' + mapString #adds proper url to beggining of string


    # @param graph: the graph from which should be analyzed
    # @param route: the route which is checked
    # @return: returns distance,cost, and time if the route exists;returns false if route doesnt exist
    def get_route(self,route,graph):
        keys = graph.nodes.keys()

        routes = route.split(',')
        flag = False
        for i in range(len(routes) - 1):
            if i != 0 and flag == False:
                return False
            routeA = routes[i]
            if routeA not in keys:
                return False
            node = graph.nodes[routeA]
            edges = node.edges
            flag = False
            for edge in edges:
                if routes[i+1] == edge.destination:
                    flag = True
                    break
        dist = self.calculate_dist(routes,graph)
        cost = self.calculate_cost(routes,graph)
        time = self.calculate_time(routes,graph)
        return dist,cost,time


    # @param graph: the graph from which should be analyzed
    # @param routes: the route which is checked for distance
    # @return: returns distance of route
    def calculate_dist(self,routes,graph):
        dist = 0
        for i in range(len(routes)-1):
            routeA = routes[i]
            node = graph.nodes[routeA]
            edges = node.edges
            for edge in edges:
                if routes[i+1] == edge.destination:
                    dist += edge.distance
                    break

        return dist


    # @param graph: the graph from which should be analyzed
    # @param costs: the route which is checked for cost
    # @return: returns cost of route
    def calculate_cost(self,routes,graph):
        cost = 0
        multiplier = .35

        for i in range(len(routes)-1):
            routeA = routes[i]
            node = graph.nodes[routeA]
            edges = node.edges
            for edge in edges:
                if routes[i+1] == edge.destination:
                    cost += (multiplier * edge.distance)
                    if multiplier != 0:
                        multiplier -= .05
                    break
        return cost

    # @param graph: the graph from which should be analyzed
    # @param route: the route which is checked for time
    # @return: returns time of the route
    def calculate_time(self,routes,graph):
        time = 0
        acceleration = (750.0 * 750.0) / 400.0
        for i in range(len(routes)-1):
            routeA = routes[i]
            node = graph.nodes[routeA]
            edges = node.edges
            for edge in edges:
                if routes[i+1] == edge.destination:
                    if edge.distance < 400:
                        dist = edge.distance/2.0
                        t = math.sqrt((2.0*dist)/acceleration) * 60.0
                        time += (2.0*t)
                    else:
                        mid_distance = edge.distance - 400.0
                        mid_time = mid_distance/750.0

                        time += (mid_time * 60.0)

                        start_end_time = math.sqrt((2.0*200.0)/acceleration) * 60.0
                        time += (2.0*start_end_time)
                    break
            if i != len(routes)-2:
                city = graph.nodes[routes[i+1]]
                time += (120 - ((len(city.edges) -1) * 10))

        return time



    # @param graph: the graph from which should be analyzed
    # @param source: the source from which to start dijkstras
    # @return: returns distances and predecessors which are dijstra algorithm arrays of the route
    def run_dijkstra(self,source,graph):
        distances = {}
        predecessors = {}
        queue = []

        nodes = graph.nodes

        for node in nodes:
            c = nodes[node]
            if c.code == source:
                distances[c.code] = 0
            else:
                distances[c.code] = sys.maxint
            predecessors[c.code] = None

            queue.append(c)#dist to city from source,city

        while len(queue) != 0:
            min = sys.maxint
            pop = None
            for cityA in queue:
                if distances[cityA.code] < min:
                    min = distances[cityA.code]
                    pop = cityA
            queue.remove(pop)
            edges = pop.edges
            for edge in edges:
                city = nodes[edge.destination]
                num = distances[pop.code] + edge.distance
                if num < distances[edge.destination]:
                    distances[city.code] = num
                    predecessors[city.code] = pop.code

        return distances,predecessors


    # @param graph: the graph from which should be analyzed
    # @param route: the route from which should be checked by dijkstras
    # @return: returns path of the shortest route
    def get_shortest_path(self,route,graph):
        routes = route.split(',')
        dijkstra = self.run_dijkstra(routes[0],graph)
        predecessors = dijkstra[1]

        target = routes[1]

        path = []
        while True:
            path.append(target)
            if target == routes[0]:
                break
            target = predecessors[target]
            if target == None:
                return False
        path.reverse()

        return path



























