import json
from Graph import *
from GraphStatistics import *
from UserView import *

class Controller:
    def __init__(self):
        return

    #runs and loops throught the queries
    def main(self):
        #Create both the graph, statistics, and view objects to create the base for CSAir
        graph = Graph()
        statistics = GraphStatistics()
        view = UserView()

        #Read file and build graph
        print("Do you want to use original file?(Y/N)")
        f_ans = raw_input()
        if f_ans == 'Y':
            file = '/Users/kushmaheshwari/cs242/Assignment2/test_data.json'
        else:
            file = '/Users/kushmaheshwari/cs242/Assignment2/map_data_written.json'


        f = open(file, 'r')
        json_data = json.loads(f.read())
        graph.build_nodes(json_data['metros'])
        graph.build_edges(json_data['routes'])

        # Include CMI or not
        print("Do you want to include CMI?(Y/N)")
        ans = raw_input()
        if ans == 'Y':
            file2 = '/Users/kushmaheshwari/cs242/Assignment2/cmi_hub.json'
            f2 = open(file2, 'r')
            json_data = json.loads(f2.read())
            graph.build_nodes(json_data['metros'])
            graph.build_edges(json_data['routes'])

        #This loop continually asks users for what they want to know about CSAir
        #Each number grabs data from statistics and send data to view class to display
        while(True):
            view.print_options()
            view.ask_questions()
            userInput = raw_input()


            #What each number corresponds too
            # "[0] exit\n"
            # "[1] City list\n"
            # "[2] City Information\n"
            # "[3] Longest Flight\n"
            # "[4] Shortest flight\n"
            # "[5] Average Flight Distance \n"
            # "[6] Biggest Population\n"
            # "[7] Smallest Population\n"
            # "[8] Average Population\n"
            # "[9] Continents and Cities\n"
            # "[10] Top 3 Hub Cities\n"
            # "[11] Map URl\n"
            # "[12] Remove a City\n"
            # "[13] Remove a Route\n"
            # "[14] Add a City\n"
            # "[15] Add a Route\n"
            # "[16] Edit a City\n"
            # "[17] Info about a Route\n"
            # "[18] Shortest Path\n"
            # "[19] Save to Disk"


            if(userInput == '0'):
                print("Exiting Query Mode")
                exit(0)
            elif(userInput == '1'):
                view.print_cities(graph)

            elif(userInput == '2'):
                print("Please type in a code for a city:")
                cityCode = raw_input()
                view.print_city(cityCode, graph)

            elif(userInput == '3'):
                longestFlight = statistics.get_longest_flight(graph)
                view.print_longest_flight(longestFlight)

            elif(userInput == '4'):
                shortestFlight = statistics.get_shortest_flight(graph)
                view.print_shortest_flight(shortestFlight)

            elif(userInput == '5'):
                averageDistance = statistics.get_average_distance(graph)
                view.print_average_distance(averageDistance)

            elif(userInput == '6'):
                biggestCity = statistics.get_biggest_city(graph)
                view.print_biggest_city(biggestCity)

            elif(userInput == '7'):
                smallestCity = statistics.get_smallest_city(graph)
                view.print_smallest_city(smallestCity)

            elif(userInput == '8'):
                averageSize = statistics.get_average_size(graph)
                view.print_average_size(averageSize)

            elif(userInput == '9'):
                 continents = statistics.get_continets(graph)
                 view.print_continents(continents)

            elif(userInput == '10'):
                hubCities = statistics.get_hub_cities(graph)
                view.print_hub_cities(hubCities)

            elif(userInput == '11'):
                url = statistics.generate_url(graph)
                view.launch_URL(url)

            elif(userInput == '12'):
                print("Please type in a city code to remove:")
                cityCode = raw_input()
                ans = graph.remove_city(cityCode)
                if ans == False:
                    print "Not a city"

            elif(userInput == '13'):
                print("Please type in a route to remove:")
                route = raw_input()
                ans = graph.remove_route(route)
                if ans == False:
                    print "Not a route"

            elif(userInput == '14'):
                print("City Information:")
                cityJSON = view.add_city();
                graph.add_node(cityJSON)

            elif(userInput == '15'):
                print("Route Information:")
                routeJSON = view.add_route();
                graph.add_edge(routeJSON)

            elif(userInput == '16'):
                ans = view.edit_city(graph)
                if ans == False:
                    print "Bad Edit"

            elif(userInput == '17'):
                print("Print out all the cities you want to visit in order from start to finish with a comma in between: ")
                route = raw_input()
                ans = statistics.get_route(route, graph)
                if(ans == False):
                    print("No such route")
                else:
                    print("Distance: " + str(ans[0]))
                    print("Cost: " + str(ans[1]))
                    print("Time: " + str(ans[2]) + "mins")

            elif(userInput == '18'):
                print("Print Shortest Path between 2 cities with a comma in between: ")
                route = raw_input()
                path = statistics.get_shortest_path(route, graph)
                if path == False:
                    print "No such path"
                else:
                    print("The shortest path is between " + path[0] + " and " + path[len(path)-1] + " is: "),
                    pathString = ''
                    for p in path:
                        print(p),
                        pathString += p + ','
                    print

                    pathString = pathString[:-1]
                    ans = statistics.get_route(pathString, graph)
                    print("Distance: " + str(ans[0]))
                    print("Cost: " + str(ans[1]))
                    print("Time: " + str(ans[2]) + "mins")

            elif(userInput == '19'):
                print("Saving to Disk")
                graph.save_to_disk()


#runs the entire program
if __name__ == '__main__':
    controller = Controller()
    controller.main()