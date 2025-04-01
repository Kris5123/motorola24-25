import pygame as pg
import pygame.draw

from functions import *
from settings import *
import math as meth
import random

from datetime import datetime



keys_to_detect = [i for i in range(pygame.K_0, pygame.K_z + 1)]
special_keys =[
    pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK, pygame.K_TAB,pygame.K_SPACE
]
keys_to_detect.extend(special_keys)


def set_sfx_volume(volume):
    for sfx in sounds:
        sounds[sfx].set_volume(adjust_volume(volume))

def detect_keys(keys):
    for key in keys_to_detect:
        if keys[key]:
            return key
    return 0


def adjust_volume(volume):
    return volume ** 2


class Snowfall:
    def __init__(self, screen, image_path, num_flakes=100):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),[16,16])
        self.num_flakes = num_flakes
        self.flakes = self._generate_flakes()

    def _generate_flakes(self):
        flakes = []
        screen_width, screen_height = self.screen.get_size()
        for _ in range(self.num_flakes):
            x = random.randint(0, screen_width)
            y = random.randint(-screen_height, 0)
            speed = random.uniform(1, 3)  # Szybko?? opadania
            drift = random.uniform(-0.5, 0.5)  # Delikatny dryf w bok
            flakes.append([x, y, speed, drift])
        return flakes

    def update(self):
        screen_width, screen_height = self.screen.get_size()
        for flake in self.flakes:
            flake[1] += flake[2]  # Opadanie w d?
            flake[0] += flake[3]  # Dryf w bok

            # Resetuj p?atek, gdy spadnie poza ekran
            if flake[1] > screen_height:
                flake[0] = random.randint(0, screen_width)
                flake[1] = random.randint(-20, 0)
                flake[2] = random.uniform(1, 3)
                flake[3] = random.uniform(-0.5, 0.5)

    def draw(self):
        for flake in self.flakes:
            self.screen.blit(self.image, (flake[0], flake[1]))

