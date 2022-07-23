from quadtree import Rectangle, Point
import pygame
import math
from egene import pygameTools as pgt


class Person:
    def __init__(self, x, y, qt, color=(100, 100, 100), speed=1):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.speed = speed
        self.qt = qt
        self.color = color

    def check_collision(self):  # Checks if the person is colliding with a wall and returns which direction to move them

        self.touching_walls = self.qt.query(Rectangle(self.x - 10 - 25, self.y - 10 - 25, 45, 45))
        # self.touching_walls.sort(key=lambda p: pgt.cdistance(p.x + 25/2, p.y + 25/2, self.x, self.y))
        if len(self.touching_walls) > 0:
            tw = self.touching_walls[0]
            d = math.atan2((self.y - (tw.y + 25 / 2)), (self.x - (tw.x + 25 / 2)))
            # print("cos:", math.cos(d), "sin:", math.sin(d))
            if abs(math.cos(d)) > abs(math.sin(d)):
                self.x += math.cos(d) * 2
            else:
                self.y += math.sin(d) * 2

    def pos_update(self):  # Updates the person's position based on their velocity vectors and collisions
        self.x += self.xv
        self.y += self.yv

        # Apply friction
        self.xv /= 10
        self.yv /= 10

        self.check_collision()

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), 10)
        # if len(self.touching_walls) > 0:
        #     p = self.touching_walls[0]
        #     # print("drawing walls")
        #     pygame.draw.circle(surface, (100, 200, 0), (p.x + 25 / 2, p.y + 25 / 2), 10)
