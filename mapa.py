from settings import *
import pygame as pg

def mapping(image_name, w, h, tile_size=1):
    img = pg.transform.scale(pg.image.load(image_name),(w,h))
    a=[]
    for x in range(w // tile_size ):
        a.append([])
        for y in range(h // tile_size):
            color=img.get_at((x * tile_size, y * tile_size))[:3]
            if sum(color)<=100:
                a[-1].append(wall)
            elif color==(0,128,192):
                a[-1].append(ice)
            elif color==(255,255,51):
                a[-1].append(sand)
            elif color==(203,10,10):
                a[-1].append(sztutr)
            elif color==(255,0,0):
                a[-1].append(underway)
            else:
                a[-1].append(0)
    return a
# checkpoints