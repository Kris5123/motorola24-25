import pygame

from assets import Simple_label,Button
from item import Engine,Nitro,Tires,Talisman
from settings import *




class Inventory_Display:
    def __init__(self,pos,size,eq,row,scroll,gap_y,start_gap=0,end_gap=0,bg_color="black",window_color = "pink",window_fill=0):
        self.mouse_ready = True
        self.lowest_y = 0
        self.eq = eq

        self.bg_color = bg_color
        self.window_color = window_color
        self.window_fill = window_fill

        self.row = row
        self.scroll = scroll
        self.gap_y = gap_y
        self.start_gap = start_gap
        self.end_gap = end_gap
        self.pos = pos
        self.w = size[0]
        self.h = size[1]


        # self.tires_pos = tires_pos
        # self.armor_pos = armor_pos
        # self.engine_pos = engine_pos
        # self.nitro_pos = nitro_pos

        self.filter = set(["tires","talisman","engine","nitro"])



        self.all_button = Button("all", 70, 50, (35, 375), 7, 20, (204, 229, 255), (51, 53, 255), pos_type=1,
                            font_color="black")
        self.tires_button = Button("tires", 70, 50, (105, 375), 7, 20, (204, 229, 255), (51, 53, 255), pos_type=1,
                              font_color="black")
        self.armor_button = Button("armor", 70, 50, (175, 375), 7, 20, (204, 229, 255), (51, 53, 255), pos_type=1,
                              font_color="black")
        self.engine_button = Button("engine", 70, 50, (245, 375), 7, 20, (204, 229, 255), (51, 53, 255), pos_type=1,
                               font_color="black")
        self.nitro_button = Button("nitro", 70, 50, (315, 375), 7, 20, (204, 229, 255), (51, 53, 255), pos_type=1,
                              font_color="black")

    def update(self,mp,mc):
        self.all_button.check_click(mp, mc)
        self.tires_button.check_click(mp, mc)
        self.armor_button.check_click(mp, mc)
        self.engine_button.check_click(mp, mc)
        self.nitro_button.check_click(mp, mc)

        if self.all_button.do:
            self.filter = set(["tires","talisman","engine","nitro"])
            self.scroll = 0
        elif self.tires_button.do:
            self.filter = set(["tires"])
            self.scroll = 0
        elif self.armor_button.do:
            self.filter = set(["talisman"])
            self.scroll = 0
        elif self.engine_button.do:
            self.filter = set(["engine"])
            self.scroll = 0
        elif self.nitro_button.do:
            self.filter = set(["nitro"])
            self.scroll = 0



    def set_pos(self,mc,mp,car):



        if not mc[0]:
            self.mouse_ready = True

        elif self.mouse_ready and self.pos[0] <= mp[0] <= self.pos[0] + self.w and self.pos[1] < mp[1] < self.pos[1] + self.h:
            self.mouse_ready = False
            # .copy() ?
            for e in self.eq:
                # and self.pos[0] < e.rect.x < self.pos[0] + self.w and self.pos[1] < e.rect.y < self.pos[1] + self.h:
                if e.detect_click(mp) and e.type in self.filter:
                    self.eq.remove(e)
                    self.eq.append(car.items[e.type])
                    car.items[e.type] = e
                    e.rect.x, e.rect.y = items_pos[e.type]
                    break

        if len(self.eq) > 0:
            row = 0
            r  = 0
            column = 0
            item_w = self.eq[0].w
            item_h = self.eq[0].h
            gap_x = (self.w - (self.row * item_w)) / (self.row + 1)
            m = 0
            for e in self.eq:
                if e.type in self.filter:
                    e.rect.y = self.pos[1] + item_h * int(row) + self.gap_y * int(row) - self.scroll + self.start_gap
                    e.rect.x = self.pos[0] + item_w * column + gap_x * (column + 1)

                    column += 1
                    r  += 1
                    if r  == self.row:
                        r  = 0
                        row += 1
                        column = 0

                    m=e.rect.y

            if m + item_h < self.pos[1] + self.h - self.end_gap:
                if self.start_gap + (row+1) * item_h + row*self.gap_y+self.end_gap > self.h:
                    self.scroll = self.scroll + m + item_h - self.pos[1] - self.h + self.end_gap

            if self.start_gap + (row + 1) * item_h + row * self.gap_y + self.end_gap <= self.h:
                self.scroll = 0








            # self.scroll = min(self.scroll + self.eq[-1].rect.y + item_h - self.pos[1] - self.h + self.end_gap,self.scroll)



    def draw(self,screen,mp,car):
        pygame.draw.rect(screen, self.window_color, (self.pos[0], self.pos[1], self.w, self.h), self.window_fill)
        # print("")
        # print("")

        r = 0
        for e in self.eq:
            if e.type in self.filter:
                skibidi = e.draw(screen,mp)

                if skibidi:
                    r=skibidi

        pygame.draw.rect(screen, self.bg_color, (self.pos[0], 0, self.w, self.pos[1]), 0)
        pygame.draw.rect(screen, self.bg_color, (self.pos[0], self.pos[1]+self.h, self.w, 800-self.pos[1]+self.h), 0)





        for i in car.items:
            skibidi = car.items[i].draw(screen,mp)
            if skibidi:
                r=skibidi
            # print(car.items[i].rect.x, car.items[i].rect.y, i)

        self.all_button.draw(screen)
        self.tires_button.draw(screen)
        self.armor_button.draw(screen)
        self.engine_button.draw(screen)
        self.nitro_button.draw(screen)

        if r:
            screen.blit(r[0],r[1])


