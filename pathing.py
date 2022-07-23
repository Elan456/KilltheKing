import img_to_map
from quadtree import Point
from egene import pygameTools as pgt
import pygame
import time
import bisect


def point_to_nearest_node(point, map):  # Finds the navigation node closest to a point without going through walls
    # Find nearest power of 25 to check for node there
    # print(map.node_map)
    return sorted(map.nodes, key=lambda n: pgt.cdistance(n.x, n.y, point.x, point.y) if not map.line_blocked(point, n) else float("inf"))[0]


class SimplePath:
    def __init__(self, points):
        self.points = points

    def draw(self, surface):
        for i, n in enumerate(self.points):
            pygame.draw.circle(surface, (0, 0, 255), (n.x, n.y), 3)

            try:
                pygame.draw.line(surface, (0, 0, 255), (n.x, n.y), (self.points[i + 1].x, self.points[i + 1].y), 2)
            except IndexError:
                pass
            pgt.text(surface, (n.x, n.y), str(i), (0, 0, 0), 30)


class Path:
    def __init__(self, old_path, node_to_attach, end_node):  # Creating a new path must start with an existing path with a new node being added
        if old_path is not None:  # The initial path won't have an old path
            self.length = old_path.length + pgt.cdistance(old_path.nodes[-1].x, old_path.nodes[-1].y, node_to_attach.x, node_to_attach.y)
            self.nodes = old_path.nodes + [node_to_attach]
        else:
            self.length = 0
            self.nodes = [node_to_attach]

        self.distance_to_goal = pgt.cdistance(node_to_attach.x, node_to_attach.y, end_node.x, end_node.y)
        self.score =self.length + self.distance_to_goal

        self.potential_paths = None
        self.end_point = end_node

    def expand(self):  # Explores all options a path could take
        self.potential_paths = []
        for c in self.nodes[-1].connections:  # Explore all of the last's nodes connections
            if c.nodes[1] not in self.nodes:  # To prevent going to the same spot twice
                self.potential_paths.append(Path(self, c.nodes[1], self.end_point))

    def __lt__(self, other):
        return self.score < other.score


# Uses A* to find the shortest path between two points
def astar(start: Point, end: Point, map: img_to_map.Map, surface=None):
    if not map.line_blocked(start, end):
        print("CAN SEE")
        return SimplePath([start, end])
    start_time = time.time()
    end_node = point_to_nearest_node(end, map)
    i_path = Path(None, point_to_nearest_node(start, map), end_node)
    priority = [i_path]

    # print("priortiy:", priority)
    while True:
        # print("length", len(priority))
        # print(priority[0].nodes[-1].x, priority[0].nodes[-1].y)
        # print(priority[0].potential_paths)
        check = priority[0]
        # print(len(priority), check.nodes[-1].x, check.nodes[-1].y)


        # time.sleep(1)
        timeout = time.time() - start_time > 1
        if check.nodes[-1] == end_node or timeout:  # Found the end
            # Find furthest one the start point can still see
            si = 0
            for i in range(len(check.nodes) - 1, -1, -1):
                #print("i:", i)
                if not map.line_blocked(start, check.nodes[i]):
                    si = i
                    #print("si:", si)
                    break


            ei = len(check.nodes) - 1
            # Find earliest point the end point can still see
            if not timeout:
                for i in range(0, len(check.nodes)):
                    if not map.line_blocked(end, check.nodes[i]):
                        ei = i
                        #print("ei:", ei)

            # time.sleep(2)
            #print("SI EI:", si, ei)
            # return check
            if (si == 0 and ei == 0):# or (si == len(check.nodes) - 1):
                #print("SIMPLE")
                return SimplePath([start, end])
            final = SimplePath([start] + check.nodes[si:max(si, ei) + 1])  # Makes first and last node approximates the actual points
            if not timeout:
                final.points += [end]
            return final
        else:
            priority.pop(0)  # If it is completly expanded then the parent is no longer needed
            check.expand()
            for p in check.potential_paths:
                bisect.insort(priority, p)
            # print([p.score for p in priority])



