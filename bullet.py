import math as meth
from settings import *

import pygame


class Bullet:
    def __init__(self,pos,angle,speed):
        self.pos = pos
        self.angle = angle
        self.bounce = 0
        self.speed = speed





    def update(self,map):

        x = meth.sin(meth.radians(self.angle+90))
        y = meth.cos(meth.radians(self.angle+90))
        for n in range(int(self.speed)):
            self.pos[0] += x
            self.pos[1] += y
            if self.collide_map(self.pos,map):
                return 1
        return 0



    def collide_map(self, pos,map):
        if pos[0] < 0 or pos[0] >= screen_width or pos[1] < 0 or pos[1] >= screen_height:
            return True
        return map[int(pos[0]) // tile_size][int(pos[1]) // tile_size] == 1

    def draw(self,screen):

        pygame.draw.circle(screen,"pink",self.pos,5,0)



    def reflect(self, velocity, normal):
        """
        Oblicza wektor odbicia.
        :param velocity: Wektor prędkości początkowej (pygame.Vector2)
        :param normal: Wektor normalny do powierzchni (musi być jednostkowy!)
        :return: Wektor prędkości po odbiciu (pygame.Vector2)
        """
        velocity = pygame.Vector2(velocity)
        normal = pygame.Vector2(normal).normalize()  # Normalizacja wektora
        reflected = velocity - 2 * velocity.dot(normal) * normal
        reflected.x = round(reflected.x, 10)
        reflected.y = round(reflected.y, 10)
        return reflected

# # Przykład użycia:
# velocity = pygame.Vector2(1, 0)  # Prędkość początkowa
# normal = pygame.Vector2(2**(1/2)/2, 2**(1/2)/2)  # Normalna (np. ściana pozioma, więc normalna w górę)
#
# reflected_velocity = reflect(velocity, normal)
# # reflected_velocity.x = round(reflected_velocity.x, 10)  # Zaokrąglamy małe wartości do 0
# # reflected_velocity.y = round(reflected_velocity.y, 10)
# print("Wektor odbicia:", reflected_velocity)
