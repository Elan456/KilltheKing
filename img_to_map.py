import numpy as np
from quadtree import Point
import quadtree
from PIL import Image
import pickle
import math
from egene import pygameTools as pgt
import sys
import pygame

sys.setrecursionlimit(10000)


class Connection:
    def __init__(self, nodes, length):
        self.nodes = nodes
        self.length = length


class Node:
    def __init__(self, x, y):
        self.connections = None
        self.x = x
        self.y = y
        self.connections = []


def is_corner(n, node_map):
    neis = {}
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                neis[(dx, dy)] = node_map[int(n.y // 25 + dy)][int(n.x // 25) + dx] == 0


    if neis[(-1, -1)] and not (neis[(0, -1)] or neis[(-1, 0)]):
        return True
    if neis[(-1, 1)] and not (neis[(0, 1)] or neis[(-1, 0)]):
        return True
    if neis[(1, -1)] and not (neis[(0, -1)] or neis[(1, 0)]):
        return True
    if neis[(1, 1)] and not (neis[(0, 1)] or neis[(1, 0)]):
        return True

    # if neis[(-1, -1)] and neis[(-1, 0)] and neis[(0, -1)]:
    #     return True
    # if neis[(-1, 1)] and neis[(0, 1)] and neis[(-1, 0)]:
    #     return True
    # if neis[(1, -1)] and neis[(0, -1)] and neis[(1, 0)]:
    #     return True
    # if neis[(1, 1)] and neis[(0, 1)] and neis[(1, 0)]:
    #     return True


class Map:
    def __init__(self, array):
        print("INITALIZING MAP")
        self.walls = set()
        self.nodes = []
        self.node_map = [[0 for c in range(array.shape[1])] for r in range(array.shape[0])]
        for y in range(array.shape[0]):
            for x in range(array.shape[1]):
                if sum(array[y, x]) == 0:
                    self.walls.add(Point(x * 25, y * 25))
                elif sum(array[y, x]) == 255 * 3:
                    n = Node(x * 25 + 25 / 2, y * 25 + 25 / 2)
                    self.nodes.append(n)
                    self.node_map[y][x] = n


        # Finding the nodes that are on a corner
        self.corner_nodes = []
        for n in self.nodes:
            if is_corner(n, self.node_map):
                self.corner_nodes.append(n)

        self.nodes = self.corner_nodes

        # Remake node map with just the corners
        self.node_map = [[0 for c in range(array.shape[1])] for r in range(array.shape[0])]
        for n in self.nodes:
            self.node_map[int(n.y / 25)][int(n.x / 25)] = n

        # self.nodes = self.corner_nodes

        self.quadtree = quadtree.QuadTree(quadtree.Rectangle(0, 0, array.shape[1] * 25, array.shape[0] * 25), 6)
        for wall in self.walls:
            self.quadtree.insert(Point(wall.x, wall.y))

        for i in self.nodes:  # Connected nodes together if there is no wall inbetween
            for j in self.nodes:
                if not self.line_blocked(Point(i.x, i.y), Point(j.x, j.y)):
                    i.connections.append(Connection([i, j], pgt.cdistance(i.x, i.y, j.x, j.y)))
            # if len(i.connections) > 4:
            #     i.connections.sort(key=lambda x: x.length)
            #     i.connections = i.connections[:4]

    def line_blocked(self, start, end):  # Checks if a straight line through this map is not blocked (used for pathing)
        loc = Point(start.x, start.y)
        d = math.atan2(end.y - start.y, end.x - start.x)
        while pgt.cdistance(loc.x, loc.y, end.x, end.y) > 10:
            if len(self.quadtree.query(quadtree.Rectangle(loc.x - 25, loc.y - 25, 25, 25))) > 0:  # It hits a wall
                return True
            loc.x += math.cos(d) * 10
            loc.y += math.sin(d) * 10
        return False

    def draw_nodes(self, surface):
        for n in self.nodes:
            pygame.draw.circle(surface, (100, 100, 100), (n.x, n.y), 4)
            for c in n.connections:
                pygame.draw.line(surface, (100, 100, 100), (c.nodes[0].x, c.nodes[0].y), (c.nodes[1].x, c.nodes[1].y), 3)
        for n in self.corner_nodes:
            pygame.draw.circle(surface, (0, 100, 100), (n.x, n.y), 4)


def convert(image_name):
    im = np.asarray(Image.open("assets\\"+image_name).convert("RGB"))
    return Map(im)


if __name__ == "__main__":
    # pickle.dump(convert("Big.png"), open("big.p", "wb"))
    pickle.dump(convert("Basic.png"), open("basic.p", "wb"))