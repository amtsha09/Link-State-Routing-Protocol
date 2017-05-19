import numpy as np
import pandas as pd
import sys
l = []
l_str = []
sum_path = 0

def make_file():
    """This function is used to read the input file,  which containing Network Details.
    """
    global l
    global l_str
    f_name = input("Input original network topology matrix data file:")
    f = open ( f_name , 'r')
    l_str = [ line.strip().split(' ') for line in f ]
    f.close()

def create_network_topology():
    """This function is used to create the N/W Topology, prints the Topology Matrix on the user screen.
    """
    global l
    global l_str
    
    print("\nReview original topology matrix:\n")
    
    for i in l_str:
        print(' '.join(i))
    print("\n\n")
    
    l = [[int(i) for i in j] for j in l_str]




def dijkstra(source):

    """Dijkstra Shortest Path Algorithm for weighted graphs. 
    This function implements Dijkstra's algorithm, 
    gets the shortest paths from source router to all others. 
    Here we also create the Parent Child mapping for the graph.
    """
    for idx_i, i in enumerate(l):
        for idx_j, j in enumerate(i):
            if j == -1:
                l[idx_i].pop(idx_j)
                l[idx_i].insert(idx_j, sys.maxsize)


    source = source
    current = source

    map_heap = {}
    v_dist = {}
    v_parent = {}

    for i in range(len(l)):
        map_heap[i+1] = sys.maxsize

    map_heap[current] = 0
    sorted_map_heap = sorted(map_heap.items(), key=lambda x: x[1])
    v_parent[source] = 0
    
    v_dist[sorted_map_heap[0][0]] = sorted_map_heap[0][1]
    row = l[sorted_map_heap[0][0]-1]
    del map_heap[sorted_map_heap[0][0]]



    while (len(map_heap) != 0):

        for i,j in enumerate(row):
            if i+1 in map_heap and (j + v_dist[current]) < map_heap[i+1]:
                map_heap[i+1] = j + v_dist[current]
                v_parent[i+1] = current


        sorted_map_heap = sorted(map_heap.items(), key=lambda x: x[1])
        v_dist[sorted_map_heap[0][0]] = sorted_map_heap[0][1]

        current = sorted_map_heap[0][0]
        row = l[sorted_map_heap[0][0]-1]
        del map_heap[sorted_map_heap[0][0]]

    return (v_dist,v_parent)


def connection_table(source,vd):

	"""This function creates a connection table i.e. the destination and interface combination.
    """
    global sum_path
    sum_path = 0

    print("\n\n Router %d Connection Table" %source)
    print("Destination \t","Interface")
    print("==========================\n")
    for i,j in vd.items():
        print("   ",i,"\t\t   ",j)
        sum_path += j


def path(source,destination,vp,vd):

    """Gets the path from source to destination & also the cost along the path.
    """
    list_child = []
    list_parent = []
    for i,j in vp.items():
        list_child.append(i)
        list_parent.append(j)

    link = []
    link.append(destination)
    a = destination
    while link.count(source) != 1:
        b = list_child.index(a)
        a = list_parent[b]
        link.append(a)
    print(vd)
    print("The shortest path from router %d to router %d is: "%(source,destination), "-".join([str(i) for i in link[::-1]]),
          " the total cost is: ",vd[destination])


def router_remove(rem,source):
    """This function is used to remove (turn-off) the Router from the network
    """
    global l_str
    del l_str[rem-1]
    for i in l_str:
        del i[rem-1]
    create_network_topology()
    vd,vp = dijkstra(source)
    connection_table(source,vd)


def best_router():
    """function to find the Best router for broadcasting"""
    global l
    source = [i for i in range(1,len(l)+1)]
    for j in source:
        vd,vp = dijkstra(j)
        connection_table(j,vd)


def main():
    source = 0
    choice = 0
    destination = 0
    while (choice != 6):
        print("\n\n\n CS542 Link State Routing Simulator \n\n")
        print("(1) Create a Network Topology")
        print("(2) Build a Connection Table")
        print("(3) Shortest Path to Destination Router")
        print("(4) Modify a Topology")
        print("(5) Best Router for Broadcast")
        print("(6) Exit\n")
        choice = int(input("Command: "))
        
        if choice == 1:
            make_file()
            create_network_topology()
        elif choice == 2:
            source = int(input("Select a source router: "))
            vd,vp = dijkstra(source)
            connection_table(source,vd)
        elif choice == 3:
            if source == 0:
                print("please enter the source")
            else:
                destination = int(input("Select the destination router: "))
                path(source,destination,vp,vd)
        elif choice ==4:
            rem = int(input("Select a router to be removed: "))
            if source != 0 and destination != 0 and source != rem and destination != rem :
                router_remove(rem,source)
                path(source,destination,vp,vd)
            else:
                router_remove(rem,source)
        elif choice == 5:
            best_router()


if __name__ == '__main__':
    main()
