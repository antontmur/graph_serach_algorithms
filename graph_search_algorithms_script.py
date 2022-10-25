from math import sqrt
from utils import generate_simple_graph, generate_maze_graph, print_path
from data_structures import AbstractNodeStorageClass
from data_structures import Stack
from data_structures import Queue
from data_structures import DijkstraQueue
from data_structures import AStarQueue
from graph_animation import GraphAnimator
from networkx import Graph


def find_path(
        graph: Graph,
        start_node: int,
        goal_node: int,
        nodes_storage_structure_name: str,
        animator: GraphAnimator
    ):
    """
        Universal function for traversing graph searching the path from start_node to goal_node.
        It uses graph structure and the auxilary node storage structure.
        The animator is used to create animations of the search process.
    """

    color = ['white'] * graph.number_of_nodes()      # coloring all nodes to white
    dist = [float('Inf')] * graph.number_of_nodes()  # the distances to all the nodes at the start are infinity
    parent = dict()                                  # dictionary {node : its parent}

    nodes_storage = {
        'Stack': Stack(),
        'Queue': Queue(),
        'DijkstraQueue': DijkstraQueue(dist),
        'AStarQueue': AStarQueue(graph, dist, goal_node)
    }[nodes_storage_structure_name]

    # place the start node to the storage
    nodes_storage.insert(start_node)
    dist[start_node] = 0
    animator.add_frame(color, parent, start_node)

    # Loop until there are nodes in storage
    while not nodes_storage.empty():
        current_node = nodes_storage.get_first()

        if current_node == goal_node:
            # End of the search, the goal is found.
            print_path(goal_node, parent)
            animator.add_frame(color, parent, current_node)
            break

        # take all the neighbours of the current node
        neighbours = list(graph.adj[current_node])
        for node_to_go in neighbours:
            if color[node_to_go] == 'white':            # if this neighbour is new
                color[node_to_go] = 'grey'              # paint in grey
                nodes_storage.insert(node_to_go)        # add to node storage
                parent[node_to_go] = current_node       # saving the parent (where we came from)
                dist[node_to_go] = dist[current_node] + graph.get_edge_data(node_to_go, current_node)['weight']
            else:
                # Otherwise we have to solve the conflict of duplicates
                # comparing the distance from the current node to the neighbor
                # with the distance to it along the previously found path
                weight_from_current_node = graph.get_edge_data(node_to_go, current_node)['weight']
                if dist[current_node] + weight_from_current_node < dist[node_to_go]:
                    dist[node_to_go] = dist[current_node] + weight_from_current_node

        # painting the current node in black, we won't come back here
        color[current_node] = 'black'
        animator.add_frame(color, parent, current_node)

    fig = graph_animator.make_animation()
    fig.show()


# Building small simple graph
# graph, start_node, goal_node = generate_simple_graph()

# Create helper class for pretty animations and make a first shot
# graph_animator = GraphAnimator(graph, start_node, goal_node)

# # DFS on simple graph
# find_path(graph, start_node, goal_node, 'Stack', graph_animator)

# BFS on simple graph
# find_path(graph, start_node, goal_node, 'Queue', graph_animator)

# Dijkstra algorithm on simple graph
# find_path(graph, start_node, goal_node, 'DijkstraQueue', graph_animator)

graph, maze_list = generate_maze_graph()
start_node, goal_node = 113, 198
graph_animator = GraphAnimator(graph, start_node, goal_node, is_maze=True, maze_list=maze_list)

# Dijkstra algorithm on large graph
# find_path(graph, start_node, goal_node, 'DijkstraQueue', graph_animator)

# A* algorithm on large graph
find_path(graph, start_node, goal_node, 'AStarQueue', graph_animator)