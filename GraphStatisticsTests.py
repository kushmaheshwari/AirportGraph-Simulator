import unittest
import json
from Graph import *
from GraphStatistics import *

class GraphStatisticsTests(unittest.TestCase):

    #tests the longest flight function
    def test_get_longest_flight(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        #tests longest flight
        longestFlight = statistics.get_longest_flight(graph)
        self.assertEquals(longestFlight[0],"Mexico City")
        self.assertEquals(longestFlight[1], "LIM")
        self.assertEquals(longestFlight[2], 4231)

    #tests the shortest flight function
    def test_get_shortest_flight(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        # tests shortest flight
        shortestFlight = statistics.get_shortest_flight(graph)
        self.assertEquals(shortestFlight[0],"Bogota")
        self.assertEquals(shortestFlight[1], "LIM")
        self.assertEquals(shortestFlight[2], 1879)

    #tests the average distance function
    def test_get_average_distance(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        # tests average distance
        averageDistance = statistics.get_average_distance(graph)
        self.assertEquals(averageDistance,2854)

    #tests the biggest city function
    def test_get_biggest_city(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        # tests biggest city
        biggestCity = statistics.get_biggest_city(graph)
        self.assertEquals(biggestCity[0],'Mexico City')
        self.assertEquals(biggestCity[1], 23400000)

    #tests the smallest city function
    def test_get_smallest_city(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        # tests smallest city
        smallestCity = statistics.get_smallest_city(graph)
        self.assertEquals(smallestCity[0],'Santiago')
        self.assertEquals(smallestCity[1], 6000000)

    #tests the average size function
    def test_get_average_size(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        # tests average size
        averageSize = statistics.get_average_size(graph)
        self.assertEquals(averageSize, 11762500)

    #tests the getContinents function
    def test_get_continents(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])


        #tests structure of continent dictionary
        continents = statistics.get_continets(graph)
        keys = continents.keys()
        self.assertEquals(keys[0],"North America")
        self.assertEquals(keys[1],"South America")

        citiesNorthAmerica = continents['North America']
        self.assertEquals(citiesNorthAmerica[0],"Mexico City")

        citiesSouthAmerica = continents['South America']
        self.assertEquals(citiesSouthAmerica[0],"Santiago")
        self.assertEquals(citiesSouthAmerica[1], "Bogota")
        self.assertEquals(citiesSouthAmerica[2], "Lima")

    #tests the hubCities function
    def test_get_hub_cities(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        #tests that Lima is the biggest hub city in the tests data
        hubCities = statistics.get_hub_cities(graph)
        self.assertEquals(hubCities[0][0],"Lima")
        self.assertEquals(hubCities[0][1], 3)


    #tests the url function
    def test_generate_URL(self):
        graph = Graph()
        statistics = GraphStatistics()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        #check the url matches what it should be
        url = statistics.generate_url(graph)
        self.assertEquals(url,'http://www.gcmap.com/mapui?P=SCL-LIM,+BOG-LIM,+MEX-LIM,+LIM-SCL,+LIM-MEX,+LIM-BOG')


    #tests getting info about a route
    def test_info_about_route(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        statistics = GraphStatistics()
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        route = {
            "ports": ["MEX", "BOG"],
            "distance": 10
        }

        graph.add_bidirectional_edge(route)

        route = "SCL,LIM,MEX,BOG"
        ans = statistics.get_route(route, graph)

        self.assertEquals(ans[0] == 6694,True)
        self.assertEquals(ans[1] == 2130.35,True) #check this again
        self.assertEquals(int(ans[2]) == 818,True) #check this again

    #tests that shortest path/dijkstras works
    def test_dijkstra_algo(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        statistics = GraphStatistics()
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        route = {
            "ports": ["MEX", "BOG"],
            "distance": 10
        }

        graph.add_bidirectional_edge(route)
        route = "SCL,MEX"
        ans = statistics.get_shortest_path(route, graph)

        self.assertEquals(ans[0] == "SCL", True)
        self.assertEquals(ans[1] == "LIM", True)
        self.assertEquals(ans[2] == "BOG", True)
        self.assertEquals(ans[3] == "MEX", True)



if __name__ == '__main__':
    unittest.main()