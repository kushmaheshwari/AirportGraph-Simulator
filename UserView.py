import webbrowser
import json


class UserView:

    def __init__(self):
        return

    #prints the options a user can choose from
    def print_options(self):
        print("\n\n"
              "[0] exit\n"
              "[1] City list\n"
              "[2] City Information\n"
              "[3] Longest Flight\n"
              "[4] Shortest flight\n"
              "[5] Average Flight Distance \n"
              "[6] Biggest Population\n"
              "[7] Smallest Population\n"
              "[8] Average Population\n"
              "[9] Continents and Cities\n"
              "[10] Top 3 Hub Cities\n"
              "[11] Map URl\n"
              "[12] Remove a City\n"
              "[13] Remove a Route\n"
              "[14] Add a City\n"
              "[15] Add a Route\n"
              "[16] Edit a City\n"
              "[17] Info about a Route\n"
              "[18] Shortest Path\n"
              "[19] Save to Disk\n")

    #the prompt
    def ask_questions(self):
        print("Pick a number:")

    #prints cities and their codes
    def print_cities(self, graph):
        for key in graph.nodes:
            city = graph.nodes[key]
            print("Name: " + str(city.name) + " Code: " + str(city.code))


    #prints all the info for a certain city based on a city
    def print_city(self, city_code, graph):
        cityNode = graph.get_city(city_code)

        if(cityNode is None):
            print("Invalid City Code")
            return
        else:
            print('Code: ' + cityNode.code)
            print('Name: ' + cityNode.name)
            print('Country: ' + cityNode.country)
            print('Continent: ' + cityNode.continent)
            print('Timezone: ' + str(cityNode.timezone))
            print('Coordinates: ' + str(cityNode.coordinates))
            print('Population: ' + str(cityNode.population))
            print('Region: ' + str(cityNode.region))

            destinations = cityNode.get_destinations()
            for dest in destinations:
                print("City: " + str(dest.destination) + " Distance: " + str(dest.distance))


    #@param longestFlight: the longest flight
    #prints the longest flight, its start city, and end city
    def print_longest_flight(self, longest_flight):

        print("The longest flight in CSAir goes from " + str(longest_flight[0]) + " to " + str(longest_flight[1]) + " and the distance is " + str(longest_flight[2]))

    # @param shortestFlight: the longest flight
    # prints the shortest flight, its start city, and end city
    def print_shortest_flight(self, shortest_flight):

        print("The shortest flight in CSAir goes from " + str(shortest_flight[0]) + " to " + str(shortest_flight[1]) + " and the distance is " + str(shortest_flight[2]))

    # @param averageDistance: the average distance of the graph
    # prints the average distance
    def print_average_distance(self, average_distance):

        print("The average distance in CSAir flight is " + str(average_distance))

    # @param longestFlight: the biggest city
    # prints the biggest city and its popualtion
    def print_biggest_city(self, biggest_city):

        print("The biggest city in CSAir is " + str(biggest_city[0]) + " and its population is " + str(biggest_city[1]))

    # @param smallestCity: the smallest city
    # prints the smallest city and its population
    def print_smallest_city(self, smallest_city):
        print("The smallest city in CSAir is " + smallest_city[0] + " and its population is " + str(smallest_city[1]))


    # @param averageSize: the average size
    # prints the average size of popualtion
    def print_average_size(self, average_size):
        print("The average size of CSAir cities is " + str(average_size))

    # @param continents: the continents with their respective cities
    # prints the continents and their cities city and its popualtion
    def print_continents(self, continents):
        for key in continents:
            cityList = continents[key]
            print(key + ":")
            for city in cityList:
                print("\t" + city)


    # @param hubCities: a sorted list by how many flights go through certain cities
    # prints the top 3 hub cities and the number of flights that go through
    def print_hub_cities(self, hub_cities):
        print("HubCity1: " + str(hub_cities[0][0]) + " Num Destinations: " + str(hub_cities[0][1]))
        print("HubCity2: " + str(hub_cities[1][0]) + " Num Destinations: " + str(hub_cities[1][1]))
        print("HubCity3: " + str(hub_cities[2][0]) + " Num Destinations: " + str(hub_cities[2][1]))


    # @param url: a URL for which to open on the webbrowser
    # launches url on a web browser
    def launch_URL(self, url):
        webbrowser.open(url, new=1)


    # adding a city to the graph
    # returns JSON of a city that can be passed into Graph library
    def add_city(self):
        citydata = {}
        print("City code(ABC): ")
        citydata['code'] = raw_input()

        print("City name: ")
        citydata['name'] = raw_input()

        print("Country that city is in: ")
        citydata['country'] = raw_input()

        print("Continent that city is in: ")
        citydata['continent'] = raw_input()

        print("Timezone that city is in: ")
        citydata['timezone'] = raw_input()

        print("Coordinates: ")
        citydata['coordinates'] = raw_input()

        print("Population: ")
        citydata['population'] = raw_input()

        print("Region: ")
        citydata['region'] = raw_input()

        return json.dumps(citydata)


    #adding a route to the graph
    #returns JSON of a route that can be passed into Graph library
    def add_route(self):
        print("Port A: ")
        portA = raw_input()
        print("Port B: ")
        portB = raw_input()
        print("Distance: ")
        distance = raw_input()

        new_route = {
            'ports': [portA, portB],
            'distance': distance
        }

        return json.dump(new_route)

    # editing a city
    # @param graph: graph to be examined
    # returns JSON of a route that can be passed into Graph library
    def edit_city(self,graph):
        print("Which City do you want to edit: ")
        city = raw_input()
        print("Which part of the City do you want to edit: (code,name,country,continent,timezone,coordinates,population,region")
        part = raw_input()
        print("What is the new value?")
        value = raw_input()
        node = graph.nodes[city]

        if part == "code":
            node.code = value
        elif part == "name":
            node.name = value
        elif part == "country":
            node.country = value
        elif part == "continent":
            node.continent = value
        elif part == "timezone":
            node.timezone = value
        elif part == "coordinates":
            node.coordinates = value
        elif part == "population":
            node.population = value
        elif part == "region":
            node.region = value
        else:
            return False

        graph.nodes[city] = node
        return True





