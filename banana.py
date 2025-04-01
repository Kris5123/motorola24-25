import pygame.transform
from settings import tile_size,wall

accuracy = 2
banana_size = [50,50]


def banana_terrain_check(pos, map):
    for x in range(banana_size[0]//accuracy):
        x-=banana_size[0]//2
        for y in range(banana_size[1]//accuracy):
            y-=banana_size[1]//2
            if 0>(pos[0]+x*accuracy)>1200 or 0>(pos[1]+y*accuracy)>800 or  map[(pos[0]+x*accuracy)//tile_size][(pos[1]+y*accuracy)//tile_size] == wall:
                return False

    return True


class Banana:
    def __init__(self,pos,level=0):
        self.level = level
        self.img = pygame.transform.scale(pygame.image.load('banana_peel.png'), banana_size)
        self.rect = self.img.get_rect()
        self.rect.center=pos




    def update(self,enemys):
        for enemy in enemys:
            for rect in enemy.rects:
                if self.rect.colliderect(rect) and enemy.level == self.level:
                    enemy.banana_effect=enemy.banana_effect_duration
                    return True

        return False


    def draw(self,screen):
        screen.blit(self.img,self.rect)