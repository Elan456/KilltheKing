from person import Person, Point
from pathing import find_path
from egene import pygameTools as pgt
import math
import pygame
from multiprocessing import Process, Manager
import copy


class Guard(Person):
    def __init__(self, x, y, map, color=(100, 100, 100), speed=1):
        self.p = None
        self.q = None
        self.map = map
        self.state = "waiting"
        self.d = 0
        self.target_point = None
        self.path = None
        self.next_waypoint = None
        super().__init__(x, y, map.quadtree, color, speed)


    def gotoo(self, end: Point):  # Tell the guard to go somewhere
        self.target_point = Point(end.x, end.y)
        self.path = find_path(Point(self.x, self.y), self.target_point, self.map)
        self.state = "pathing"  # means moving along a math
        self.new_waypoint(initial_setup=True)


    def new_waypoint(self, initial_setup=False):  # Once a point along the path is reached, go to the next one
        # Checking if that path is full or not
        # If the path is not full then try making a new path now that the guard is a bit closer
        if not initial_setup and self.path.points[-1] != self.target_point:  # Not full path
            print("Not on a full path trying again")
            self.gotoo(self.target_point)

        if len(self.path.points) > 1:  # Only move on if there is something to move too
            if not initial_setup:
                self.path.points.pop(0)
            self.next_waypoint = self.path.points[0]
            self.d = math.atan2(self.next_waypoint.y - self.y, self.next_waypoint.x - self.x)
        else:
            self.state = "waiting"  # finished pathing

    def draw_path(self, surface):
        if self.path is not None:
            self.path.draw(surface)
            pygame.draw.line(surface, (0, 0, 255), (self.x, self.y), (self.path.points[0].x, self.path.points[0].y))
    def update(self):
        if self.state == "pathing":
            if pgt.cdistance(self.x, self.y, self.next_waypoint.x, self.next_waypoint.y) <= self.speed * 1.1:
                self.new_waypoint()

            self.x += math.cos(self.d) * self.speed
            self.y += math.sin(self.d) * self.speed
        elif self.state == "waiting":
            pass  # Do nothing
        else:
            self.check_collision()

