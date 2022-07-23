import person
import math


class Player(person.Person):
    def __init__(self, x, y, qt):
        super().__init__(x, y, qt, speed=4)

    def move(self, keystates):
        d = []
        if keystates.w:
            d.append(3 * math.pi / 2)
        if keystates.s:
            d.append(math.pi / 2)
        if keystates.a:
            d.append(math.pi)
        if keystates.d:
            d.append(0)
        if keystates.d and keystates.w:
            d = 7 * math.pi / 4
        elif len(d) > 0:
            d = sum(d) / len(d)
        else:
            return
        self.xv += math.cos(d) * self.speed
        self.yv += math.sin(d) * self.speed
