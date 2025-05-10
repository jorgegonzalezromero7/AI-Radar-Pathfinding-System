# Required imports
import numpy as np
import networkx as nx
from Boundaries import Boundaries
from Map import EPSILON

# Number of nodes expanded in the heuristic search (stored in a global variable to be updated from the heuristic functions)
NODES_EXPANDED = 0

def h1(current_node, objective_node) -> np.float32:
    """ First heuristic to implement """
    global NODES_EXPANDED
    h = 0
    ...
    NODES_EXPANDED += 1
    return h

def h2(current_node, objective_node) -> np.float32:
    """ Second heuristic to implement """
    global NODES_EXPANDED
    h = 0
    ...
    NODES_EXPANDED += 1
    return h

def build_graph(detection_map: np.array, tolerance: np.float32) -> nx.DiGraph:
    """ Builds an adjacency graph (not an adjacency matrix) from the detection map """
    # The only possible connections from a point in space (now a node in the graph) are:
    #   -> Go up
    #   -> Go down
    #   -> Go left
    #   -> Go right
    # Not every point has always 4 possible neighbors
    G = nx.Graph()

    # Obtener las dimensiones del mapa
    height, width = detection_map.shape

    # Función para verificar si una celda está dentro de los límites
    def is_within_bounds(x, y):
        return 0 <= x < width and 0 <= y < height

    # Iterar sobre cada celda del mapa
    for y in range(height):
        for x in range(width):
            # Nodo actual
            current_node = (x, y)

            # Agregar el nodo al grafo
            G.add_node(current_node, cost=detection_map[y, x])

            # Posibles movimientos: arriba, abajo, izquierda, derecha
            neighbors = [
                (x, y - 1),  # Arriba
                (x, y + 1),  # Abajo
                (x - 1, y),  # Izquierda
                (x + 1, y)  # Derecha
            ]

            # Evaluar cada vecino
            for nx, ny in neighbors:
                if is_within_bounds(nx, ny):
                    # Verificar si la diferencia de costos está dentro de la tolerancia
                    if detection_map[ny, nx] <= tolerance:
                        # Agregar una arista al grafo con el costo del vecino
                        G.add_edge(current_node, (nx, ny), weight=detection_map[ny, nx])

    return G

def discretize_coords(high_level_plan: np.array, boundaries: Boundaries, map_width: np.int32, map_height: np.int32) -> np.array:
    # Crear un array para almacenar las coordenadas discretizadas
    discretized_coords = np.zeros((len(high_level_plan), 2), dtype=np.int32)

    # Calcular los incrementos por celda en latitud y longitud
    delta_lat = (boundaries.max_lat - boundaries.min_lat) / (map_height - 1)
    delta_lon = (boundaries.max_lon - boundaries.min_lon) / (map_width - 1)

    # Iterar sobre cada coordenada en el plan de alto nivel
    for i, (lat, lon) in enumerate(high_level_plan):
        # Convertir latitud a coordenada y (fila)
        y = int(round((lat - boundaries.min_lat) / delta_lat))
        # Convertir longitud a coordenada x (columna)
        x = int(round((lon - boundaries.min_lon) / delta_lon))

        # Asegurarse de que las coordenadas estén dentro de los límites de la malla
        y = max(0, min(y, map_height - 1))
        x = max(0, min(x, map_width - 1))

        # Almacenar las coordenadas discretizadas
        discretized_coords[i] = [x, y]

    return discretized_coords

def path_finding(G: nx.DiGraph,
                 heuristic_function,
                 locations: np.array, 
                 initial_location_index: np.int32, 
                 boundaries: Boundaries,
                 map_width: np.int32,
                 map_height: np.int32) -> tuple:
    """ Implementation of the main searching / path finding algorithm """
    ...

def compute_path_cost(G: nx.DiGraph, solution_plan: list) -> np.float32:
    total_cost = 0.0

    # Iterate through the solution plan to sum the weights of the destination nodes
    for i in range(1, len(solution_plan)):  # Start from the second node
        current_node = solution_plan[i]

        # Add the cost of the current node (destination node in the edge)
        total_cost += G.nodes[current_node]['cost']

    return np.float32(total_cost)
