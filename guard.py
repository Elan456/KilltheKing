from person import Person, Point
from pathing import astar, astar_friend
from egene import pygameTools as pgt
import math
from multiprocessing import Process, Manager
import copy


class Guard(Person):
    def __init__(self, x, y, map, color=(100, 100, 100), speed=1):
        self.p = None
        self.q = None
        self.map = map
        self.state = "waiting"
        self.d = 0
        super().__init__(x, y, map.quadtree, color, speed)

        # Creating the process incharge of calculating paths for this guard
        self.manager = Manager()
        self.talk = self.manager.dict()
        print("at make process")
        self.p = Process(target=astar_friend, args=(self.talk,))
        self.p.start()
        print("process started")
        exit()


    def gotoo(self, end: Point):
        """
        State will be set to thinking until the path is calculated in a subprocess
        """
        print(self.state)
        if self.state != "thinking" and self.state != "pathing":
            self.state = "thinking"

            # Add a request to our thinking process
            print("MADE REQUEST")
            self.talk["request"] = [Point(self.x, self.y), end, self.map]


    def new_waypoint(self):
        if len(self.path.points) > 1:  # Only move on if there is something to move too
            self.path.points.pop(0)
            self.next_waypoint = self.path.points[0]
            self.d = math.atan2(self.next_waypoint.y - self.y, self.next_waypoint.x - self.x)
        else:
            self.state = "waiting"

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

        if self.state == "thinking":  # Trying to make a path from one point to another
            print(self.talk["path"])
            if self.talk["path"] != None:
                self.path = copy.copy(self.talk["path"])
                self.talk["path"] = None  # Clears the path so a new one must be made

                print("\n path recieved \n")
                self.state = "pathing"  # And start following it
                self.next_waypoint = self.path.points[0]

