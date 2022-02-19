# Computer assignment 1
# Av Lucas Kallenberg
import time

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.sparse import csr_matrix
from scipy.sparse import csgraph
from matplotlib.collections import LineCollection
from scipy.spatial import cKDTree

def read_coordinate_file(filename):  # Create a function that reads the txtfile and rename it as file
    """ Reads a textfile and converts the numbers into coordinates

    :param filename: Textfile containing coordinate points that has '{' and '}' around them
    :type filename: txt file

    :return: Array of coordinates
    :rtype: Numpy array of arrays of floats
    """

    with open(filename, 'r') as file:
        lst =[]  # Create an empty list to store my arrays
        r =1
        line = file.readline()  # Read the first line before we remove all unwanted characters with the while loop
        while line:
            line = line.strip()
            line = line.strip('{')
            line = line.strip('}')
            line = line.split(',')  # Split the arrays in the , mark
            line = [r*np.pi*float(line[1])/180, r*np.log(np.tan(np.pi/4+np.pi*float(line[0])/360))]
            lst.append(line)  # Save x,y into a list
            line = file.readline()
    arr = np.array(lst)  # Converts the list into a numpy array

    return arr

def plot_points(coord, indices,path):
    """ Plots the 'coords' as points and then drawing lines between chosen 'indices'
    and then drawing the shortest path of two points on the lines

    :param coord: Coordinates that sould be ploted
    :type: Array of arrays
    :param indices: Specific points of which coords that lines should be between
    :type: Arrays of arrays
    :param path: The shortest path between two predefined points on top of the lines
    :type: Array of int

    :return: Shows a plot
    :rtype: Have no type
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)   # Create a subplot in the figure to be able to add stuff later
    plt.scatter(coord[:,0],coord[:,1], s = 2, c= 'r')  # Plot the coords as nodes
    seg = np.empty((len(indices),2,2))

    for i,p in enumerate(indices): #Take each array in indices
        seg[i,:,0] = [coord[p[0]][0], coord[p[1]][0]]   #x
        seg[i,:,1] = [coord[p[0]][1],coord[p[1]][1]]   #y
    ax.add_collection(LineCollection(seg,color= 'gray',linewidths= 0.2))    # Drawing the lines to the plot

    seg = np.empty((len(path), 2, 2))
    for i in range(len(path)-1):
        # Segments between points
        seg[i,:,0] = [coord[path[i]][0],coord[path[i+1]][0]]
        seg[i,:,1] = [coord[path[i]][1],coord[path[i+1]][1]]
    ax.add_collection(LineCollection(seg,color= 'blue',linewidths= 1))    # Drawing the lines to the plot


    plt.gca().set_aspect('equal')
    plt.show()

def construct_graph_connections(coord_list, radius):
    """ Creates two lists, one with the distances between coordinates that are within a certain radius
    and a list of the numbers of the coordinates

    :param coord_list: Checking if the coordinats ar within a certain radius of each other and storying those values
    :type: Array of arrays
    :param radius: Predefined value that the function checks against
    :type: Float

    :return: Distances between coords within the radius. Also returns which number of the coords the distance is between
    :rtype: 'distance' list of floats, 'coords' list of arrays
    """
    distance = []
    coords = []
    for n, a in enumerate(coord_list):  # Create a number infront of the arrays and then we loop over the arrays (For me to understand)
        for i in range(n+1, len(coord_list)):  # Takes the second array of the coord_list
            dist = np.linalg.norm(a - coord_list[i])  # Calculates the distance using pythagoras of the coords
            if dist <= radius:  #Checks if the coords are within a certain radius
                distance.append(dist)
                coords.append([n,i])

    distance = np.array(distance) # Converting into numpy arrays
    coords = np.array(coords)
    return distance , coords

def construct_graph(distance, indices,N):
    """ Creates a sparse matrix

    :param distance: The distance between the coordinates of the indices.
    :type: List of floats
    :param indices: The numbers of the coordinates that the distances are between
    :type: A list of arrays
    :param N: A predefined int that is the length of the list distance
    :type: int

    :return: A sparse matrix with the numbers of the coordinates and distances between them
    :rtype: csr_matrix
    """
    indices = indices.T     # Transpose to get the right input
    s = sp.sparse.csr_matrix((distance, indices), shape=[N,N])   # Saves the numbers between the points and the distance in a sparce matrix
    return s

def find_shortest_path(graph, start_node, end_node):
    """
    nodes, shortdist = find_shortest_path(sparsegrahp, start, end)


    :param graph: The sparse matrix that the function checks the values of
    :type: csr matrix
    :param start_node: A predefined value of which coordinate number to start at
    :type: int
    :param end_node: A predefined value of which coordinate number to end at
    :type: int

    :return: 'list' A list of the shortest path of the nodes that it goes through
    'shortestdistance' is the sum of distances between all the connecting nodes in the list from start to end
    :rtype: 'list' is array of ints, 'shortestdistance' is a float
    """

    dist, path = csgraph.shortest_path(graph, directed= False, return_predecessors= True, indices= (start_node))
    # dist = the shortest distance from each node from the starting node, path = last node before
    shortesdistance = dist[end_node]    # We take the distance from the end node

    list = [end_node]
    last = end_node
    # This while loop will be checking if we are back at the start node by starting at our last node and working its
    # way back by looking at the last nodes predecessor and so on
    while last > 0:
        list.append(path[last])     # Add the preceding node of the last node
        last = path[last]
        if last == -9999:   # If there is no path the value of list/last will be -9999
            del list[-1]    # Delete the last value of the list


    list.reverse()   # Get the order from start to end node
    list = np.array(list)
    return list, shortesdistance

def construct_fast_graph_connections(coord_list, radius):
    """Creates two lists, one with the distances between coordinates that are within a certain radius
    and a list of the numbers of the coordinates

    :param coord_list: Checking if the coordinats ar within a certain radius of each other and storying those values
    :type: Array of arrays
    :param radius: Predefined value that the function checks against
    :type: Float

    :return: 'dist' distances between coords within the radius. 'indices' returns which number of the coords the distance is between
    :rtype: 'dist' list of floats, 'indices' list of arrays
    """
    tree = sp.spatial.cKDTree(coord_list)
    dist = []
    indices = []
    points = tree.query_ball_point(coord_list, r=radius)     # Creates lists with the nearby nodes withing range of the choosen coordinate

    for i, point in enumerate(points):      # Check if the element is larger than i to make it undirected
        for j in point:
            if j >= i:
                indices.append(np.array([i, j]))

    speed = np.array(indices)
    up = np.array([coord_list[speed[:, 0]], coord_list[speed[:,1]]])
    dist = np.linalg.norm(up[0]-up[1], axis=-1)

    indices = np.array(indices)   # Convert
    dist = np.array(dist)

    return indices, dist


if __name__=='__main__':

    # Choose file to read: 1 = Sample, 2 = Hungary, 3 = Germany
    Choose = 2

    # Choose fast or slow graph conections: True or False
    Fast = False

    if Choose == 1:
        start_time = time.time()
        arr = read_coordinate_file('SampleCoordinates.txt')
        end_time = time.time()
        print('read_coordinate_file \t\t\t time: ',end_time-start_time)
        radius = 0.08
        start = 0
        end = 5

    elif Choose == 2:
        start_time = time.time()
        arr = read_coordinate_file('HungaryCities.txt')
        end_time = time.time()
        print('read_coordinate_file \t\t\t time: ', end_time - start_time)
        radius = 0.005
        start = 311
        end = 702

    elif Choose == 3:
        start_time = time.time()
        arr = read_coordinate_file('GermanyCities.txt')
        end_time = time.time()
        print('read_coordinate_file \t\t\t time: ', end_time - start_time)
        radius = 0.0025
        start = 1573
        end = 10584

    else:
        print('Wrong input. Choose either 1, 2 or 3 ')

    if Fast == False:
        start_time = time.time()
        distance, coords = construct_graph_connections(arr, radius)
        end_time = time.time()
        print('construct_graph_connections \t time: ', end_time - start_time)

    elif Fast == True:
        start_time = time.time()
        coords , distance = construct_fast_graph_connections(arr,radius)
        end_time = time.time()
        print('construct_fast_graph \t\t\t time: ', end_time - start_time)

    else:
        print('Write in true or false')

    N = len(distance)

    start_time = time.time()
    sparsegrahp = construct_graph(distance, coords,N)
    end_time = time.time()
    print('construct_graph \t\t\t\t time: ', end_time - start_time)

    start_time = time.time()
    nodes, shortdist = find_shortest_path(sparsegrahp, start, end)
    end_time = time.time()
    print('find_shortest_path \t\t\t\t time: ', end_time - start_time)


    start_time = time.time()
    plot_points(arr, coords,nodes)
    end_time = time.time()
    print('plot_points \t\t\t\t\t time: ', end_time - start_time)



