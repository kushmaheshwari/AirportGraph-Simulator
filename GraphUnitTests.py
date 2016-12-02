import unittest
from Graph import *


#tests the edge class and its variables
class TestEdgeClass(unittest.TestCase):
    def test_edge_destination(self):
        edge = Edge('SYD',1000)
        self.assertEqual(edge.destination, 'SYD')

    def test_edge_distance(self):
        edge = Edge('SYD', 1000)
        self.assertEqual(edge.distance,1000)


#tests the node class and its constructor
class TestNodeClass(unittest.TestCase):

    def test_node_info(self):

        metro = {}
        metro['code'] = "MIL"
        metro['name'] = "Milan"
        metro['country'] = "IT"
        metro['continent'] = "Europe"
        metro['timezone'] = 1
        metro['coordinates'] = {"N" : 45, "E" : 9}
        metro['population'] = 3575000
        metro['region'] = 3


        edge1 = Edge('SYD', 1000)
        edge2 = Edge('LED', 2000)
        edge3 = Edge('MOW',500)


        node = Node(metro)
        node.add_edge(edge1.destination, edge1.distance)
        node.add_edge(edge2.destination, edge2.distance)
        node.add_edge(edge3.destination, edge3.distance)


        #check constructor
        self.assertEqual(node.code, 'MIL')
        self.assertEqual(node.name, 'Milan')
        self.assertEqual(node.country, 'IT')
        self.assertEqual(node.continent, 'Europe')
        self.assertEqual(node.timezone, 1)
        self.assertEqual(node.coordinates, {"N" : 45, "E" : 9})
        self.assertEquals(node.population,3575000)
        self.assertEquals(node.region,3)

        #check that all edges have been added properly
        nodeEdges = node.get_destinations()
        self.assertEquals(nodeEdges[0].destination, edge1.destination)
        self.assertEquals(nodeEdges[1].destination, edge2.destination)
        self.assertEquals(nodeEdges[2].destination, edge3.destination)

        self.assertEquals(nodeEdges[0].distance, edge1.distance)
        self.assertEquals(nodeEdges[1].distance, edge2.distance)
        self.assertEquals(nodeEdges[2].distance, edge3.distance)


#tests the Graph data structure class and building the graph
class TestGraphClass(unittest.TestCase):

    def test_graph(self):
        graph = Graph()

        metro = {}
        metro['code'] = "MIL"
        metro['name'] = "San Francisco"
        metro['country'] = "US"
        metro['continent'] = "North America"
        metro['timezone'] = 1
        metro['coordinates'] = {"N": 45, "E": 9}
        metro['population'] = 3575000
        metro['region'] = 3

        metro1 = {}
        metro1['code'] = "SFO"
        metro1['name'] = "San Fran"
        metro1['country'] = "IT"
        metro1['continent'] = "Europe"
        metro1['timezone'] = -6
        metro1['coordinates'] = {"N" : 42, "W" : 88}
        metro1['population'] = 9850000
        metro1['region'] = 3

        metros = [metro,metro1]

        graph.build_nodes(metros)

    #check that routes/edges have been added
        route = {}
        route['ports'] = ["MIL", "SFO"]
        route['distance'] = 407
        graph.add_bidirectional_edge(route)

        mil = graph.get_city("MIL")
        sfo = graph.get_city("SFO")

        milDests = mil.get_destinations()
        sfoDests = sfo.get_destinations()

        #check for proper graph edges
        self.assertEquals(milDests[0].destination,"SFO")
        self.assertEquals(sfoDests[0].destination,"MIL")

    #tests removing a city
    def test_remove_city(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        graph.remove_city('BOG')
        keys = graph.get_cities()
        self.assertEquals('BOG' in keys,False)



    #tests removing a route
    def test_remove_bidirectional_route(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        cityA = graph.nodes['SCL']
        cityB = graph.nodes['LIM']
        cityA.remove_edge(cityB)
        cityB.remove_edge(cityA)

        scl_node = graph.nodes['SCL']
        lim_node = graph.nodes['LIM']
        edges = scl_node.get_destinations()
        edges_lim = lim_node.get_destinations()
        self.assertEquals('LIM' in edges,False)
        self.assertEquals('SCL' in edges, False)

        #check bidirectional removal vs unidirectional removal; look at commented code in graph.py

    # tests removing a route
    def test_remove_unidirectional_route(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])


        cityA = graph.nodes['LIM']
        cityB = graph.nodes['SCL']
        cityA.remove_edge(cityB)

        scl_node = graph.nodes['SCL']
        edges = scl_node.get_destinations()
        edgeNames = []
        for e in edges:
            edgeNames.append(e.destination)
        self.assertEquals('LIM' in edgeNames, True)

        # check bidirectional removal vs unidirectional removal; look at commented code in graph.py


    #tests adding a city
    def test_add_city(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        metro = {}
        metro["code"] = "SAR"
        metro["name"] = "Saratoga"
        metro["country"] = "US"
        metro["continent"] = "North America"
        metro["timezone"] = "-8"
        metro["coordinates"] = "{\"N\" : 34, \"W\" : 118}"
        metro["population"] = "10000"
        metro["region"] = "1"
        graph.add_node(metro)

        keys = graph.get_cities()
        self.assertEquals('SAR' in keys, True)


    #tests adding a route
    def test_add_route(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        route = {
            "ports": ["MEX", "BOG"],
            "distance": 2100
        }

        graph.add_bidirectional_edge(route)

        mex_node = graph.nodes['MEX']
        edges = mex_node.get_destinations()
        var = False
        for edge in edges:
            if edge.destination == 'BOG':
                var = True
        self.assertEquals(var, True)

    #tests editing a city
    def test_edit_city(self):
        graph = Graph()
        file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        f = open(file, 'r')
        jsonData = json.loads(f.read())
        graph.build_nodes(jsonData['metros'])
        graph.build_edges(jsonData['routes'])

        value = 4
        node = graph.nodes["BOG"]
        node.region = value
        graph.nodes["BOG"] = node

        self.assertEquals(graph.nodes["BOG"].region == 4, True)


if __name__ == '__main__':
    unittest.main()