class Keybind_button:
    def __init__(self,id,pos,width,color,f_color,txt_size,starting_txt):
        self.id = id
        self.rect = pygame.Rect(pos,[width,txt_size+5])
        h = pg.font.SysFont("Arial", txt_size).render(starting_txt, 1, color).get_height()
        self.label = Simple_label([pos[0]+width//2,pos[1]+h//2],width,starting_txt,txt_size,f_color,color,pos_type=1)
        self.is_clicked = False
        self.color = color

    def update(self,car,mp,mc,keys):

        # if self.is_clicked and mc[0]:
        #     self.label.update_text(pygame.key.name(car.keybinds[self.id]))
        if self.is_clicked == False and mc[0] and self.rect.collidepoint(mp):
            sounds['click'].play()
            self.is_clicked = True
            self.label.update_text("set a key")

        if self.is_clicked:
            sigma = detect_keys(keys)
            if sigma:
                car.keybinds[self.id] = sigma
                self.label.update_text(pygame.key.name(sigma))
                self.is_clicked = False

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        self.label.draw(screen)


class text_box():
    def __init__(self, p, width, height, size, text):
        self.active = False
        self.pos = p
        self.width = width
        self.height = size
        self.thick = 5
        self.text = text
        self.textr = [self.text]
        self.size = size
        self.ofs = self.thick / 2
        ofs = self.ofs
        self.font = pg.font.SysFont("ComicSans", size)
        self.rect = pg.Rect(p[0] - ofs, p[1] - ofs, self.width + ofs * 3, self.height + ofs * 3)

    def draw(self, screen):
        for n in range(len(self.textr)):
            a = text(self.font, self.textr[n], (255, 255, 255))
            screen.blit(a[0], (self.pos[0] + self.ofs * 2, self.pos[1] + self.size * n))
        if self.active:
            pg.draw.rect(screen, (255, 125, 0), self.rect, self.thick)
        else:
            pg.draw.rect(screen, (125, 125, 0), self.rect, self.thick)

    def update_size(self):
        self.textr = []
        pointer = 0
        l = len(self.text)
        self.textr = text_down(self.text, self.font, self.width)
        b = len(self.textr)
        self.height = b * self.size
        self.rect.height = self.height + self.ofs * 5


class cotton_picker():
    def __init__(self, list, pos, width, size, border_size,font=0):
        self.border = border_size
        self.list = list
        self.pos = pos
        self.width = width
        if font:
            self.font=font
        else:
            self.font = pg.font.SysFont("TimesNewRoman", size)
        self.surfaces = []
        self.rects = []
        self.size = size
        y = pos[1]
        self.ofs = 6
        self.active = 0
        for n in list:
            txt=text(self.font,n,(0,0,0))
            self.rects.append(pg.Rect(self.pos[0],y,width,txt[2]+self.border*2))
            self.surfaces.append(Simple_label(self.rects[-1].center,200,n,0,(255,255,255),pos_type=1,font=self.font))
            y = self.rects[-1].bottom
        self.pick = 0
        self.pressed=0
    def update_x(self,x):
        self.pos=x,self.pos[1]
        for j,i in enumerate(self.rects):
            i.x=x
            self.surfaces[j].update_x(i.centerx)
    def draw(self, screen):
        color = (50, 50, 50)
        if self.active:
            for n in range(len(self.rects)):
                color = (50, 50, 50)
                if n == self.pick:
                    color = (255, 125, 0)
                pg.draw.rect(screen, (150,150,150), self.rects[n])
                pg.draw.rect(screen, color, self.rects[n], self.border)
                self.surfaces[n].draw(screen)


        else:
            rect=pg.Rect((self.pos), (self.rects[self.pick].size))
            pg.draw.rect(screen, (150,150,150), rect)
            pg.draw.rect(screen, color,rect,self.border)
            self.surfaces[self.pick].rect.center=rect.center
            self.surfaces[self.pick].draw(screen)
            self.surfaces[self.pick].rect.center=self.rects[self.pick].center


    def update(self, mp,mc):
        if not mc[0]:
            if self.pressed:
                if self.active:
                    self.active=0
                    for n in range(len(self.list)):
                        if self.rects[n].collidepoint(mp):
                            self.pick = n
                            return True
                else:
                    self.active = self.rects[self.pick].collidepoint((mp[0], mp[1] + self.rects[self.pick].y - self.pos[1]))
        self.pressed=mc[0]
        return False

class slider():
    def __init__(self, pos, width, height, point_radius, colors, a=1, b=0, intiger=0, vertical=0,show_value=0):
        self.srect = pg.Rect(pos, (width, height))
        self.pr = point_radius
        self.colors = colors
        self.v = vertical
        self.ppos = [self.srect.center[0], self.srect.center[1]]
        self.value = 30
        self.pos = pos
        self.size = (width, height)
        self.font = pg.font.SysFont("Arial", self.pr)
        self.a = a
        self.b = b
        self.i = intiger
        self.show_val=show_value
        self.active=0

    def draw(self, screen):
        pg.draw.rect(screen, self.colors[0], self.srect)
        pg.draw.circle(screen, self.colors[1], self.ppos, self.pr)
        if self.active and self.show_val:
            self.show_value(screen)
    def update(self,mp,mc):
        self.active=0
        if mc[0]:
            if self.move(mp):
                self.active=1


    def move(self, mp):
        if self.pos[self.v] + self.size[self.v] > mp[self.v] > self.pos[self.v] and (mp[0] - self.ppos[0]) ** 2 + (
                mp[1] - self.ppos[1]) ** 2 < self.pr ** 2:
            self.ppos[self.v] = mp[self.v]
            self.value = (mp[self.v] - self.pos[self.v]) / self.size[self.v]
            self.value *= self.a
            self.value += self.b
            if self.i:
                self.value = int(self.value)
            return True
        return False

    def show_value(self, screen):
        sv = int(self.value * 1000) / 1000
        txt = text(self.font, str(sv), (0))
        w = txt[1]
        rect = pg.Rect(self.ppos[0] - w / 2, self.ppos[1] - self.pr * 2, w, self.pr)
        pg.draw.rect(screen, (255, 255, 255), rect)
        screen.blit(txt[0], rect)


gui_font = pg.font.Font(None,30)
class Button:
    def __init__(self,text,width,height,pos,elevation,font_size,color_1,color_2,font_color=(255,255,255),font="Arial",pos_type=0):
        if pos_type:
            pos=pos[0]-width/2,pos[1]-height/2
        self.pressed = False
        self.elevation = elevation
        self.swap = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pg.Rect(pos,(width,height))
        self.top_color = color_1
        self.size=font_size

        self.bottom_rect = pg.Rect(pos,(width,height))
        self.bottom_color = color_2
        self.texts=text_down(text,pg.font.SysFont(font,font_size),width)
        self.surfaces = [pg.font.SysFont(font,font_size).render(i,True,font_color) for i in self.texts]
        self.rects = [i.get_rect() for i in self.surfaces]
        self.l=len(self.surfaces)
        self.set_labels()
        self.do=0
    def set_labels(self):
        for n in range(self.l):
            self.rects[n].centerx=self.top_rect.centerx
            self.rects[n].centery=self.top_rect.centery-(self.size)*(self.l-1)//2+n*self.size

    def draw(self,screen):
        self.top_rect.y = self.original_y_pos - self.swap
        self.set_labels()

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.swap

        pg.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pg.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        for i,n in enumerate(self.rects):
            screen.blit(self.surfaces[i], n)

    def check_click(self,mp,mc):
        self.do=0
        if self.top_rect.collidepoint(mp):
            if mc[0]:
                self.swap = 0
                self.pressed = True
            else:
                self.swap = self.elevation
                if self.pressed == True:
                    sounds['click'].play()
                    self.do=1
                    self.pressed = False
        else:
            self.swap = self.elevation
            self.pressed = False


class label():
    def __init__(self, pos, width, txt, size, font_color, bgcolor=0):
        self.font = pg.font.SysFont("Arial", size)
        self.labels = text_down(txt, self.font, width)
        self.surfaces = []
        self.bgcolor = bgcolor
        self.size = size
        maxx = 0
        for n in self.labels:
            self.surfaces.append(text(self.font, n, font_color))
            maxx = max(self.surfaces[-1][1], maxx)

        self.rect = pg.Rect(pos, (maxx, size * len(self.surfaces)))

    def draw(self, screen):
        if self.bgcolor:
            pg.draw.rect(screen, self.bgcolor, self.rect)
        for n in range(len(self.surfaces)):
            screen.blit(self.surfaces[n][0], (self.rect.x, self.rect.y + self.size * n))
class Simple_label():
    def __init__(self, pos, width, txt, size, font_color, bgcolor=0,pos_type=0,font=0):
        if font:
            self.font=font
        else:
            self.font = pg.font.SysFont("Arial", size)

        self.label = text( self.font,txt, font_color)
        self.color=font_color
        self.bgcolor = bgcolor
        self.pos_type=pos_type
        if pos_type==1:
            self.rect=pg.Rect(pos[0]-self.label[1]//2,pos[1]-self.label[2]//2, self.label[1], self.label[2])
        elif pos_type==2:
            self.rect=pg.Rect(pos[0],pos[1]-self.label[2]//2, self.label[1], self.label[2])
        else:
            self.rect=pg.Rect(pos,(self.label[1],size))
    def draw(self, screen):
        if self.bgcolor:
            pg.draw.rect(screen, self.bgcolor, self.rect)
        screen.blit(self.label[0],self.rect)
    def update_text(self,txt):
        self.label = text(self.font,txt, self.color)
        if self.pos_type==1:
            r=self.label[0].get_rect()
            r.center=self.rect.center
            self.rect=r
            del r
        elif self.pos_type==2:
            r=self.label[0].get_rect()
            r.centery=self.rect.centery
            r.x=self.rect.x
            self.rect=r
            del r
    def update_x(self,x):
        if self.pos_type:
            self.rect.centerx=x
        else:
            self.rect.x=x
    def update_y(self,y):
        if self.pos_type:
            self.rect.centery=y
        else:
            self.rect.y=y


class Simple_list:
    def __init__(self, pos, width, texts, size, font_color=0,font_colors=0, bgcolor=0, pos_type=0,gap=0):
        self.size = len(texts)
        if not font_colors:
            if font_color:
                font_colors=[font_color for i in range(self.size)]
            else:
                font_colors = [(255,255,255) for i in range(self.size)]
        self.labels = [Simple_label([pos[0], pos[1] + (size+gap) * i], width, texts[i], size, font_colors[i], bgcolor, pos_type)
                       for i in range(self.size)]
        self.info = [pos, width, size, font_colors, bgcolor, pos_type]

    def draw(self, screen):
        for i in self.labels:
            i.draw(screen)

    def update_text(self, txt, index):
        self.labels[index].update_text(txt)

    def add(self, txt,color=(255,0,0)):
        self.info[3].append(color)
        self.labels.append(Simple_label([self.info[0][0], self.info[0][1] + self.info[2] * self.size], self.info[1], txt
                                        , self.info[2], color, self.info[4], self.info[5]))
        self.size += 1

    def insert(self, txt, index):
        pass

class Particle:
    def __init__(self, x, y, opacity, colors, angle,speed,radius=5):
        self.x = x
        self.y = y
        self.opacity = opacity
        self.colors = colors
        self.angle = angle
        self.speed = speed
        self.parpop=False
        self.radius=radius

    def fading(self):
        self.colors = (int(max(0, self.colors[0] - self.opacity)), int(max(0, self.colors[1] - self.opacity)),
                       int(max(0, self.colors[2] - self.opacity)))

    def move(self):
        self.x += meth.sin(self.angle) * self.speed
        self.y += meth.cos(self.angle) * self.speed

    def draw(self, scene):
        if self.colors[0] > 0 or self.colors[1] > 0 or self.colors[2] > 0:
            pg.draw.circle(scene, (self.colors[0], self.colors[1], self.colors[2], self.opacity), (self.x, self.y),
                               self.radius)
        else:
            self.parpop = True


class Slots:
    def __init__(self,x,y,slot_w,slot_h,items,slots,ods,gap=10):
        self.x=x
        self.y=y
        self.w=slot_w
        self.h=slot_h
        self.gap=gap
        self.items=items
        self.l=len(items)
        self.slots_quantity=slots
        self.rolls=0
        self.roll_delay=5
        self.items_q = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0
        }
        for i in items:
            self.items_q[i.rarity]+=1
        self.rarities={0:"common",
            1:"uncommon",
            2:"rare",
            3:"epic",
            4:"legendary"}
        print(self.items_q)
        s=sum(ods)
        self.ods=[meth.ceil(100*i/s) for i in ods]
        print(len(ods))
        self.shuffle()
    def shuffle(self):
        self.slots=[]
        rolled=set()
        cuantity=self.items_q.copy()
        for i in range(self.slots_quantity):
            rarity=random.randint(0,100)
            s=0
            for j in range(len(self.ods)):
                s+=self.ods[j]
                if s>rarity:
                    break
            rarity=self.rarities[j]
            cuantity[rarity]-=1
            item=random.randint(0,cuantity[rarity])
            for j in self.items:
                if j.rarity==rarity and j.id not in rolled:
                    if item==0 :
                        self.slots.append(j)
                        rolled.add(j.id)
                        print(j.id)
                        break
                    else:
                        item-=1
        self.set_pos()
    def sell(self,mc,mp):
        if self.rolls==0 and mc[0]:
            for i in self.slots:
                if i.rect.collidepoint(mp):
                    # self.roll(10)
                    return i.copy()
        return 0
    def update(self):
        if self.rolls>0:
            if self.roll_delay:
                self.roll_delay-=1
            else:
                self.rolls-=1
                self.shuffle()
                self.roll_delay=5
    def roll(self,rolls):
        self.rolls=rolls
        sounds['slots'].play()
    def set_pos(self):
        j=0
        for i in self.slots:
            i.rect.y=self.y
            i.rect.x=self.x+j*(self.w+self.gap)
            j+=1
    def draw(self,screen,mp):
        s = 0
        for i in self.slots:
            r = i.draw(screen,mp)
            if r:
                s = r
        if s:
            screen.blit(s[0],s[1])
class Map_snippets:
    def __init__(self,x,y,width,height,images,laps,gold_income,gem_income,unlocked_maps,lock_image,gap=10,border=7,border_color=(200,200,0),shown=2):
        self.x=x
        self.y=y
        self.images=[pg.transform.scale(pg.image.load(i),(width,height)) for i in images]
        self.laps = laps
        self.l=len(images)
        self.gap=gap
        self.border=border
        self.border_color=border_color
        self.rects=[pg.Rect(x+(gap+width)*i,y,width,height) for i in range(shown)]
        self.shown=shown
        self.current=0
        bw=100
        bh=100
        self.left_button=Button("<",bw,bh,[x-bw-gap,y+height/2-bh/2],0,50,(0,50,125),(0,0,0),(255,255,255))
        self.right_button=Button(">",bw,bh,[1200-bw,y+height/2-bh/2],0,50,(0,50,125),(0,0,0),(255,255,255))
        self.lock_img=lock_image
        self.lock_rect=lock_image.get_rect()
        self.unlocked_maps=unlocked_maps
        self.darking_surface=pg.surface.Surface((width,height),pg.SRCALPHA)
        self.darking_surface.fill((0,0,0,200))
        self.original_unlocks=unlocked_maps[:]
        self.gold_income=gold_income
        self.gem_income=gem_income
        self.best_times=[-1 for i in range(self.l)]
        self.best_laps=[-1 for i in range(self.l)]
        self.names=[Simple_label((screen_width//2,200),0,f"{images[i][:-4]}",80,(255,255,255),pos_type=1) for i in range(self.l)]
        self.stats=[Simple_list((280,600),300,[f"Laps: {laps[i]}",f"Best time: --",f"Best lap: --"],50,pos_type=1,font_color=(255,255,255),gap=15) for i in range(self.l)]
        self.requirments=[Simple_list((screen_width//2,600),300,["To unlock this map","you need to get the first place",f"on the {images[i-1][:-4]}"],50,pos_type=1,font_color=(255,0,0)) for i in range(1,self.l)]
        #To unlock this map you need to get the first place on the map
    def custom(self):
        self.unlocked_maps=[1 for i in range(self.l)]

        self.gold=[Simple_list((600,600),300,[f"1st: 0$",f"2nd: 0$",f"3rd: 0"],50,pos_type=1,font_color=(255,215,0),gap=15) for i in range(self.l)]
        self.gems=[Simple_list((920,600),300,[f"1st: 0 gems",f"2nd: 0 gems",f"3rd: 0 gems"],50,pos_type=1,font_color=(185,242,255),gap=15) for i in range(self.l)]

    def update_best_time(self,time,map):
        self.stats[map].labels[1].update_text(f"Best time: {time}")
    def update_best_lap(self,time,map):
        self.stats[map].labels[2].update_text(f"Best lap: {time}")

    def campaign(self):
        self.unlocked_maps=self.original_unlocks.copy()
        self.gold=[Simple_list((600,600),300,[f"1st: {self.gold_income[i][0]}$",f"2nd: {self.gold_income[i][1]}$",f"3rd: {self.gold_income[i][2]}$"],50,pos_type=1,font_color=(255,215,0),gap=15) for i in range(self.l)]
        self.gems=[Simple_list((920,600),300,[f"1st: {self.gem_income[i][0]} gems",f"2nd: {self.gem_income[i][1]} gems",f"3rd: {self.gem_income[i][2]} gems"],50,pos_type=1,font_color=(185,242,255),gap=15) for i in range(self.l)]
    def update_records(self,laps,map):
        time=sum(laps)
        if self.best_times[map]>time or self.best_times[map]==-1:
            self.best_times[map]=time
            self.update_best_time(time,map)
        for i in laps:
            if self.best_laps[map]>i or self.best_laps[map]==-1:
                self.best_laps[map]=i
                self.update_best_lap(i,map)
    def unlock(self,i):
        self.unlocked_maps[i]=1
        self.original_unlocks[i]=1
    def update(self,mp,mc):
        self.left_button.check_click(mp,mc)
        self.right_button.check_click(mp,mc)
        if self.current>0 and self.left_button.do:
            self.current-=1
        elif self.current<self.l-2 and self.right_button.do:
            self.current+=1
        if mc[0]:
            for j,i in enumerate(self.rects):
                if self.unlocked_maps[j+self.current]:
                    if i.collidepoint(mp):
                        return j+self.current
        return -1

    def draw(self,screen,mp):
        for i in range(self.shown):
            if self.rects[i].collidepoint(mp):
                pg.draw.rect(screen,self.border_color,pg.Rect(self.rects[i].x-self.border,self.rects[i].y-self.border,self.rects[i].w+self.border*2,self.rects[i].h+self.border*2),
                             width=self.border,border_radius=self.border*1)
                if not self.unlocked_maps[i+self.current]:
                    self.requirments[i+self.current-1].draw(screen)
                else:
                    self.stats[i+self.current].draw(screen)
                    self.gold[i+self.current].draw(screen)
                    self.gems[i+self.current].draw(screen)

                self.names[i+self.current].draw(screen)

            screen.blit(self.images[i+self.current],self.rects[i])
            if not self.unlocked_maps[i+self.current]:
                screen.blit(self.darking_surface,self.rects[i])
                self.lock_rect.center=self.rects[i].center
                screen.blit(self.lock_img,self.lock_rect)

        self.left_button.draw(screen)
        self.right_button.draw(screen)

class Bullet:
    def __init__(self,x,y,angle,speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.vect = pg.math.Vector2(meth.sin(meth.radians(self.angle+90)) * self.speed,meth.cos(meth.radians(self.angle+90)) * self.speed)
        self.w=5
        # self.bullet_part=[]
        # for i in range(self.w):
        #     for j in range(self.w):
        #         self.bullet_part.append(Bullets_part(self.x-self.w//2+i,self.y-self.w//2+j,self.vect))
        self.lifetime = 500
        self.bouncy_cheeks = 6
        self.pop=0
    def collide_map(self,pos):
        if pos[0]<0 or pos[0]>=screen_width or pos[1]<0 or pos[1]>=screen_height:
            return True
        return map[int(pos[0])//tile_size][int(pos[1])//tile_size]==1

    def move(self):
        if self.collide_map((self.x + self.vect.x, self.y)):
            self.bouncy_cheeks-=1
            self.vect.x*=-1
        self.x += self.vect.x
        if self.collide_map((self.x , self.y+ self.vect.y)):
            self.bouncy_cheeks-=1
            self.vect.y *= -1
        self.y += self.vect.y
        self.lifetime-=1
        if self.bouncy_cheeks<=0 or self.lifetime<=0:
            self.pop=1
    def draw(self,screen):
        pg.draw.circle(screen,(0,255,0),(self.x,self.y),5)
class Check_points:
    def __init__(self,check_points):
        self.check_points=check_points
        self.len=len(check_points)
    def check(self,rekt,check_point):
        return self.check_points[check_point].colliderect(rekt)
    def draw(self,screen):
        for i in self.check_points:
            pygame.draw.rect(screen,(0,255,0),i)
class Under_points:
    def __init__(self,under_points,control_points):
        self.under_points=under_points
        self.control_points=control_points
    def check(self,rekt):
        for n in self.control_points:
            if n.colliderect(rekt):
                return 0
        for n in self.under_points:
            if n.colliderect(rekt):
                return 1
        return -1
    def draw(self,screen):
        for i in self.under_points:
            pygame.draw.rect(screen,(255,0,0),i)
        for i in self.control_points:
            pygame.draw.rect(screen,(0,0,255),i)
class Pause_screen:
    def __init__(self,x,y,width,height,color,mv,sfxv):
        self.rect=pg.Rect(x,y,width,height)
        self.color=color
        self.active=False
        self.color=color
        self.check=1
        self.surface=pg.surface.Surface((width,height), pygame.SRCALPHA)
        self.surface.fill((0,0,0,0))
        self.surface.convert_alpha()
        self.musik_slider=slider((x+150,230+y),150,15,20,[(125,125,125),(0,0,50)],60,intiger=1,show_value=1)

        self.musik_slider.value = mv * self.musik_slider.a
        self.musik_slider.ppos = [self.musik_slider.srect.x + self.musik_slider.value / self.musik_slider.a * self.musik_slider.srect.width,self.musik_slider.srect.centery]

        self.SFX_slider=slider((x+width-300,230+y),150,15,20,[(125,125,125),(0,0,50)],60,intiger=1,show_value=1)

        self.SFX_slider.value = sfxv * self.SFX_slider.a
        self.SFX_slider.ppos = [self.SFX_slider.srect.x + self.SFX_slider.value / self.SFX_slider.a * self.SFX_slider.srect.width,self.SFX_slider.srect.centery]

        pg.draw.rect(self.surface,self.color,pg.Rect(0,0,width,height),border_radius=self.rect.height//10)
        [i.draw(self.surface) for i in [Simple_label((width//2,50),300,"Paused ||",80,(255,255,255),pos_type=1),
                                        Simple_label((width//4,150),300,"Musik",50,(255,255,255),pos_type=1),
                                        Simple_label((width//4*3,150),300,"SFX",50,(255,255,255),pos_type=1)]]
        self.quit_button=Button("Quit",230,100,(x+50,y+height-200),10,50,(0,0,200),(0,0,150))
        self.console_button=Button("Open;console",230,100,(x+width-280,y+height-200),10,50,(0,0,200),(0,0,150))
        self.controls_button = Button("Adjust;controls", 230, 100, ((x + width)//2-40, y + height - 200), 10, 50, (0, 0, 200),(0, 0, 150))

    def draw(self,screen):
        if self.active:
            bg=pg.surface.Surface((screen_width,screen_height), pygame.SRCALPHA)
            bg.fill((0,0,0,200))
            screen.blit(bg,(0,0))
            screen.blit(self.surface,self.rect)
            self.musik_slider.draw(screen)
            self.SFX_slider.draw(screen)
            self.quit_button.draw(screen)
            self.console_button.draw(screen)
            self.controls_button.draw(screen)
            del bg
    def update(self,keys,mp,mc):
        if keys[pg.K_ESCAPE]:
            if self.check:
                self.check=0
                self.active=self.active==False
        else:
            self.check=1
        if self.active:
            self.musik_slider.update(mp,mc)
            self.SFX_slider.update(mp,mc)
            self.quit_button.check_click(mp,mc)
            if self.quit_button.do:
                self.active=0
                return 1
            self.console_button.check_click(mp,mc)
            if self.console_button.do:
                self.active=0
                return 2
            self.controls_button.check_click(mp, mc)
            if self.controls_button.do:
                self.active = 0
                return 3
        return 0

class Settings_screen:
    def __init__(self,x,y,width,height,color,mv,sfxv):
        self.rect=pg.Rect(x,y,width,height)
        self.color=color
        self.active=False
        self.color=color
        self.check=1
        self.surface=pg.surface.Surface((width,height), pygame.SRCALPHA)
        self.surface.fill((0,0,0,0))
        self.surface.convert_alpha()
        self.musik_slider=slider((x+150,230+y),150,15,20,[(125,125,125),(0,0,50)],60,intiger=1,show_value=1)

        self.musik_slider.value = mv*self.musik_slider.a
        self.musik_slider.ppos = [self.musik_slider.srect.x + self.musik_slider.value/self.musik_slider.a * self.musik_slider.srect.width,self.musik_slider.srect.centery]

        self.SFX_slider=slider((x+width-300,230+y),150,15,20,[(125,125,125),(0,0,50)],60,intiger=1,show_value=1)

        self.SFX_slider.value = sfxv * self.SFX_slider.a
        self.SFX_slider.ppos = [self.SFX_slider.srect.x + self.SFX_slider.value / self.SFX_slider.a * self.SFX_slider.srect.width,self.SFX_slider.srect.centery]

        pg.draw.rect(self.surface,self.color,pg.Rect(0,0,width,height),border_radius=self.rect.height//10)
        [i.draw(self.surface) for i in [Simple_label((width//2,50),300,"Settings",80,(255,255,255),pos_type=1),
                                        Simple_label((width//4,150),300,"Musik",50,(255,255,255),pos_type=1),
                                        Simple_label((width//4*3,150),300,"SFX",50,(255,255,255),pos_type=1)]]
        self.console_button=Button("Open;console",230,100,(x+width-280,y+height-200),10,50,(0,0,200),(0,0,150))
        self.controls_button = Button("Adjust;controls", 230, 100, (x + 280, y + height - 200), 10, 50, (0, 0, 200),(0, 0, 150))

    def draw(self,screen):
        if self.active:
            bg=pg.surface.Surface((screen_width,screen_height), pygame.SRCALPHA)
            bg.fill((0,0,0,200))
            screen.blit(bg,(0,0))
            screen.blit(self.surface,self.rect)
            self.musik_slider.draw(screen)
            self.SFX_slider.draw(screen)
            self.console_button.draw(screen)
            self.controls_button.draw(screen)
            del bg
    def update(self,keys,mp,mc):
        if keys[pg.K_ESCAPE]:
            if self.check:
                self.check=0
                self.active=self.active==False
        else:
            self.check=1
        if self.active:
            self.musik_slider.update(mp,mc)
            self.SFX_slider.update(mp,mc)
            self.console_button.check_click(mp,mc)
            if self.console_button.do:
                self.active=0
                return 2
            self.controls_button.check_click(mp, mc)
            if self.controls_button.do:
                self.active = 0
                return 3
        return 0
class Simple_text_box:
    def __init__(self,x,y,w,h,font,size,speed=100,enter_clear=1,border=5,pointer_w=7,int_=0):
        self.rect=pg.Rect(x,y,w,h)
        self.pointer=0
        self.text=""
        self.font=font
        self.size=size
        self.pointer_rect=pg.Rect(x+5,y+5,pointer_w,h-10)
        self.active=0
        self.surface=pg.surface.Surface((0,0))
        self.keys_pressed=[0 for i in range(50)]
        self.l=0
        self.speed=speed
        self.cur=speed
        self.enter_clear=enter_clear
        self.border=border
        self.int=int_
    def move_x(self,x):
        self.rect.x=x
        self.move_pointer()
    def draw(self,screen):
        pg.draw.rect(screen,(125,125,125),self.rect)
        if self.active:
            pg.draw.rect(screen,(150,50,0),self.rect,self.border)
        else:
            pg.draw.rect(screen,(0,0,0),self.rect,self.border)

        screen.blit(self.surface,(self.rect.x+5,self.rect.y))
        if self.active and self.cur>self.speed//2:
            pg.draw.rect(screen,(255,255,255),self.pointer_rect)
        self.cur-=1
        self.cur%=self.speed
    def update_text(self,char):
        self.cur=self.speed
        self.l+=1
        self.text = self.text[:self.pointer]+char+self.text[self.pointer:]
        self.pointer+=1
        self.surface=self.font.render(self.text,True,(0,0,0))
        self.move_pointer()
    def move_pointer(self):
        self.cur=self.speed
        self.pointer_rect.x=text(self.font,self.text[:self.pointer],(0,0,0))[1]+self.rect.x+5
    def delete_char(self):
        self.cur=self.speed
        self.l-=1
        self.text = self.text[:self.pointer-1]+self.text[self.pointer:]
        self.pointer-=1
        self.surface=self.font.render(self.text,True,(0,0,0))
        self.move_pointer()

    def update(self,mp,mc,keys):
        if mc[0]:
            if self.rect.collidepoint(mp):
                self.active=1
            else:
                self.active=0

        if self.active:
            if keys[pg.K_RETURN]:
                if self.enter_clear:
                    txt=self.text
                    self.text=""
                    self.update_text("")
                    self.pointer=0
                    return txt
                else:
                    self.active=0
                    return
            if keys[pg.K_LSHIFT]:
                #print(ord('a')-ord('A'))
                shift=32
            else:
                shift=0
            if self.pointer>0 and keys[pg.K_LEFT]:
                if not self.keys_pressed[37]:
                    self.pointer-=1
                    self.move_pointer()
                    self.keys_pressed[37]=1
            else:
                self.keys_pressed[37]=0

            if self.pointer!=self.l and keys[pg.K_RIGHT]:
                if not self.keys_pressed[38]:
                    self.pointer+=1
                    self.move_pointer()
                    self.keys_pressed[38]=1
            else:
                self.keys_pressed[38]=0

            if self.pointer!=0 and keys[pg.K_BACKSPACE]:
                if not self.keys_pressed[39]:
                    self.delete_char()
                    self.keys_pressed[39]=1
            else:
                self.keys_pressed[39]=0
            w=self.surface.get_width()
            #a-z
            if not self.int:
                for i in range(97,123):
                    if keys[i]:
                        if not self.keys_pressed[i-96]:
                            if w+text(self.font,chr(ord(pygame.key.name(i))-shift),(0,0,0))[1]<self.rect.width-self.border*2:
                                self.update_text(chr(ord(pygame.key.name(i))-shift))
                                self.keys_pressed[i-96]=1
                                w=self.surface.get_width()
                            else:
                                return 0
                    else:
                        self.keys_pressed[i-96]=0
                if keys[pg.K_SPACE]:
                    if not self.keys_pressed[0]:
                        if w+text(self.font," ",(0,0,0))[1]<self.rect.width-self.border*2:
                            self.update_text(" ")
                            self.keys_pressed[0]=1
                            w=self.surface.get_width()
                        else:
                            return 0
                else:
                    self.keys_pressed[0]=0
            #0-9
            for i in range(48,58):
                if keys[i]:
                    if not self.keys_pressed[i-21]:
                        if w+text(self.font,pygame.key.name(i),(0,0,0))[1]<self.rect.width-self.border*2:
                            self.update_text(pygame.key.name(i))
                            self.keys_pressed[i-21]=1
                            w=self.surface.get_width()
                        else:
                            return 0
                else:
                    self.keys_pressed[i-21]=0
        return 0






class Console:
    def __init__(self,x,y,width,height,font_size,slider_width,slider_height,font="Arial"):
        self.rect=pg.Rect(x,y,width,height)
        self.font=pg.font.SysFont(font,font_size)
        self.texts=[]
        self.text_box=Simple_text_box(x,y+height-height//10,width,height//10,self.font,font_size)
        self.active=0
        self.surfaces=[]
        self.user_surface=text(self.font,"User: ",(255,0,0))
        self.system_surface=text(self.font,"System: ",(0,0,255))
        self.l=0
        self.surface=pg.surface.Surface(self.rect.size)
        self.slide_y=0
        self.slider=pg.Rect(x+width,y,slider_width,height-self.text_box.rect.h)
        self.slider_pressed=0
        self.unlock_everything = False
        self.give_gold = False
        self.give_gems = False
        self.show_fps=False


    def draw(self,screen):
        if self.active:
            bg=pg.surface.Surface((screen_width,screen_height), pygame.SRCALPHA)
            bg.fill((0,0,0,230))
            screen.blit(bg,(0,0))
            self.surface.fill((100,100,100))
            y=self.rect.h-self.text_box.rect.h-self.user_surface[2]+self.slide_y
            for i in range(self.l-1,-1,-1):
                x=0
                if self.texts[i][0]==0:
                    self.surface.blit(self.user_surface[0],(x,y))
                    x+=self.user_surface[1]
                elif self.texts[i][0]==1:
                    self.surface.blit(self.system_surface[0],(x,y))
                    x+=self.system_surface[1]
                self.surface.blit(self.surfaces[i][0],(x,y))
                y-=self.user_surface[2]
            screen.blit(self.surface,self.rect)
            self.text_box.draw(screen)
            pg.draw.rect(screen,(200,200,200),self.slider)
            del bg
    def add_user_text(self,txt):
        a=text_down(txt,self.font, self.rect.w-self.user_surface[1])
        for i in range(len(a)):
            self.l+=1
            self.texts.append([0 if i==0 else 2,txt])
            self.surfaces.append(text(self.font,a[i],(0,0,0)))

    def add_system_text(self,txt):
        a=text_down(txt,self.font, self.rect.w-self.system_surface[1])
        for i in range(len(a)):
            self.l+=1
            self.texts.append([1 if i==0 else 2,txt])
            self.surfaces.append(text(self.font,a[i],(0,0,0)))
        self.update_sliders_height()
    def analyse_input(self,txt,players):
        if txt=="unlock everything" or txt=="unlockeverything" or txt=="unlock_everything":
            self.add_system_text("Everything unlocked")
            self.unlock_everything = True
        elif txt=="give gold" or txt=="givegold" or txt=="give_gold":
            self.add_system_text("Gold given")
            self.give_gold = True
        elif txt=="give gems" or txt=="givegems" or txt=="give_gems":
            self.add_system_text("Gems given")
            self.give_gems = True

        elif txt=="players info":
            a=""
            for i in players:
              a+=f";Car id: {i.id};x: {i.x}, y: {i.y};Angle: {i.angle};Type: {i.type}"
            self.add_system_text(a)
        elif txt=="clear":
            self.clear()
        elif txt=="show fps":
            self.show_fps=True
        elif txt=="hide fps":
            self.show_fps=False

        else:
            self.add_system_text("Command not recognized")

    def clear(self):
        self.texts = []
        self.surfaces = []
        self.l = 0
    def update_sliders_height(self):
        self.slider.height = min((self.rect.h - self.text_box.rect.h) ** 2 / max(self.l * self.user_surface[2], 1),
                                 self.rect.h - self.text_box.rect.h)
        self.slider.bottom = self.rect.bottom - self.text_box.rect.h
        self.slide_y = 0
    def update(self,mp,mc,keys,players):
        if self.unlock_everything:
            self.unlock_everything = False
        elif self.give_gold:
            self.give_gold = False
        elif self.give_gems:
            self.give_gems = False
        if self.active:
            txt = self.text_box.update(mp,mc,keys)
            if txt:
                self.add_user_text(txt)
                self.analyse_input(txt,players)


                self.slider.height=min((self.rect.h-self.text_box.rect.h)**2/max(self.l*self.user_surface[2],1),self.rect.h-self.text_box.rect.h)
                self.slider.bottom=self.rect.bottom-self.text_box.rect.h
                self.slide_y=0


            if mc[0]:
                if self.slider.collidepoint(mp):
                    self.slider_pressed=1
            else:
                self.slider_pressed=0
            if self.slider_pressed:
                if mp[1]+self.slider.height//2<=self.rect.bottom-self.text_box.rect.h:
                    if mp[1]-self.slider.height//2>=self.rect.y:
                        self.slider.centery=mp[1]
                    else:
                        self.slider.y=self.rect.y
                else:
                    self.slider.bottom=self.rect.bottom-self.text_box.rect.h
                self.slide_y=(self.rect.bottom-self.text_box.rect.h-self.slider.bottom)/(self.rect.h-self.text_box.rect.h)*max(self.l*self.user_surface[2],1)
class Player_slots:
    def __init__(self,x,y,slots,starting_items):
        self.x=x
        self.y=y
        self.w=450
        self.h=750
        self.gap=60
        self.l=slots
        self.slots=[Player_slot(x+i*(self.gap+self.w),y,self.w,self.h,f"Car {i+1}",starting_items) for i in range(self.l)]
        self.pick=0
        self.left_button=Button("<",70,70,(10,350),0,70,(0,50,125),(0,0,0),(255,255,255))
        self.right_button=Button(">",70,70,(1120,350),0,70,(0,50,125),(0,0,0),(255,255,255))
    def draw(self,screen,mp):
        self.slots[self.pick].draw(screen,mp)
        self.slots[self.pick+1].draw(screen,mp)
        self.left_button.draw(screen)
        self.right_button.draw(screen)
    def switch_items(self,item,i):
        self.slots[i].switch_items(item)
    def check(self):
        player=-1
        for j,i in enumerate(self.slots):
            if i.type_picker.pick==1:
                if player==-1:
                    player=j
                else:
                    return 6,0
            if i.type_picker.pick in [4,5]:
                print(i.target_picker.pick)
                if self.slots[i.picks[i.target_picker.pick]].type_picker.pick==0:
                    return 5,j
            if i.check():
                return i.check(),j
        return 0,-1
    def ret_info(self):
        info=[]
        for i in self.slots:
            a=i.ret_info()
            print(a)
            if a:
                info.append(a)
        return info
    def update(self,mp,mc,keys):
        self.left_button.check_click(mp,mc)
        self.right_button.check_click(mp,mc)
        if self.left_button.do and self.pick>0:
            self.pick-=1
            self.slots[self.pick].move_x(self.x)
            self.slots[self.pick+1].move_x(self.x+self.gap+self.w)
        elif self.right_button.do and self.pick<self.l-2:
            self.pick+=1
            self.slots[self.pick].move_x(self.x)
            self.slots[self.pick+1].move_x(self.x+self.gap+self.w)
        a=self.slots[self.pick].update(mp,mc,keys)
        if a!=-1:
            return a,self.pick
        a=self.slots[self.pick+1].update(mp,mc,keys)
        if a!=-1:
            return a,self.pick+1
        return -1
class Player_slot:
    def __init__(self,x,y,width,height,name,starting_items):
        self.rect=pg.Rect(x,y,width,height)
        self.font=pg.font.SysFont("TimesNewRoman",50)
        self.font2=pg.font.SysFont("Arial",40)
        self.surface=pg.surface.Surface((width,height))
        self.label=Simple_label((width//2,30),200,name,0,(255,255,255),pos_type=1,font=self.font)
        self.type_label=Simple_label((width//2-100,110),200,"Type: ",0,(255,255,255),pos_type=1,font=self.font2)
        self.name_label=Simple_label((width//2-100,200),200,"Name: ",0,(255,255,255),pos_type=1,font=self.font2)
        self.max_speed_label=Simple_label((width//2-100,290),200,"Max speed: ",0,(255,255,255),pos_type=1,font=self.font2)
        self.max_turn_speed_label=Simple_label((width//2-90,360),200,"Max turn speed: ",0,(255,255,255),pos_type=1,font=self.font2)
        self.slowing_speed_label=Simple_label((width//2-90,360),200,"Slowing speed: ",0,(255,255,255),pos_type=1,font=self.font2)
        self.target_label=Simple_label((width//2-100,450),200,"Target: ",0,(255,255,255),pos_type=1,font=self.font2)

        self.type_picker=cotton_picker(["None","Player","1","2","3","4"],(width//2+10,90),width//3,30,5,font=pg.font.SysFont("Arial",30))
        a=["Car 1","Car 2","Car 3","Car 4","Car 5"]
        self.picks=[]
        for i in range(5):
            if a[i]!=name:
                self.picks.append(i)
        a.remove(name)

        self.target_picker=cotton_picker(a,(width//2+10,430),width//3,30,5,font=pg.font.SysFont("Arial",30))

        self.max_speed_box=Simple_text_box(width//2+20,270,80,50,self.font2,35,enter_clear=0,border=3,pointer_w=4,int_=1)
        self.max_turn_speed_box=Simple_text_box(width//2+40,340,80,50,self.font2,35,enter_clear=0,border=3,pointer_w=4,int_=1)
        self.text_box=Simple_text_box(width//2-30,180,220,50,self.font2,35,enter_clear=0,border=3,pointer_w=4)

        self.engine_rect=pg.Rect(110,500,100,100)
        self.nitro_rect=pg.Rect(250,500,100,100)
        self.talisman_rect=pg.Rect(110,610,100,100)
        self.tires_rect=pg.Rect(250,610,100,100)
        self.engine=starting_items[0]
        self.nitro=starting_items[1]
        self.talisman=starting_items[2]
        self.tires=starting_items[3]
        self.set_items()
        self.reset()
    def set_items(self):
        self.engine.rect.topleft=self.engine_rect.x+self.rect.x,self.engine_rect.y+self.rect.y
        self.nitro.rect.topleft=self.nitro_rect.x+self.rect.x,self.nitro_rect.y+self.rect.y
        self.talisman.rect.topleft=self.talisman_rect.x+self.rect.x,self.talisman_rect.y+self.rect.y
        self.tires.rect.topleft = self.tires_rect.x+self.rect.x,self.tires_rect.y+self.rect.y
    def switch_items(self,item):
        if self.engine_choose:
            self.engine=item
        if self.nitro_choose:
            self.nitro=item
        if self.talisman_choose:
            self.talisman=item
        if self.tires_choose:
            self.tires=item
        self.set_items()
    def reset(self):
        self.engine_choose=False
        self.tires_choose=False
        self.talisman_choose=False
        self.nitro_choose=False
    def draw(self,screen,mp):
        pg.draw.rect(self.surface,(20,0,110),pg.Rect(0,0,self.rect.w,self.rect.h))
        pg.draw.rect(self.surface,(10,0,50),pg.Rect(0,0,self.rect.w,self.rect.h),5)
        self.label.draw(self.surface)
        if self.type_picker.pick!=0:
            self.text_box.draw(self.surface)
            self.name_label.draw(self.surface)
            if self.type_picker.pick>=2:
                self.max_speed_label.draw(self.surface)
                self.max_speed_box.draw(self.surface)
                if 5>self.type_picker.pick>2:
                    self.max_turn_speed_label.draw(self.surface)
                    self.max_turn_speed_box.draw(self.surface)
                if self.type_picker.pick>3:
                    self.target_picker.draw(self.surface)
                    self.target_label.draw(self.surface)
                if self.type_picker.pick==5:
                    self.slowing_speed_label.draw(self.surface)
                    self.max_turn_speed_box.draw(self.surface)
        self.type_label.draw(self.surface)
        self.type_picker.draw(self.surface)
        screen.blit(self.surface,self.rect)
        if self.type_picker.pick!=0:
            self.set_items()
            b=0
            a=self.engine.draw(screen,mp)
            if a:
                b=a
            a=self.nitro.draw(screen,mp)
            if a:
                b=a
            a=self.tires.draw(screen,mp)
            if a:
                b=a
            a=self.talisman.draw(screen,mp)
            if a:
                b=a
            pg.draw.rect(screen,(0,0,0),self.engine.rect,2)
            pg.draw.rect(screen,(0,0,0),self.talisman.rect,2)
            pg.draw.rect(screen,(0,0,0),self.tires.rect,2)
            pg.draw.rect(screen,(0,0,0),self.nitro.rect,2)
            if b:
                screen.blit(b[0],b[1])

    def ret_info(self):
        info=[]
        if self.type_picker.pick==0:
            info.append(0)
        if self.type_picker.pick==1:
            info.append(3)
        elif self.type_picker.pick==2:
            info.append(1)
        elif self.type_picker.pick==3:
            info.append(2)
        elif self.type_picker.pick==4:
            info.append(4)
        elif self.type_picker.pick==5:
            info.append(5)
        info.append(self.text_box.text)
        if self.type_picker.pick>=2:
            info.append(int(self.max_speed_box.text))
        else:
            info.append(0)
        if self.type_picker.pick in [3,4,5]:
            info.append(int(self.max_turn_speed_box.text))
        else:
            info.append(0)
        if self.type_picker.pick==4 or self.type_picker.pick==5:
            info.append(self.picks[self.target_picker.pick])
        else:
            info.append(0)
        if self.type_picker.pick!=0:
            items = {
                "tires": self.tires,
                "talisman": self.talisman,
                "engine": self.engine,
                "nitro": self.nitro
            }
            info.append(items)
        return info
    def check(self):
        if self.type_picker.pick==0:
            return 0
        elif self.type_picker.pick==1:
            if len(self.text_box.text)==0:
                return 1
            else:
                return 0
        elif self.type_picker.pick==2:
            if len(self.text_box.text)==0:
                return 1
            if len(self.max_speed_box.text)==0:
                return 2
            else:
                return 0

        elif self.type_picker.pick==3 or self.type_picker.pick==4:
            if len(self.text_box.text)==0:
                return 1
            if len(self.max_speed_box.text)==0:
                return 2
            if len(self.max_turn_speed_box.text)==0:
                return 3
            else:
                return 0

        elif self.type_picker.pick==5:
            if len(self.text_box.text)==0:
                return 1
            if len(self.max_speed_box.text)==0:
                return 2
            if len(self.max_turn_speed_box.text)==0:
                return 4
            else:
                return 0


        return 0
    def move_x(self,x):
        self.rect.x=x
        self.set_items()
    def update(self,mp,mc,keys):
        mp=mp[0]-self.rect.x,mp[1]-self.rect.y

        self.type_picker.update(mp,mc)
        if self.type_picker.pick!=0:
            self.text_box.update(mp,mc,keys)
            if self.type_picker.pick >=2:
                self.max_speed_box.update(mp,mc,keys)
                if self.type_picker.pick>2:
                    self.max_turn_speed_box.update(mp,mc,keys)
                    if self.type_picker.pick>3:
                        self.target_picker.update(mp,mc)
            if mc[0]:
                if self.engine_rect.collidepoint(mp):
                    self.reset()
                    self.engine_choose=True
                    return 0
                if self.nitro_rect.collidepoint(mp):
                    self.reset()
                    self.nitro_choose=True
                    return 1
                if self.tires_rect.collidepoint(mp):
                    self.reset()
                    self.tires_choose=True
                    return 2
                if self.talisman_rect.collidepoint(mp):
                    self.reset()
                    self.talisman_choose=True
                    return 3
        return -1

    # self.slider.height = min((self.height) ** 2 / max(self.l * (self.h + self.gap), 1), self.rect.h)
    # self.slider.y = self.rect.y
    # self.slide_y = 0
    #     if self.slider_pressed:
    #         if mp[1] + self.slider.height // 2 <= self.rect.bottom:
    #             if mp[1] - self.slider.height // 2 >= self.rect.y:
    #                 self.slider.centery = mp[1]
    #             else:
    #                 self.slider.y = self.rect.y
    #         else:
    #             self.slider.bottom = self.rect.bottom
    #         self.slide_y = (self.rect.y - self.slider.y) / (
    #                     self.rect.height) * max(self.l * (self.h+self.gap), 1)

class Item_chooser:
    def __init__(self,items,width,height,heading_h,width2,height2):
        self.items=items
        self.surface=pg.surface.Surface((width,height))
        self.rect=self.surface.get_rect()
        self.heading=Simple_label((width//2,heading_h//2),0,"",heading_h,(255,255,255),pos_type=1)
        self.headings=["Engine","Nitro","Tires","Talisman"]
        self.items_surface=pg.surface.Surface((width2,height2))
        self.items_rect=self.items_surface.get_rect()
        self.items_pos=[10,heading_h+5]
        self.active=False
        self.slider=pg.Rect(self.items_rect.w+self.items_pos[0],self.items_pos[1],5,self.items_rect.h)
        self.slide_y=0
        self.slider_pressed=0
        print(self.items_rect)
    def initialise(self,type,pos,i):
        self.pos=pos
        self.filter = ["engine","nitro","tires","talisman"][type]
        self.type=type
        self.heading.update_text(self.headings[type])
        self.active=True
        self.set_pos()
        self.ind=i
        self.clicked=False
        self.first_click=True
    def set_pos(self):
        edges=10
        start_x=20
        x=start_x
        y=edges
        gap_x=10
        gap_y=5
        self.gap_y=gap_y
        self.l=1
        for i in self.items:
            if i.type==self.filter:
                i.rect.topleft=x,y
                x+=i.rect.w+gap_x
                if  x+i.rect.w>self.items_rect.w-edges:
                    x=start_x
                    y+=i.rect.h+gap_y
                    self.l+=1
        self.slider.height = min((self.items_rect.h) ** 2 / max(self.l * (100 + gap_y), 1), self.items_rect.h)
        self.slider.y = self.items_pos[1]
        self.slide_y = 0
    def update(self,mp,mc):
        if self.active:
            mp=mp[0]-self.pos[0],mp[1]-self.pos[1]
            if mc[0]:
                if self.slider.collidepoint(mp):
                    self.slider_pressed = 1
            else:
                self.slider_pressed = 0
            if self.slider_pressed:
                if mp[1] + self.slider.height // 2 <= self.items_rect.bottom+self.items_pos[1]:
                    if mp[1] - self.slider.height // 2 >= self.items_pos[1]:
                        self.slider.centery = mp[1]
                    else:
                        self.slider.y = self.items_pos[1]
                else:
                    self.slider.bottom = self.items_rect.bottom+self.items_pos[1]
                self.slide_y = (self.items_pos[1] - self.slider.y) / (
                    self.items_rect.height) * max(self.l * (100 + self.gap_y), 1)
            if mc[0]==False:
                self.first_click=False
            if not self.first_click:
                if not mc[0] and self.clicked:
                    if not self.rect.collidepoint(mp):
                        self.active=False
                    mp = mp[0] - self.items_pos[0], mp[1] - self.items_pos[1]
                    for i in self.items:
                        if i.type==self.filter and i.detect_click(mp):
                            self.active=False
                            return [i.copy(),self.ind]
                self.clicked=mc[0]
        return 0





    def draw(self,screen,mp):
        if self.active:
            original_mp=mp
            self.items_surface.fill(0)
            mp=mp[0]-self.items_pos[0]-self.pos[0],mp[1]-self.items_pos[1]-self.pos[1]
            b=0
            for i in self.items:
                if i.type==self.filter:
                    i.rect.y+=self.slide_y
                    a=i.draw(self.items_surface,mp,original_mp)
                    if a:
                        b=a
                    i.rect.y-=self.slide_y
            pg.draw.rect(self.items_surface,(255,0,0),self.items_rect,2)
            self.surface.fill((125,125,125))
            self.surface.blit(self.items_surface,self.items_pos)
            self.heading.draw(self.surface)
            pg.draw.rect(self.surface,(0,0,0),self.rect,5)
            pg.draw.rect(self.surface,(200,200,200),self.slider)
            screen.blit(self.surface,self.pos)
            if b:
                screen.blit(b[0],b[1])
            # pg.draw.rect(screen,(255,255,0),pg.Rect(self.pos[0]+self.items_rect.x,self.pos[1]+self.items_rect.y,self.items_rect.w,self.items_rect.h),10)


class Bug_message:
    def __init__(self,font):
        self.color=(255,0,0)
        self.cur=0
        self.font=font
    def initialise(self,x,y,width,txt,duration):
        self.duration=duration
        self.cur=duration
        self.x=x-width//2
        self.y=y
        self.width=width
        surfaces=[text(self.font,i,self.color) for i in text_down(txt,self.font,width)]
        gap=5
        h=sum([i[2]+gap for i in surfaces])
        self.surface=pg.surface.Surface((width,h),pg.SRCALPHA)
        y=0
        for i in surfaces:
            self.surface.blit(i[0],(width//2-i[1]//2,y))
            y+=i[2]+gap
    def draw(self,screen):
        if self.cur>0:
            self.cur-=1
            self.surface.set_alpha(int(255*self.cur/self.duration))
            screen.blit(self.surface,(self.x,self.y))
class Circle:
    def __init__(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r
    def collide_point(self,px,py):
        return (self.x-px)**2+(self.y-py)**2<=self.r**2
    def collide_circle(self,other):
        return (self.x-other.x)**2+(self.y-other.y)**2<=(self.r+other.r)**2
    def draw(self,screen):
        pg.draw.circle(screen,(255,0,0),(self.x,self.y),self.r)
class Timetable:
    def __init__(self,players,width,x,y,size,size2=40):
        self.l=players
        self.gap=10
        self.rect=pg.Rect(x,y,width,(size+self.gap)*(self.l+1)+self.gap)
        self.surface=pg.surface.Surface(self.rect.size,pg.SRCALPHA)
        self.players_labels=[Simple_label((width//5*1,(size+self.gap)*(i+1)),200,"",size,(255,255,255),pos_type=1) for i in range(players)]

        self.ct_label=Simple_label((width//5*3,size//2),200,"Last Lap",size,(255,255,255),pos_type=1)
        self.current_times=[Simple_label((width//5*3,(size+self.gap)*(i+1)+size//2),200,"--",size,(255,255,255),pos_type=1) for i in range(players)]

        self.bt_label=Simple_label((width//5*2,size//2),200,"Best Lap",size,(255,255,255),pos_type=1)
        self.best_times=[Simple_label((width//5*2,(size+self.gap)*(i+1)+size//2),200,"--",size,(255,255,255),pos_type=1) for i in range(players)]

        self.lap=Simple_label((width//5*4,size//2),200,"Lap",size,(255,255,255),pos_type=1)
        self.player_laps=[Simple_label((width//5*4,(size+self.gap)*(i+1)+size//2),200,"--",size,(255,255,255),pos_type=1) for i in range(players)]
        w=300
        h=50
        self.lap_label=Simple_label((w//4,size2//2),200,"",size2,(255,255,255),pos_type=1)
        self.time_label=Simple_label((w//4*3,size2//2),200,"",size2,(255,255,255),pos_type=1)
        self.rect2=pg.Rect(0,0,w,size2)
        self.rect2.center=(screen_width//2,size2//2)
        self.surface2=pg.surface.Surface(self.rect2.size,pg.SRCALPHA)
    def intialise(self,laps,names):
        self.times=[pg.time.get_ticks() for i in range(self.l)]
        self.lap_times=[[] for i in range(self.l)]
        self.laps=[0 for i in range(self.l)]
        self.best_laps=[-1 for i in range(self.l)]
        for j,i in enumerate(self.players_labels):
            i.update_text(names[j])
        self.laps_q=laps
        self.lap_label.update_text(f"Lap 1/{laps}")
        for i in self.player_laps:
            i.update_text("1")
        for i in self.current_times:
            i.update_text("--")
        for i in self.best_times:
            i.update_text("--")


    def update(self,Cars, console:Console):
        time=pg.time.get_ticks()
        for j,i in enumerate(Cars):
            if i.lap>self.laps[j]:
                self.laps[j]=i.lap
                if time-self.times[j]<self.best_laps[j] or self.best_laps[j]==-1:
                    self.best_laps[j]=time-self.times[j]
                    self.best_times[j].update_text(f"{self.best_laps[j]/1000}s")
                self.lap_times[j].append((time-self.times[j])/1000)
                self.current_times[j].update_text(f"{(time-self.times[j])/1000}s")
                console.add_system_text(f"{i.name} finished lap {i.lap} in: {(time-self.times[j])/1000}s")
                self.times[j]=time
                self.player_laps[j].update_text(str(self.laps[j]+1))
                if i.type==3:
                    self.lap_label.update_text(f"Lap {i.lap+1}/{self.laps_q}")
            if i.type==3:
                self.time_label.update_text(str((time-self.times[j])/1000)+"s")
        self.page=0

    def draw(self,screen):
        self.surface.fill((0,0,0,200))
        self.bt_label.draw(self.surface)
        self.ct_label.draw(self.surface)
        self.lap.draw(self.surface)
        for i in self.players_labels:
            i.draw(self.surface)
        for i in self.best_times:
            i.draw(self.surface)
        for i in self.current_times:
            i.draw(self.surface)
        for i in self.player_laps:
            i.draw(self.surface)
        screen.blit(self.surface, self.rect)

        self.surface2.fill((0,0,0,200))
        self.lap_label.draw(self.surface2)
        self.time_label.draw(self.surface2)
        screen.blit(self.surface2, self.rect2)

class Map_replay:
    def __init__(self,image,width,height,radius=5,color=(0,255,0),speed=5):
        self.image=pg.transform.scale(pg.image.load(image),(width,height))
        self.w=width
        self.h=height
        self.speed=speed
        self.cur=self.speed
        self.fading=10
        self.r=radius
        surface=pg.surface.Surface((radius*2,radius*2),pg.SRCALPHA)
        self.surfaces=[surface.copy() for i in range(self.fading)]
        for j,i in enumerate(self.surfaces):
            pg.draw.circle(i,color,(radius,radius),radius)
            i.set_alpha(255*(self.fading-j)/(self.fading))
        self.cur_i=self.fading
    def update_replay(self,replay):
        self.cur_i=0
        self.replay=replay
        self.l=len(replay)
    def update(self):
        if self.cur==0:
            self.cur=self.speed
            self.cur_i+=1
            self.cur_i%=self.l
        else:
            self.cur-=1
    def draw(self,screen,x,y):
        screen.blit(self.image,(x,y))
        for i in range(self.fading):
            screen.blit(self.surfaces[i],(self.replay[self.cur_i-i][0]*self.w/screen_width+x-self.r,self.replay[self.cur_i-i][1]*self.h/screen_height+y-self.r))
class Game_result:
    def __init__(self,console):
        self.labels=["Congratulations!","Well done!","Good job","Could've been worse :)","Damnn"]
        self.console=console
        self.results_button=Button("result",200,50,(200,150),0,40,(50,50,50),(0,0,0))
        self.stats_button=Button("Players Stats",200,50,(500,150),0,40,(50,50,50),(0,0,0))
        self.console_button=Button("console",200,50,(800,150),0,40,(50,50,50),(0,0,0))
        self.quit_button=Button("Quit",200,50,(750, 25),0,40,(50, 200, 0), (25, 100, 0), font_color=(0, 0, 255))
        self.save_quit_button=Button("Save;& Quit",200,50,(975, 25),0,40,(50, 200, 0), (25, 100, 0), font_color=(0, 0, 255))

    def intialise(self,place,names,players_info,places,gold_info,diamond_info,laps,map,speed,items):
        self.label=Simple_label((screen_width//2,50),100,self.labels[int(4*place/places)],50,(255,255,255),pos_type=1)
        self.place_label=Simple_label((screen_width//2,100),100,f"you got {place+1} place",30,(255,255,255),pos_type=1)
        rs=40
        self.resources_font=pg.font.SysFont("Times New Roman",rs)
        self.coin_label=Simple_label((300,300),100,f"Gold income:",30,(255,215,0),pos_type=1,font=self.resources_font)
        self.coin_labels=[Simple_label((300,350+rs*(i+1)),100,"",30,(255,215,0),pos_type=1,font=self.resources_font) for i in range(len(gold_info))]
        self.total_coins_label=Simple_label((300,700),100,f"",30,(255,215,0),pos_type=1,font=self.resources_font)
        self.gold_info=gold_info
        self.div=50
        self.cur_div=0
        self.gold_i=0
        gem_x=800
        self.gem_label=Simple_label((gem_x,300),100,f"Gem income:",30,(185,242,255),pos_type=1,font=self.resources_font)
        self.gem_labels=[Simple_label((gem_x,350+rs*(i+1)),100,f"",30,(185,242,255),pos_type=1,font=self.resources_font) for i in range(len(diamond_info))]
        self.total_gems_label=Simple_label((gem_x,700),100,f"",30,(185,242,255),pos_type=1,font=self.resources_font)
        self.gem_info=diamond_info
        self.div2=50
        self.cur_div2=0
        self.gem_i=0
        self.items=[[i.copy() for i in items[j]] for j in range(len(items))]
        y=720
        cx=130
        for i in self.items:
            x=650
            for j in i:
                j.rect.center=(x,y)
                x+=cx
        ps=35
        self.players_font=pg.font.SysFont("Times New Roman",ps)
        self.player_label=Simple_label((200,300),100,f"Player:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.player_picker=cotton_picker(names,(300,280),200,20,5,font=self.players_font)

        self.lap_label=Simple_label((700,300),100,f"lap:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.lap_pickers=[cotton_picker([str(i) for i in range(1,len(players_info[i])+1)],(800,280),200,20,5,font=self.players_font) for i in range(len(players_info))]
        self.laps=laps

        self.players_info=players_info
        self.time_label=Simple_label((300,500),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.avg_speed_label=Simple_label((850,400),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.max_speed_label=Simple_label((300,700),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.time_to_leader_label=Simple_label((300,600),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.place_lap_label     =Simple_label((300,400),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        font=pg.font.SysFont("Arial",80)
        self.save_text_box=Simple_text_box(screen_width//2-150,screen_height//2-100,300,100,font,80,)

        self.map=map
        self.speed=speed
        self.names=names
        self.map_replay=Map_replay(map,300,200,speed=speed)
        self.analyse_players_info()
        self.page=0
        self.total_coins=sum([i[1] for i in self.gold_info])
        self.total_gems=sum([i[1] for i in self.gem_info])
    def analyse_players_info(self):
        self.places = [[] for i in range(len(self.players_info))]
        self.time_to_leader = [[] for i in range(len(self.players_info))]
        a = [[0, i, 1] for i in range(len(self.players_info))]
        for i in range(self.laps):
            for k, j in enumerate(self.players_info):
                if i < len(j) and j[i][0]:
                    for x in a:
                        if x[1] == k:
                            x[0] += j[i][0]
                else:
                    for x in range(len(a)):
                        if a[x][1] == k:
                            a[x][2] = 0
            a.sort()
            print(a)
            for j, i in enumerate(a):
                if i[2]:
                    self.places[i[1]].append(j + 1)
                    self.time_to_leader[i[1]].append(int((a[j][0] - a[0][0]) * 1000) / 1000)
                else:
                    self.places[i[1]].append("--")
                    self.time_to_leader[i[1]].append("-- ")
    def update_player_stats(self):
        if self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][0]:
            self.time_label.update_text(f"Time: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][0]}s")
        else:
            self.time_label.update_text(f"Time: --")
        self.avg_speed_label.update_text(f"Average speed: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][1]}")
        self.max_speed_label.update_text(f"Max speed: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][2]}")
        self.time_to_leader_label.update_text(f"Time to leader: {self.time_to_leader[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick]}s")
        self.place_lap_label.update_text(f"Place: {self.places[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick]}")
        self.map_replay.update_replay(self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][3])
    def draw(self,screen,mp):
        self.results_button.draw(screen)
        self.stats_button.draw(screen)
        self.console_button.draw(screen)
        self.label.draw(screen)
        self.place_label.draw(screen)
        if self.page==0:
            self.gem_label.draw(screen)
            for i in self.gem_labels:
                i.draw(screen)
            for i in self.coin_labels:
                i.draw(screen)
            self.coin_label.draw(screen)
            self.total_gems_label.draw(screen)
            self.total_coins_label.draw(screen)
        elif self.page==1:
            self.player_label.draw(screen)
            self.lap_label.draw(screen)

            self.time_label.draw(screen)
            self.avg_speed_label.draw(screen)
            self.max_speed_label.draw(screen)
            self.place_lap_label.draw(screen)
            self.time_to_leader_label.draw(screen)

            self.map_replay.draw(screen,700,450)
            self.player_picker.draw(screen)
            self.lap_pickers[self.player_picker.pick].draw(screen)
            b=0
            for i in self.items[self.player_picker.pick]:
                a=i.draw(screen,mp)
                if a:
                    b=a
            if b:
                screen.blit(b[0],b[1])

        elif self.page==2:
            self.console.draw(screen)
        elif self.page==3:
            surface=pg.surface.Surface((screen_width,screen_height),pg.SRCALPHA)
            surface.fill((0,0,0,125))
            screen.blit(surface,(0,0))
            self.save_text_box.draw(screen)
        self.quit_button.draw(screen)
        self.save_quit_button.draw(screen)

        # with open("replays.txt", "r", encoding="utf-8") as file:
        #     for line in file:
        #         # print(line.strip())
        #         pass


            # \n adds a new line
    def update(self,mp,mc,keys,players):
        self.quit=False
        self.results_button.check_click(mp,mc)
        self.console_button.check_click(mp,mc)
        self.stats_button.check_click(mp,mc)
        self.quit_button.check_click(mp,mc)
        self.save_quit_button.check_click(mp,mc)
        if self.quit_button.do:
            self.quit=True
        if self.save_quit_button.do:
            self.page=3
            self.save_text_box.active =1
            # self.save()
            # self.quit=True
        if self.results_button.do:
            self.page=0
        if self.console_button.do:
            self.page=2

            self.console.active=1
        if self.stats_button.do:
            self.page=1
            self.update_player_stats()
        if self.page==3:
            save_name=self.save_text_box.update(mp,mc,keys)
            if save_name:
                self.save(save_name)
                self.quit=True

            if self.save_text_box.active==0:
                self.page=0
        if self.page==0:
            if self.gold_i<len(self.gold_info):
                self.coin_labels[self.gold_i].update_text(f"{self.gold_info[self.gold_i][0]}: +{self.gold_info[self.gold_i][1]*self.cur_div/self.div}")
                self.cur_div+=1
                if self.cur_div>self.div:
                    self.gold_i+=1
                    self.cur_div=0
            elif self.gold_i==len(self.gold_info):
                self.total_coins_label.update_text(
                    f"Total: {self.total_coins*self.cur_div/self.div}")
                self.cur_div += 1
                if self.cur_div > self.div:
                    self.gold_i += 1
                    self.cur_div = 0
            if self.gem_i<len(self.gem_info):
                self.gem_labels[self.gem_i].update_text(f"{self.gem_info[self.gem_i][0]}: +{self.gem_info[self.gem_i][1]*self.cur_div2/self.div2}")
                self.cur_div2+=1
                if self.cur_div2>self.div2:
                    self.gem_i+=1
                    self.cur_div2=0
            elif self.gem_i==len(self.gem_info):
                self.total_gems_label.update_text(f"Total: {self.total_gems*self.cur_div2/self.div2}")
                self.cur_div2+=1
                if self.cur_div2>self.div2:
                    self.gem_i+=1
                    self.cur_div2=0
        if self.page==1:
            if self.player_picker.update(mp,mc):
                self.update_player_stats()
            if self.lap_pickers[self.player_picker.pick].update(mp,mc):
                self.update_player_stats()
            self.map_replay.update()
        elif self.page==2:
            if keys[pg.K_ESCAPE]:
                self.console.active=0
                self.page=0
            self.console.update(mp,mc,keys,players)
    def save(self,save_name):
        with open("replays.txt", "a") as file:
            file.write(save_snippet)
            file.write(save_name+" . "+str(datetime.now().date()))
            file.write("\n")
            file.write(new_replay_save)
            for j,i in enumerate(self.players_info):
                print(i)
                file.write(new_player)
                file.write(f"{self.names[j]} . ")
                for k in i:
                    file.write(next_lap)
                    file.write(f"t{k[0]} ")
                    file.write(f"a{k[1]} ")
                    file.write(f"m{k[2]} ")
                    file.write("r ")
                    for i in k[3]:
                        file.write(f"{i[0]} {i[1]} ")
                    file.write("e ")
            file.write("\n")
            file.write(general_info)
            file.write(f"{self.laps} {self.map} {self.speed}")
            file.write("\n")
class Replay:
    def __init__(self):
        self.general_button=Button("General info",250,80,(275,60),5,45, (200, 200, 0), (125, 125, 0))
        self.stats_button=Button("Players Stats",250,80,(675,60),5,45, (200, 200, 0), (125, 125, 0))
        self.back_button=Button("Back",150,50,(1025, 725),5,40,(50, 200, 0), (25, 100, 0), font_color=(0, 0, 255))
    def intialise(self,laps,map,speed):
        rs=40
        ps=35
        self.players_font=pg.font.SysFont("Times New Roman",ps)
        self.resources_font=pg.font.SysFont("Times New Roman",rs)

        self.laps=laps
        self.analyse_players_info()

        self.bigger_font=pg.font.SysFont("Times New Roman",55)
        self.map_label=Simple_label((400,250),100,f"Map: {map.split('.')[0]}",30,(255,255,255),pos_type=1,font=self.bigger_font)
        self.laps_label=Simple_label((800,250),100,f"laps: {laps}",30,(255,255,255),pos_type=1,font=self.bigger_font)
        self.player_laps_label=Simple_label((400,400),100,f"laps:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.player_times_label=Simple_label((650,400),100,f"time:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.player_places_label=Simple_label((900,400),100,f"place: ",30,(255,255,255),pos_type=1,font=self.resources_font)

        gap=rs+20
        y=450
        l=len(self.names)
        self.players_labels=[Simple_label((150,y+gap*i),100,f"{self.names[i]}",30,(255,255,255),pos_type=1,font=self.resources_font) for i in range(l)]
        places=[0 for i in range(l)]
        times=[0 for i in range(l)]
        place=0
        for i in range(l):
            if self.final_result[i][2]!=0:
                place+=1
                places[self.final_result[i][1]]=place
                times[self.final_result[i][1]]=self.final_result[i][0]
            else:
                places[self.final_result[i][1]] = "-- "
                times[self.final_result[i][1]] = "-- "

        self.players_laps=[Simple_label((400,y+gap*i),100,f"{self.final_laps[i]}",30,(255,255,255),pos_type=1,font=self.resources_font) for i in range(l)]
        self.players_times=[Simple_label((650,y+gap*i),100,f"{times[i]}",30,(255,255,255),pos_type=1,font=self.resources_font) for i in range(l)]
        self.players_places=[Simple_label((900,y+gap*i),100,f"{places[i]}",30,(255,255,255),pos_type=1,font=self.resources_font) for i in range(l)]

        self.player_label=Simple_label((200,250),100,f"Player:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.player_picker=cotton_picker(self.names,(300,230),200,20,5,font=self.players_font)

        self.lap_label=Simple_label((700,250),100,f"lap:",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.lap_pickers=[cotton_picker([str(i) for i in range(1,len(self.players_info[i])+1)],(800,230),200,20,5,font=self.players_font) for i in range(l)]


        self.time_label=Simple_label((300,450),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.avg_speed_label=Simple_label((850,350),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.max_speed_label=Simple_label((300,650),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.time_to_leader_label=Simple_label((300,550),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)
        self.place_lap_label     =Simple_label((300,350),100,f"",30,(255,255,255),pos_type=1,font=self.resources_font)

        self.map_replay=Map_replay(map,300,200,speed=speed)
        self.page=0
        self.Quit=0
    def update_player_stats(self):
        if self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][0]:
            self.time_label.update_text(
                f"Time: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][0]}s")
        else:
            self.time_label.update_text(f"Time: --")
        self.avg_speed_label.update_text(
            f"Average speed: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][1]}")
        self.max_speed_label.update_text(
            f"Max speed: {self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][2]}")
        self.time_to_leader_label.update_text(
            f"Time to leader: {self.time_to_leader[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick]}s")
        self.place_lap_label.update_text(
            f"Place: {self.places[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick]}")
        self.map_replay.update_replay(
            self.players_info[self.player_picker.pick][self.lap_pickers[self.player_picker.pick].pick][3])
    def load(self,ind):
        self.get_players_info(ind)
        self.get_general_info(ind)
        self.intialise(self.general_info[0],self.general_info[1],self.general_info[2])
    def get_general_info(self,ind):
        self.general_info = []
        curr = 0
        with open("replays.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip().split()
                if line[0] == general_info.strip():
                    if curr == ind:
                        self.general_info.append(int(line[1]))
                        self.general_info.append(line[2])
                        self.general_info.append(int(line[3]))
                        return 0
                    else:
                        curr+=1
        return
    def get_players_info(self,ind):
        self.players_info=[]
        self.names=[]
        curr=0
        with open("replays.txt", "r", encoding="utf-8") as file:
            for line in file:
                line=line.strip().split()
                if line[0]==new_replay_save.strip():
                    if curr==ind:
                        i=0
                        l=len(line)
                        while i+1<l:
                            i+=1
                            if line[i]==new_player.strip():
                                self.players_info.append([])
                                i+=1
                                name=""
                                while line[i]!='.':
                                    name+=line[i]+" "
                                    i+=1
                                self.names.append(name.strip())
                            elif line[i]==next_lap.strip():
                                self.players_info[-1].append([])
                            elif line[i][0]=='t':
                                self.players_info[-1][-1].append(float(line[i][1:]))
                            elif line[i][0]=='a':
                                self.players_info[-1][-1].append(float(line[i][1:]))
                            elif line[i][0]=='m':
                                self.players_info[-1][-1].append(float(line[i][1:]))
                            elif line[i][0]=='r':
                                self.players_info[-1][-1].append([])
                                i+=1
                                while line[i][0]!='e':
                                    self.players_info[-1][-1][-1].append([int(line[i]),int(line[i+1])])
                                    i+=2
                        # print(self.players_info)
                        # print(self.names)
                        return 0
                    else:
                        curr+=1
        return 0
    def analyse_players_info(self):
        self.places=[[] for i in range(len(self.players_info))]
        self.time_to_leader=[[] for i in range(len(self.players_info))]
        self.final_laps=[0 for i in range(len(self.players_info))]
        a=[[0,i,1] for i in range(len(self.players_info))]
        for i in range(self.laps):
            for k,j in enumerate(self.players_info):
                if i<len(j) and j[i][0]:
                    for x in a:
                        if x[1]==k:
                            x[0]+=j[i][0]
                else:
                    if not self.final_laps[k]:
                        self.final_laps[k]=i
                    for x in range(len(a)):
                        if a[x][1]==k:
                            a[x][2]=0
            a.sort()
            print(a)
            for j,i in enumerate(a):
                if i[2]:
                    self.places[i[1]].append(j+1)
                    self.time_to_leader[i[1]].append(int((a[j][0]-a[0][0])*1000)/1000)
                else:
                    print("negro")
                    self.places[i[1]].append("--")
                    self.time_to_leader[i[1]].append("-- ")
        for i in range(len(self.final_laps)):
            if not self.final_laps[i]:
                self.final_laps[i]=self.laps

        self.final_result=a[:]

        print(self.final_result,self.final_laps)
    def quit(self):
        self.Quit=1
        del self.players_info
    def update(self,mp,mc,keys):
        self.stats_button.check_click(mp,mc)
        self.general_button.check_click(mp,mc)
        self.back_button.check_click(mp,mc)
        if self.back_button.do:
            self.quit()
        elif self.stats_button.do:
            self.page=1
            self.update_player_stats()
        elif self.general_button.do:
            self.page=0
        elif self.page==1:
            if self.player_picker.update(mp,mc):
                self.update_player_stats()
            if self.lap_pickers[self.player_picker.pick].update(mp,mc):
                self.update_player_stats()
            self.map_replay.update()
    def draw(self,screen):
        self.general_button.draw(screen)
        self.stats_button.draw(screen)
        self.back_button.draw(screen)
        if self.page==1:
            self.player_label.draw(screen)
            self.lap_label.draw(screen)

            self.time_label.draw(screen)
            self.avg_speed_label.draw(screen)
            self.max_speed_label.draw(screen)
            self.place_lap_label.draw(screen)
            self.time_to_leader_label.draw(screen)

            self.map_replay.draw(screen,700,450)
            self.player_picker.draw(screen)
            self.lap_pickers[self.player_picker.pick].draw(screen)
        else:
            self.map_label.draw(screen)
            self.laps_label.draw(screen)
            [i.draw(screen) for i in self.players_labels]
            [i.draw(screen) for i in self.players_laps]
            [i.draw(screen) for i in self.players_times]
            [i.draw(screen) for i in self.players_places]
            self.player_places_label.draw(screen)
            self.player_laps_label.draw(screen)
            self.player_times_label.draw(screen)



class Replay_snippets:
    def __init__(self,w,h,x,y,):
        self.y=y
        self.w=w
        self.h=h
        self.snippets=[]
        self.gap=10
        self.l=0
        self.height=700
        self.width=w
        self.surface=pg.surface.Surface((self.width,self.height))
        self.rect=pg.Rect(x,self.y,self.width,self.height)
        self.slider=pg.Rect(self.rect.right,y,20,self.height)
        self.slide_y=0
        self.slider_pressed=0
    def load(self):
        self.snippets=[]
        self.l=0
        with open("replays.txt", "r", encoding="utf-8") as file:
            for line in file:
                line=line.strip().split()
                if line[0]==save_snippet.strip():
                    i=1
                    name=""
                    while line[i] != '.':
                        name += line[i] + " "
                        i += 1
                    self.add(name,line[i+1])

    def add(self,name,date):
        # current_date = datetime.now().date()
        # print("Current Date:", current_date)
        self.snippets.append(Replay_snippet((self.h+self.gap)*self.l,self.w,self.h,name,date))
        self.l+=1
        self.slider.height = min((self.height) ** 2 / max(self.l * (self.h+self.gap), 1),self.rect.h)
        self.slider.y = self.rect.y
        self.slide_y = 0
    def update(self,mp,mc):
        if mc[0]:
            if self.slider.collidepoint(mp):
                self.slider_pressed = 1
        else:
            self.slider_pressed = 0
        if self.slider_pressed:
            if mp[1] + self.slider.height // 2 <= self.rect.bottom:
                if mp[1] - self.slider.height // 2 >= self.rect.y:
                    self.slider.centery = mp[1]
                else:
                    self.slider.y = self.rect.y
            else:
                self.slider.bottom = self.rect.bottom
            self.slide_y = (self.rect.y - self.slider.y) / (
                        self.rect.height) * max(self.l * (self.h+self.gap), 1)

        for j ,i in enumerate(self.snippets):
            if i.check_click(mp,mc,self.rect.x,self.y+self.slide_y):
                return j
        return -1
    def draw(self,screen):
        self.surface.fill(0)
        for i in self.snippets:
            i.draw(self.surface,self.slide_y)
        screen.blit(self.surface,self.rect)
        pg.draw.rect(screen,(200,200,200),self.slider)

class Replay_snippet:
    def __init__(self,y,w,h,name,date):
        self.y=y
        self.surface=pg.surface.Surface((w,h),pg.SRCALPHA)
        self.rect=pg.Rect(0,y,w,h)
        font_size=h-10
        font=pg.font.SysFont("Arial",font_size)
        Simple_label((0,0),0,f"{name}",font_size,(255,255,255),pos_type=0).draw(self.surface)
        Simple_label((w-text(font,f"{date}",(0,0,0))[1]-50,0),0,f"{date}",font_size,(255,255,255),pos_type=0).draw(self.surface)
    def check_click(self,mp,mc,x,y):
        self.active=0
        if self.rect.collidepoint((mp[0]-x,mp[1]-y)):
            self.active=1
            if mc[0]:
                return True
        return False
    def draw(self,screen,scroll):
        if self.active:
            pg.draw.rect(screen,(200,50,0),pg.Rect((self.rect.x,self.rect.y+scroll),self.rect.size))
        screen.blit(self.surface,(self.rect.x,self.rect.y+scroll))
class Icons:
    def __init__(self,images,size,positions,labels):
        font_size=50
        font=pg.font.SysFont("Comic Sans",font_size)
        self.l=len(images)
        self.icons=[Icon(images[i],size,positions[i],labels[i],font,font_size) for i in range(self.l)]
    def set_active(self,list):
        self.active=list
    def update_labels(self,labels):
        for i in range(self.l):
            self.icons[i].update_txt(labels[i])
    def set_max_values(self,values):
        for i in range(self.l):
            self.icons[i].set_max_val(values[i])
    def check_collisions(self,players):
        for i in self.icons:
            i.check_collision(players)
    def draw(self,screen,values):
        for i in range(self.l):
            if self.active[i]:
                self.icons[i].draw(screen,values[i])

class Icon:
    def __init__(self,image,size,pos,label,font,f_size):
        self.darking_surface=pg.Surface(size,pg.SRCALPHA)
        self.darking_surface.fill((0,0,0,150))
        self.image=pg.transform.scale(image,size)
        self.surface=pg.Surface(size,pg.SRCALPHA)
        self.surface.set_colorkey((0,0,0,150))
        self.pos=pos
        self.size=size
        self.label=Simple_label((pos[0]+size[0]+5,pos[1]+size[1]//2),0,label,f_size,(0,255,0),font=font,pos_type=2)
        self.rect=pg.Rect(pos,size)
        self.colliding=False
    def set_max_val(self,val):
        self.max_val=val
    def check_collision(self,players):
        self.colliding=False
        for i in players:
            if i.rects[0].colliderect(self.rect) or  i.rects[1].colliderect(self.rect):
                self.colliding = True
                break

    def draw(self,screen,current_val):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.image,(0,0))
        self.surface.blit(self.darking_surface,(0,self.size[1]*(1-current_val/self.max_val)))
        if self.colliding:
            self.surface.set_alpha(100)
        else:
            self.surface.set_alpha(255)
        screen.blit(self.surface,self.pos)
        self.label.draw(screen)
    def update_txt(self,txt):
        self.label.update_text(txt)


oil_size=[80,80]
oil_image=pg.Surface(oil_size,pg.SRCALPHA)
oil_image.blit(pg.transform.scale(pg.image.load("Oil.png"),oil_size),(0,0))
class Oil_stain:
    def __init__(self,pos,fading,level=0):
        self.level=level
        self.rect=pg.Rect([0,0],oil_size)
        self.rect.center=pos
        self.loooooow_tapeeer_fadee=255/fading
        self.fading=0
    def collide(self,player):
        return player.rects[0].colliderect(self.rect) or player.rects[1].colliderect(self.rect)
    def update(self,screen,players):

        for player in players:
            if self.collide(player):
                player.oil_effect=player.oil_effect_duration

        self.fading+=self.loooooow_tapeeer_fadee
        if self.fading>255:
            return True
        return False
    def draw(self,screen):
        surface=oil_image.copy()
        surface.set_alpha(int(255-self.fading))
        screen.blit(surface,self.rect)
accuarcy=2
def oil_terrain_check(pos, map):
    # if pos[0]+oil_size[0]//2>screen_width or pos[0]-oil_size[0]//2<0 or pos[1]+oil_size[1]//2>screen_height or pos[1]-oil_size[1]//2<0:
    #     return False
    # for x in range(oil_size[0]//accuarcy):
    #     x-=oil_size[0]//2
    #     for y in range(oil_size[1]//accuarcy):
    #         y-=oil_size[1]//2
    #         if map[(pos[0]+x*accuarcy)//tile_size][(pos[1]+y*accuarcy)//tile_size] == wall:
    #             return False
    return True