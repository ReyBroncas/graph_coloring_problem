import networkx as nx
import matplotlib.pyplot as plt
# EDITED BY MARK


# This was edited on a new branch

def matrix_symetry_check(matrix: list) -> bool:
    """
    Function gets a 2D-array (matrix) and check whether it is symetrical.
    """

    symetry_flag = True
    for rows in range(0, len(matrix)):
        for col in range(0, len(matrix)):
            if matrix[rows][col] != matrix[col][rows]:
                symetry_flag = False
    return symetry_flag


def read_from_file() -> dict:
    """
    (None) -> dict / None
    Function reads matrix from a file and forms a dictionary with all adjacent
    vertices.
    Returns None if matrix is no symetrical
    """

    adj_vertices_dict = {}
    matrix = []
    vertex = 1
    mf = open("matrix.txt", "r")
    for line in mf:
        line = line.strip()
        line_list = line.split(",")
        line_list = [int(elm) for elm in line_list]
        matrix.append(line_list)
        for vertice in range(1, len(line_list) + 1):
            if line_list[vertice - 1] == 1:
                if vertex in adj_vertices_dict.keys():
                    adj_vertices_dict[vertex][0].append(vertice)
                else:
                    adj_vertices_dict[vertex] = [[vertice]]
        vertex += 1
    mf.close()
    for key, value in adj_vertices_dict.items():
        adj_vertices_dict[key].append(0)
        adj_vertices_dict[key].append(
            [0 for zero in range(0, len(adj_vertices_dict[key][0]))])
    if matrix_symetry_check(matrix):
        return adj_vertices_dict
    else:
        return None


def safeCheck(c: int, v: int, vDict: dict) -> bool:
    """
    This function checks if it is safe to put color c in vertex v, comparing
    colors of adjacent vertices
    """

    for k, value in vDict.items():
        if k in vDict[v][0] and vDict[k][1] == c:
            return False
    return True


def sync(s_vertex: int, vDict: dict) -> None:
    """
    Saves information in vDict whether s_vertex was
    visited before
    """

    for k, v in vDict.items():
        for indx, vertex in enumerate(v[0]):
            if vertex == s_vertex:
                v[-1][indx] = 1


def graph_color(v: int, vDict: dict, depth=1, v_real=set(), color_c=False) -> dict:
    """
    (int,dict) -> vDict
    Main function that (using DFC path) tries to color each v in vDict
    using backtracking
    """

    while 1:
        if not color_c:
            sync(v, vDict)
        v_real.add(v)
        for c in range(vDict[v][1] + 1, 5):
            if safeCheck(c, v, vDict):
                vDict[v][1] = c
                break
        if vDict[v][1] == 5:
            vDict[v][1] = 0
            v_real.remove(v)
            return vDict, True
        if ((sum(vDict[v][-1]) == len(vDict[v][-1])) and v in v_real):
            return vDict, False
        for i, h in enumerate(vDict[v][-1]):
            if not h:
                vDict, color_c = graph_color(
                    vDict[v][0][i], vDict, depth=depth + 1)
                break


def color_graph(vertex_color_dict: dict, adj_vertices_dict: dict) -> None:
    """
    Function gets two dictionaries:
    1) dictinary of vertices with colors they should be colored in
    2) dictionary of vertices adjacent to each other
    , and draws a colored graph using matplotlib and networkx libraries.
    """

    colors_dict = {1: 'orange', 2: 'yellow', 3: 'red', 4: 'purple'}
    G = nx.Graph()

    for vertice, adjacent_vertices in adj_vertices_dict.items():
        G.add_node(vertice)
        G.nodes[vertice]['color'] = colors_dict[vertex_color_dict[vertice]]
        for i in adjacent_vertices:
            G.add_edge(vertice, i)

    color = [node[1]['color'] for node in G.nodes(data=True)]
    nx.draw_networkx(G, with_labels=True, node_color=color, node_size=700)
    plt.show()


def form_base_colored_dict(colored_dict_unmod: dict) -> tuple:
    """
    Function gets dictionary where [key] is a vertice, and [value] is list of
    [[adjacent vertices], [color of vertex], [info used for backtracking]],
    and splits it into two *clean* dictionaries.
    The idea of the function is to split a main dictionary to make it easier to
    form and print a graph.
    """

    final_colored_dict = {}
    final_adj_vertex_dict = {}

    for key in colored_dict_unmod.keys():
        final_colored_dict[key] = colored_dict_unmod[key][1]
        final_adj_vertex_dict[key] = colored_dict_unmod[key][0]

    if 0 in final_colored_dict.values():
        return None
    else:
        return final_colored_dict, final_adj_vertex_dict


if __name__ == "__main__":
    if read_from_file():
        adjacent_dict = read_from_file()
        colored_dict = graph_color(1, adjacent_dict)
        if form_base_colored_dict(colored_dict[0]):
            final_colored_dict, final_adj_vertex_dict = form_base_colored_dict(
                colored_dict[0])
            color_graph(final_colored_dict, final_adj_vertex_dict)
        else:
            print("\n\n\tGraph can't not be colored in 3 colors.\n\n")
    else:
        print("\n\n\t\tInvalid matrix!\n\n")
