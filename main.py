from player import Player
from guard import Guard
from quadtree import *
import pickle
from pathing import astar

map_name = "Big"

d_width = 500
d_height = 500
Display = pygame.display.set_mode((d_width, d_height))

basic_map = pygame.image.load("assets\\"+map_name+".png").convert()
basic_map = pygame.transform.scale(basic_map, (basic_map.get_width() * 25, basic_map.get_height() * 25))
print(basic_map.get_width(), "width")

white = (255, 255, 255)
black = (0, 0, 0)




gameDisplay = pygame.surface.Surface((basic_map.get_width(), basic_map.get_height()))

clock = pygame.time.Clock()
amap = pickle.load(open(map_name + ".p", "rb"))

# print("walls:", amap.walls)

qt = amap.quadtree
guy = Player(300, 300, qt)
guard = Guard(80, 80, amap, (0, 0, 100), .7)
# print("wall count:", len(amap.walls))


found_points = qt.query(Rectangle(10, 30, 200, 200))

keystates = pgt.initialinput()

F = Point(100, 100)
T = Point(100, 100)
setting = "F"
can_click = True
path = astar(F, T, amap, gameDisplay)
# path = astar(Point(2375, 2395), Point(532, 2296), amap, gameDisplay)


class Camera:
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface


camera = Camera(0, 0, gameDisplay)

while True:
    # print("F:", F, "T:", T)
    camera.x = guy.x - 250
    camera.y = guy.y - 250

    mouse_p = pygame.mouse.get_pos()
    mouse_p = (mouse_p[0] + camera.x, mouse_p[1] + camera.y)
    mouse_b = pygame.mouse.get_pressed()
    if mouse_b[0] == 0:  # Letting go of the mouse allows it to be clicked again
        can_click = True

    if mouse_b[0] == 1 and can_click:
        if setting == "F":
            F.x, F.y = mouse_p
            setting = "T"
        else:
            T.x, T.y = mouse_p
            path = astar(F, T, amap, gameDisplay)
            setting = "F"

        can_click = False

    for event in pygame.event.get():
        keystates = pgt.basicinput(event, keystates)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # print(camera.x, camera.y)
    gameDisplay.blit(basic_map, (0, 0))
    guard.gotoo(Point(guy.x, guy.y))

    # qt.show(gameDisplay)
    guy.move(keystates)
    guy.pos_update()
    guard.update()
    guard.draw(gameDisplay)
    guy.draw(gameDisplay)

    color = (255, 0, 0) if amap.line_blocked(F, T) else (0, 0, 255)
    pygame.draw.line(gameDisplay, color, (F.x, F.y), (T.x, T.y), 3)

    for p in [F, T]:
        pygame.draw.circle(gameDisplay, (0, 0, 255), (p.x, p.y), 2)

    amap.draw_nodes(gameDisplay)
    if setting == "F":
        path.draw(gameDisplay)

    # print(camera.x, camera.y)
    Display.blit(gameDisplay, (0-camera.x, 0-camera.y))
    pgt.text(Display, (5, 5), str(int(clock.get_fps())), (100, 100, 100), 20, "right")
    pygame.display.update()
    clock.tick(60)
