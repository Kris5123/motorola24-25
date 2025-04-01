import pygame.transform
import math
from settings import tile_size,barrier,underway_barrier,screen_width,screen_height


accuracy = 2
barrier_size = [100,25] # NIE ZMIENIAĆ



def cross_product(ax, ay, bx, by):
    """Oblicza iloczyn wektorowy 2D."""
    return ax * by - ay * bx


def is_same_side(p1, p2, a, b):
    """Sprawdza, czy punkty p1 i p2 są po tej samej stronie odcinka AB."""
    ax, ay = a
    bx, by = b
    v1x, v1y = p1[0] - ax, p1[1] - ay
    v2x, v2y = p2[0] - ax, p2[1] - ay
    edge_x, edge_y = bx - ax, by - ay
    return cross_product(edge_x, edge_y, v1x, v1y) * cross_product(edge_x, edge_y, v2x, v2y) >= 0

# def is_point_inside_rectangle(p, rect):
#     """
#     Sprawdza, czy punkt (px, py) znajduje się wewnątrz prostokąta o danych wierzchołkach.
#
#     :param px, py: współrzędne punktu
#     :param rect: lista czterech wierzchołków [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
#     :return: True, jeśli punkt jest wewnątrz, False w przeciwnym razie
#     """
#
#
#
#     a, b, c, d = rect
#
#
#     # Punkt musi być po tej samej stronie wszystkich czterech boków prostokąta
#     return (is_same_side(p, a, b, c) and
#             is_same_side(p, b, c, d) and
#             is_same_side(p, c, d, a) and
#             is_same_side(p, d, a, b))

def angle_between(v1, v2):
    """Oblicza kąt między dwoma wektorami."""
    dot = v1[0] * v2[0] + v1[1] * v2[1]  # Iloczyn skalarny
    det = v1[0] * v2[1] - v1[1] * v2[0]  # Wyznacznik (iloczyn wektorowy 2D)
    return math.atan2(det, dot)  # Kąt w radianach

def is_point_inside_rectangle(p, rect):
    """Sprawdza, czy punkt P jest wewnątrz wielokąta (sumowanie kątów)."""
    px, py = p
    total_angle = 0

    for i in range(len(rect)):
        ax, ay = rect[i]
        bx, by = rect[(i + 1) % len(rect)]  # Kolejny wierzchołek

        v1 = (ax - px, ay - py)
        v2 = (bx - px, by - py)

        angle = angle_between(v1, v2)
        total_angle += angle

    return abs(total_angle) > 3.14  # Jeśli suma kątów ≈ 2π, punkt jest wewnątrz


# def rect_to_matrix(rect,matrix,value):
#
#
#     # for i in range(len(rect)):
#     #     rect[i][0] //= tile_size
#     #     rect[i][1] //= tile_size
#
#
#     min_x = int(min(p[0] for p in rect))
#     max_x = int(max(p[0] for p in rect))
#     min_y = int(min(p[1] for p in rect))
#     max_y = int(max(p[1] for p in rect))
#
#     print(rect)
#
#     for y in range(min_y, max_y + 1,tile_size):
#         for x in range(min_x, max_x + 1,tile_size):
#             if 0 <= x//tile_size < len(matrix) and 0 <= y//tile_size < len(matrix[0]):
#                 print([x,y], is_point_inside_rectangle([x,y],rect))
#
#                 if is_point_inside_rectangle([x, y], rect) and matrix[x//tile_size][y//tile_size] == 0:
#                     matrix[x//tile_size][y//tile_size] = value


def barrier_terrain_check(pos,angle,macierz,level=0):
    if level == 0:
        level = -1
    else:
        level = 1

    rect = [
            [pos[0] + math.cos(math.radians(angle + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle + 180 - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle + 180 - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle - 180 + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle - 180 + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5]

        ]

    points = 0
    no_points = 0
    min_x = int(min(p[0] for p in rect)) // tile_size
    max_x = int(max(p[0] for p in rect)) // tile_size
    min_y = int(min(p[1] for p in rect)) // tile_size
    max_y = int(max(p[1] for p in rect)) // tile_size

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            real_x = x * tile_size
            real_y = y * tile_size

            if is_point_inside_rectangle([real_x, real_y], rect):
                if 0 <= x < len(macierz) and 0 <= y < len(macierz[0]) and (macierz[x][y] == 0 or macierz[x][y] == level or macierz[x][y] == level*1.5):
                    points+=1
                else:
                    no_points+=1
    return points>(no_points*3)


def rect_to_matrix(rect, matrix, value):
    min_x = int(min(p[0] for p in rect)) // tile_size
    max_x = int(max(p[0] for p in rect)) // tile_size
    min_y = int(min(p[1] for p in rect)) // tile_size
    max_y = int(max(p[1] for p in rect)) // tile_size

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            real_x = x * tile_size
            real_y = y * tile_size

            if is_point_inside_rectangle([real_x, real_y], rect):
                if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] == 0:
                    matrix[x][y] = value






def clear_rect_from_matrix(rect,matrix,value):
    min_x = int(min(p[0] for p in rect)) // tile_size
    max_x = int(max(p[0] for p in rect)) // tile_size
    min_y = int(min(p[1] for p in rect)) // tile_size
    max_y = int(max(p[1] for p in rect)) // tile_size

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            real_x = x * tile_size
            real_y = y * tile_size

            if is_point_inside_rectangle([real_x, real_y], rect):
                if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] == value:
                    matrix[x][y] = 0


barrier_dur = 360 #6sekund

class Barrier:
    def __init__(self,pos,angle,macierz,value,level=0):
        self.level = level


        self.dur = barrier_dur

        self.value = value

        self.corners = [
            [pos[0] + math.cos(math.radians(angle + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle + 180 - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle + 180 - math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5],
            [pos[0] + math.cos(math.radians(angle - 180 + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5,
             pos[1] - math.sin(math.radians(angle - 180 + math.degrees(math.atan(barrier_size[0]/barrier_size[1])))) * 51.5]

        ]

        rect_to_matrix(self.corners,macierz,self.value)

        self.surf = pygame.Surface(barrier_size, pygame.SRCALPHA)
        self.surf.fill((0,0,0,255))
        self.surf = pygame.transform.rotate(self.surf, angle+90)
        self.rect = self.surf.get_rect(center=pos)

        # Draw rotated rectangle


    def update(self,screen,macierz):
        self.dur -= 1



        self.surf.set_alpha(int((self.dur / barrier_dur) * 205)+50)

        if self.dur <= 0:
            clear_rect_from_matrix(self.corners,macierz,self.value)
            return True




        return False


    def draw(self,screen):
        screen.blit(self.surf, self.rect.topleft)
        # for i in self.corners:
        #     pygame.draw.circle(screen,"blue",[i[0],i[1]],5)
        #
        # min_x = int(min(p[0] for p in self.corners))
        # max_x = int(max(p[0] for p in self.corners))
        # min_y = int(min(p[1] for p in self.corners))
        # max_y = int(max(p[1] for p in self.corners))
        #
        # pygame.draw.rect(screen,"red",([min_x,min_y],[max_x-min_x,max_y-min_y]),2)