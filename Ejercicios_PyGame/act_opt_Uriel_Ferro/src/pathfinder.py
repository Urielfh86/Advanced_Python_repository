import math
import pygame
from node import Node
from enum import Enum

class Heuristic(Enum):
    Manhattan = 0,
    Diagonal = 1,
    Euclidean = 2

class PathFinder:

    def __init__(self, maze, heuristic):
        self.__maze = maze
        self.__heuristic_func = self.__solve_heuristics(heuristic)

    def calc_path(self, start, end):
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0

        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Inicializar lista abierta y cerrada
        open_list = []
        closed_list = []
        
        # Añadir a la lista abierta el nodo inicial
        open_list.append(start_node)
        
        # Repetir hasta encontrar el destino o la lista abierta quedar con 0 nodos
        while len(open_list) > 0:

            # Buscar el Nodo con menor F en la lista abierta
            current_node = open_list[0]
            current_index = 0

            for index, nodo in enumerate(open_list):
                if nodo.f < current_node.f:
                    current_node = nodo
                    current_index = index
                    
            # Mover el Nodo a la lista cerrada
            open_list.pop(current_index)
            closed_list.append(current_node)
            
            # Comprobar si se ha encontrado el destino
            if current_node.position == end_node.position:
                return self.__return_path(current_node)
            
            # Generar vecinos
            vecinos = []
            adyacentes = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Solo movimientos horizontales y verticales, no diagonales. 

            for new_position in adyacentes: # 4 cuadrantes adyacentes
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                
                # Asegurar que está dentro de los límites del laberinto
                if node_position[0] > (self.__maze.get_size()[0] - 1) or node_position[0] < 0 or node_position[1] > (self.__maze.get_size()[1] - 1) or node_position[1] < 0:
                    continue

                # Asegurar que el nodo es transitable
                if not self.__maze.tile_is_walkable(node_position):
                    continue
                
                # Crear un nuevo Nodo vecino
                new_node = Node(current_node, node_position)
                
                # Añadir el vecino a la lista de vecinos
                vecinos.append(new_node)
              
            # Para cada vecino
            for neighbor in vecinos:
                # Chequeo si el nodo está en la lista cerrada
                if any(x.position == neighbor.position for x in closed_list):
                    continue

                # Calcular G, H y F para el vecino
                neighbor.g = current_node.g + 10
                neighbor.h = self.__heuristic_func(neighbor.position, end_node.position) 
                neighbor.f = neighbor.g + neighbor.h

                for open_neighbor in open_list:
                    if open_neighbor.position == neighbor.position and open_neighbor.g < neighbor.g:
                        open_neighbor.parent = current_node
                        open_neighbor.g = neighbor.g
                        open_neighbor.f = neighbor.f
                        continue

                # Añadir el vecino a la lista abierta
                open_list.append(neighbor)

        # Si no se encuentra un camino devolver una lista vacia
        return []

    def __solve_heuristics(self, heuristic):
        if heuristic == Heuristic.Manhattan:
            return self.__heuristic_manhattan_distance
        elif heuristic == Heuristic.Diagonal:
            return self.__heuristic_diagonal_distance
        elif heuristic == Heuristic.Euclidean:
            return self.__heuristic_euclidean_distance

        return self.__heuristic_manhattan_distance

    def __heuristic_euclidean_distance(self, src, dst):
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return 10 * (math.sqrt((x_dist * x_dist) + (y_dist * y_dist)))

    def __heuristic_manhattan_distance(self, src, dst):
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return 10 * (x_dist + y_dist)

    def __heuristic_diagonal_distance(self, src, dst):
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return (10 * (x_dist + y_dist)) + (-6 * min(x_dist, y_dist))

    def __return_path(self, current_node):
        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent

        # Return reversed path as we need to show from start to end path
        return path[::-1]

    def path_to_img(self, path):
        rows, cols = self.__maze.get_size()
        zoom = self.__maze.get_zoom()
        maze_img = pygame.Surface((cols* zoom, rows * zoom), pygame.SRCALPHA, 32)

        if path:
            for coord in path:
                point = self.__maze.maze_coord_to_screen_point(coord)
                rect = pygame.Rect(point,(zoom, zoom))
                pygame.draw.rect(maze_img, (0, 0, 255, 255), rect)

        return maze_img