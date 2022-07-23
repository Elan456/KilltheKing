from person import Person, Point
from pathing import astar
from egene import pygameTools as pgt
import math

class Guard(Person):
    def __init__(self, x, y, map, color=(100, 100, 100), speed=1):
        self.map = map
        self.state = "waiting"
        self.d = 0
        super().__init__(x, y, map.quadtree, color, speed)


    def gotoo(self, end: Point):
        self.path = astar(Point(self.x, self.y), end, self.map)
        self.next_waypoint = self.path.points[0]
        self.state = "pathing"


    def new_waypoint(self):
        self.path.points.pop(0)
        self.next_waypoint = self.path.points[0]
        self.d = math.atan2(self.next_waypoint.y - self.y, self.next_waypoint.x - self.x)

    def update(self):
        if self.state == "pathing":
            if pgt.cdistance(self.x, self.y, self.next_waypoint.x, self.next_waypoint.y) <= self.speed:
                self.new_waypoint()
            self.x += math.cos(self.d) * self.speed
            self.y += math.sin(self.d) * self.speed
            self.check_collision()