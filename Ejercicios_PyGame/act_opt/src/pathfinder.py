from enum import Enum
import math

import pygame

from node import Node

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

        #Tu codigo aqui

        # test if goal is reached or not, if yes then return the path
        # if current_node == end_node:
        #     return return_path(current_node)

        #Tu codigo aqui

        # if no path is found return empty path
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