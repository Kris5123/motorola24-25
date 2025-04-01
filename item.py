import pygame
import pygame as pg
from assets import *
class Engine:
    def __init__(self,power,mass,price,rarity,w,h,size,id,pos=(0,0),image_name=0,special_power=0,name=""):
        self.name = name
        self.special_power = special_power
        colors=["black",(255,255,0),(50,50,50),(255,0,0),"black","black","black","black","black","black"]
        self.id=id

        self.rarity = rarity
        self.price = price
        self.power = power
        self.mass = mass
        self.size=size

        self.image_name = image_name
        self.type="engine"
        self.w=w
        self.h=h

        self.surf = pygame.surface.Surface((w, h))
        self.surf.fill(rarity_colors[rarity])
        if image_name != 0:
            print(image_name)
            self.image = pygame.transform.scale(pygame.image.load(image_name), (w, h))
            self.surf.blit(self.image, [0, 0])

        # if image:
        #     self.image=pygame.transform.scale(pygame.image.load(image),(w,h))
        # else:
        #     self.image=pygame.surface.Surface((w,h))
        #     self.image.fill(rarity_colors[rarity])

        self.stats_surface=pg.surface.Surface((200, 300))
        self.stats_surface.fill((rarity_colors[self.rarity]))
        pg.draw.rect(self.stats_surface,(0,0,0),self.stats_surface.get_rect(),1)

        self.rect = pygame.Rect(pos,(w,h))

        texts = [f"${self.price}",f"{self.mass} kg",f"{self.power}W"]


        if self.name != "":
            sigma = []
            c = []
            for n in self.name:
                sigma.append(n)
                c.append('black')
            c.pop(0)
            c.extend(colors)
            colors = c
            sigma.extend(texts)
            texts = sigma

        else:
            texts = [f"{self.name}",f"${self.price}",f"{self.mass} kg",f"{self.power}W"]


        if special_power:
            texts.extend(special_power)
        else:
            texts.append('no special powers')
        Simple_list([200//2,size],200,texts,size,font_colors=colors,pos_type=1).draw(self.stats_surface)

        # self.stats_surface = pg.surface.Surface((w, h))
        # self.stats_surface.fill((rarity_colors[self.rarity]))
        # self.rect = pygame.Rect(pos, (w, h))
        # Simple_list([w // 2, size], w, [f"${self.price}", f"{self.mass} kg", f"{self.power} W", f"{self.dur} s"], size,
        #             font_colors=colors, pos_type=1).draw(self.stats_surface)


    def detect_click(self,mp):
        if self.rect.collidepoint(mp):
            return 1

    def draw(self,screen,mouse_pos,draw_mouse_pos=0):
        if not draw_mouse_pos:
            draw_mouse_pos=mouse_pos
        screen.blit(self.surf, self.rect)
        if self.rect.collidepoint(mouse_pos):
            return [self.stats_surface,pygame.Rect((draw_mouse_pos[0]-(draw_mouse_pos[0] > screen_width/2)*200,draw_mouse_pos[1]-(draw_mouse_pos[1] > screen_height/2)*300),(200,300))]
        return 0
    def copy(self):
        return Engine(self.power,self.mass,self.price,self.rarity,self.w,self.h,self.size,self.id,special_power=self.special_power,name=self.name,image_name=self.image_name)

class Tires:
    def __init__(self,tires_friction_on_ice,tires_friction_on_sand,tires_friction_on_asphalt,mass,price,rarity,w,h,size,id,pos=(0,0),image_name=0,special_power=0,name=""):
        self.name = name
        self.special_power = special_power
        colors = ['black',(255, 255, 0), (50, 50, 50), (255, 0, 0),(255, 0, 0),(255, 0, 0),"black","black","black","black","black","black"]
        self.id = id
        self.rarity = rarity
        self.price = price
        self.asphalt_friction = tires_friction_on_asphalt
        self.ice_friction = tires_friction_on_ice
        self.sand_friction = tires_friction_on_sand
        self.mass = mass
        self.w=w
        self.h=h
        self.size=size

        self.image_name = image_name
        self.type="tires"

        self.surf = pygame.surface.Surface((w, h))
        self.surf.fill(rarity_colors[rarity])
        if image_name != 0:
            print(image_name)
            self.image = pygame.transform.scale(pygame.image.load(image_name), (w, h))
            self.surf.blit(self.image, [0, 0])

        # if image_name:
        #     self.image=pygame.transform.scale(pygame.image.load(image_name),(w,h))
        # else:
        #     self.image=pygame.surface.Surface((w,h))
        #     self.image.fill(rarity_colors[rarity])

        self.stats_surface = pg.surface.Surface((200, 300))
        self.stats_surface.fill((rarity_colors[self.rarity]))
        pg.draw.rect(self.stats_surface,(0,0,0),self.stats_surface.get_rect(),1)


        self.rect = pygame.Rect(pos, (w, h))

        texts = [ f"${self.price}", f"{self.mass} kg",
                 f"tarcie na asfalcie {self.asphalt_friction * 100}%", f'tarcie na piasku {self.sand_friction * 100}%',
                 f'tarcie na lodzie {self.ice_friction * 100}%']

        if self.name != "":
            sigma = []
            c = []
            for n in self.name:
                sigma.append(n)
                c.append('black')
            c.pop(0)
            c.extend(colors)
            colors = c
            sigma.extend(texts)
            texts=sigma

        else:
            texts = [f'{self.name}', f"${self.price}", f"{self.mass} kg",
                     f"tarcie na asfalcie {self.asphalt_friction * 100}%",
                     f'tarcie na piasku {self.sand_friction * 100}%',
                     f'tarcie na lodzie {self.ice_friction * 100}%']





        # texts =[f"{self.name}",f"${self.price}", f"{self.mass} kg", f"tarcie na asfalcie {self.asphalt_friction*100}%",  f'tarcie na piasku {self.sand_friction*100}%', f'tarcie na lodzie {self.ice_friction*100}%']
        if special_power:
            texts.extend(special_power)
        else:
            texts.append('no special powers')
        Simple_list([200 // 2, size], 200, texts, size, font_colors=colors, pos_type=1).draw(self.stats_surface)

        # self.stats_surface = pg.surface.Surface((w, h))
        # self.stats_surface.fill((rarity_colors[self.rarity]))
        # self.rect = pygame.Rect(pos, (w, h))
        # Simple_list([w // 2, size], w, [f"${self.price}", f"{self.mass} kg", f"{self.power} W", f"{self.dur} s"], size,
        #             font_colors=colors, pos_type=1).draw(self.stats_surface)

    def detect_click(self, mp):
        if self.rect.collidepoint(mp):
            return 1


    def draw(self,screen,mouse_pos,draw_mouse_pos=0):
        if not draw_mouse_pos:
            draw_mouse_pos=mouse_pos
        screen.blit(self.surf, self.rect)
        if self.rect.collidepoint(mouse_pos):
            return [self.stats_surface,pygame.Rect((draw_mouse_pos[0]-(draw_mouse_pos[0] > screen_width/2)*200,draw_mouse_pos[1]-(draw_mouse_pos[1] > screen_height/2)*300),(200,300))]
        return 0
    def copy(self):
        return Tires(self.ice_friction,self.sand_friction,self.asphalt_friction,self.mass,self.price,self.rarity,self.w,self.h,self.size,self.id,special_power=self.special_power,name=self.name,image_name=self.image_name)


class Nitro:
    def __init__(self,power,dur,delay,mass,price,rarity,w,h,size,id,pos=(0,0),image_name=0,special_power=0,name=""):
        self.name = name
        self.special_power = special_power
        self.id = id
        self.type = 'nitro'
        colors=['black',(255,255,0),(50,50,50),(50,50,50),(50,50,50),"black","black","black","black","black","black","black","black"]

        self.rarity = rarity
        self.price = price
        self.power = power
        self.mass = mass
        self.dur = dur
        self.delay = delay



        self.w=w
        self.h=h
        self.size=size

        self.image_name = image_name


        self.surf = pygame.surface.Surface((w,h))
        self.surf.fill(rarity_colors[rarity])
        if image_name != 0:
            print(image_name)
            self.image=pygame.transform.scale(pygame.image.load(image_name),(w,h))
            self.surf.blit(self.image,[0,0])


        # if image_name != 0:
        #     print(image_name)
        #     self.image=pygame.transform.scale(pygame.image.load(image_name),(w,h))
        # else:
        #     self.image=pygame.surface.Surface((w,h))
        #     self.image.fill(rarity_colors[rarity])
        self.stats_surface = pg.surface.Surface((200, 300))
        self.stats_surface.fill((rarity_colors[self.rarity]))
        pg.draw.rect(self.stats_surface,(0,0,0),self.stats_surface.get_rect(),1)

        self.rect = pygame.Rect(pos, (w, h))

        texts = [f"${self.price}",f"{self.mass} kg",f"{self.power} W",f"{self.dur/60} s"]

        if self.name != "":
            sigma = []
            c = []
            for n in self.name:
                sigma.append(n)
                c.append('black')
            c.pop(0)
            c.extend(colors)
            colors = c
            sigma.extend(texts)
            texts = sigma

        else:
            texts = [f'{self.name}', f"${self.price}", f"{self.mass} kg", f"{self.power} W", f"{self.dur} s"]

        if special_power:
            texts.extend(special_power)
        else:
            texts.append('no special powers')
        Simple_list([200 // 2, size], 200, texts, size, font_colors=colors, pos_type=1).draw(self.stats_surface)

        # self.stats_surface = pg.surface.Surface((w, h))
        # self.stats_surface.fill((rarity_colors[self.rarity]))
        # self.rect = pygame.Rect(pos, (w, h))
        # Simple_list([w // 2, size], w, [f"${self.price}", f"{self.mass} kg", f"{self.power} W", f"{self.dur} s"], size,
        #             font_colors=colors, pos_type=1).draw(self.stats_surface)

    def detect_click(self, mp):
        if self.rect.collidepoint(mp):
            return 1


    def draw(self,screen,mouse_pos,draw_mouse_pos=0):
        if not draw_mouse_pos:
            draw_mouse_pos=mouse_pos
        screen.blit(self.surf, self.rect)
        if self.rect.collidepoint(mouse_pos):
            return [self.stats_surface,pygame.Rect((draw_mouse_pos[0]-(draw_mouse_pos[0] > screen_width/2)*200,draw_mouse_pos[1]-(draw_mouse_pos[1] > screen_height/2)*300),(200,300))]
        return 0

    def copy(self):
        return Nitro(self.power,self.dur,self.delay,self.mass,self.price,self.rarity,self.w,self.h,self.size,self.id,special_power=self.special_power,name=self.name,image_name=self.image_name)


class Talisman:
    def __init__(self,price,rarity ,w,h,size,id,pos=(0,0),image_name=0,special_power=0,name=""):
        self.name = name
        self.special_power =special_power
        self.type = 'talisman'
        self.id = id
        colors=['black',(255,0,255),"black","black","black","black","black","black"]

        self.rarity = rarity
        self.price = price

        self.w=w
        self.h=h
        self.size=size

        self.image_name=image_name

        self.surf = pygame.surface.Surface((w, h))
        self.surf.fill(rarity_colors[rarity])
        if image_name != 0:
            print(image_name)
            self.image = pygame.transform.scale(pygame.image.load(image_name), (w, h))
            self.surf.blit(self.image, [0, 0])

        # if image:
        #     self.image=pygame.transform.scale(pygame.image.load(image),(w,h))
        # else:
        #     self.image=pygame.surface.Surface((w,h))
        #     self.image.fill(rarity_colors[rarity])

        self.stats_surface = pg.surface.Surface((200, 300))
        self.stats_surface.fill((rarity_colors[self.rarity]))
        pg.draw.rect(self.stats_surface,(0,0,0),self.stats_surface.get_rect(),1)

        self.rect = pygame.Rect(pos, (w, h))
        texts = [f"{self.price} gems"]

        if self.name != "":
            sigma = []
            c = []
            for n in self.name:
                sigma.append(n)
                c.append('black')
            c.pop(0)
            c.extend(colors)
            colors = c
            sigma.extend(texts)
            texts = sigma

        else:
            texts = [f'{self.name}', f"${self.price} gems"]

        if special_power:
            texts.extend(special_power)
        else:
            texts.append('no special powers')

        Simple_list([200 // 2, size], 200, texts, size, font_colors=colors, pos_type=1).draw(self.stats_surface)

        # self.stats_surface = pg.surface.Surface((w, h))
        # self.stats_surface.fill((rarity_colors[self.rarity]))
        # self.rect = pygame.Rect(pos, (w, h))
        # Simple_list([w // 2, size], w, [f"${self.price}", f"{self.mass} kg", f"{self.power} W", f"{self.dur} s"], size,
        #             font_colors=colors, pos_type=1).draw(self.stats_surface)

    def detect_click(self, mp):
        if self.rect.collidepoint(mp):
            return 1


    def draw(self,screen,mouse_pos,draw_mouse_pos=0):
        if not draw_mouse_pos:
            draw_mouse_pos=mouse_pos
        screen.blit(self.surf, self.rect)
        if self.rect.collidepoint(mouse_pos):
            return [self.stats_surface,pygame.Rect((draw_mouse_pos[0]-(draw_mouse_pos[0] > screen_width/2)*200,draw_mouse_pos[1]-(draw_mouse_pos[1] > screen_height/2)*300),(200,300))]
        return 0

    def copy(self):
        return Talisman(self.price,self.rarity,self.w,self.h,self.size,self.id,special_power=self.special_power,name=self.name,image_name=self.image_name)


rarity_colors = {
    "common":"grey",
    "uncommon":"green",
    "rare":"blue",
    "epic":"purple",
    "legendary":"gold"
}

f_size=20 #<-------------
w=100
h=100
#Nitro
# 10-12 normal 13 Sins 14 JanSzuk 16 bananowe 17 wampiryczne 18 ładujące się 19 wybuchąjace
items=[Nitro(745*20, 5*60, 3*60, 100,100, "common", w, h, f_size,10,name=['słabe nitro'],special_power=["minimalne przyspieszenie"],image_name="items_images/zwykłe nitro.png"),
        Nitro(745*20*2, 5*60, 6*60, 150,100, "uncommon", w, h, f_size,11,name=['średnie nitro'],special_power=["ma kopa"],image_name="items_images/średnie nitro.png"),
        Nitro(745*20*3, 5*60, 10*60, 200,200, "rare", w, h, f_size,12,name=['mocne nitro'],special_power=["zrywa czapki z głów"],image_name="items_images/mocne nitro.png"),
        Nitro(745*120, 3*60, 15*60, 300,200, "rare", w, h, f_size,13,name=['najmocniejsze nitro'],special_power=["to ptak!,","to samolot!","to rakieta!","nie, to twoje auto","z naszym nitrem"],image_name="items_images/najmocniejsze nitro.png"),
        Nitro(745*35, 2*60, 3*60, 50,200, "rare", w, h, f_size,14,name=['kompaktowe nitro'],special_power=["pomimo niskiej mocy,","to nitro","ma niski cooldown,","i nieskończoną ilość użyć","co czyni je,","definicją powiedzenia","'mały, ale wariat'"],image_name="items_images/kompaktowe nitro.png"),
        # Nitro(745*20, 3*60, 15*60, 500,10, "epic", w, h, f_size,15,name=['słaby nitro'],special_power=["nic specjalnego"]),
        Nitro(745*20, 5*60, 10*60, 250,300, "epic", w, h, f_size,16,name=['bananowe nitro'],special_power=["co każde użycie","z rury wydechowej","wypada skórka banana"],image_name="items_images/bananowe_nitro.png"),
        Nitro(745*10, 4*60, 10*60, 250,400, "epic", w, h, f_size,18,name=['ładujące się nitro'],special_power=["wraz z czasem,","jego moc wzrasta","(każde użycie","ją resetuje)"],image_name="items_images/łądujące_się_nitro.png"),
        Nitro(745*20, 4*60, 15*60, 500,400, "legendary", w, h, f_size,17,name=['wampiryczne nitro'],special_power=["dusze pobliskich","przeciwników", "zwiększają moc tego","potwornego wynalazku","(każde użycie","ją resetuje)"],image_name="items_images/wampiryczne_nitro.png"),
        Nitro(745*120, 3*60, 15*60, 500,400, "legendary", w, h, f_size,19,name=['wybuchowe nitro'],special_power=["każde użycie","tego nitra tworzy","falę uderzeniową","odpychając rywali"],image_name="items_images/wybuchowe_nitro.png"),
#21 zmiowy,22 piaskowy,23 bananowy,24 stolarski,25 złoty,26 gemowy
        Engine(745*100, 200, 100, "common", w, h, f_size,20,name=['słaby silnik'],special_power=["nic specjalnego"],image_name="items_images/zwykły silnik.png"),
        Engine(745*110, 180, 150, "uncommon", w, h, f_size,27,name=['średni silnik'],special_power=["przyzwoita moc"],image_name="items_images/zwykły silnik.png"),
        Engine(745*120, 160, 200, "rare", w, h, f_size,28,name=['mocny silnik'],special_power=["istna bestia"],image_name="items_images/zwykły silnik.png"),
        Engine(745*120, 160, 200, "epic", w, h, f_size,21,name=['silnik zimowy'],special_power=["kocha niskie temperatury","(ma w nich 15%","więcej mocy)"],image_name="items_images/silnik zimowy.png"),
        Engine(745*120, 160, 200, "epic", w, h, f_size,22,name=['silnik pustynny'],special_power=["kocha wysokie temperatury","(ma w nich 15%","więcej mocy)"],image_name="items_images/silnik pustynny.png"),
        Engine(745*120, 250, 200, "epic", w, h, f_size,23,name=['silnik bananowy'],special_power=["napędzany bananami,","pasywnie dodaje skórki","do upuszczenia"],image_name="items_images/silnik bananowy.png"),
        Engine(745*120, 250, 200, "epic", w, h, f_size,24,name=['silnik stolarski'],special_power=["ktoś kiedyś zamknął","stolarza w silniku","teraz produkuje on","dodakowe bariery","w trakcie wyścigu"],image_name="items_images/silnik stolarski.png"),
        Engine(745*120, 400, 200, "legendary", w, h, f_size,25,name=['złoty silnik'],special_power=["daje 50% więcej","złota"],image_name="items_images/złoty_silnik.png"),
        Engine(745*120, 400, 200, "legendary", w, h, f_size,26,name=['diamentowy silnik'],special_power=["daje 50% więcej","diamentów"],image_name="items_images/silnik diamentowy.png"),

    #  nicnierobienia , mocy,  bananowoskórkowej odpornośći,  golda,  diamenów,  złoto-diamentowy,   banana,  nitra,  mniejszej masy,  większej masy,

        Talisman(100,"common",w,h,f_size,40,name=['talizman nicnierobienia'],special_power=["nic nie daje, zajmuje","miejsce w ekwipunku"],image_name="items_images/talizman_nicnierobienia.png"),
        Talisman(300,"epic",w,h,f_size,41,name=['talizman mocy'],special_power=["zwiększa moc","silnika o 15%"],image_name="items_images/talizman_mocy.png"),
        Talisman(600,"epic",w,h,f_size,42,name=['talizman','bananowoskórkowej','odporności'],special_power=["zapewnia bananowo-","skórkową odporność"],image_name="items_images/talizman bananowoskórkowej odporności.png"),
        Talisman(300,"epic",w,h,f_size,43,name=['talizman złota'],special_power=["daje 50% więcej","złota"],image_name="items_images/talizman złota.png"),
        Talisman(300,"epic",w,h,f_size,44,name=['talizman diamentów'],special_power=["daje 50% więcej"," diamentów"],image_name="items_images/talizman_diamentów.png"),
        Talisman(600,"epic",w,h,f_size,45,name=['talizman bogactwa'],special_power=["daje 50% więcej", "złota i diamentów"],image_name="items_images/talizman bogactwa.png"),
        Talisman(300,"epic",w,h,f_size,46,name=['bananowy talizman'],special_power=["dwukrotnie zwiększa","ilość skórek","do upuszczenia","oraz","dwukrotnie","zmniejsza cooldown"],image_name="items_images/bananowy talisman.png"),
        Talisman(300,"epic",w,h,f_size,47,name=['talizman nitra'],special_power=["podwaja ilość użyć nitra"],image_name="items_images/talizman nitro.png"),
        Talisman(500,"rare",w,h,f_size,48,name=['talizman większej masy'],special_power=['zwiększa masę','auta o 15%'],image_name="items_images/talizman zwiększenia masy.png"),
        Talisman(500,"rare",w,h,f_size,49,name=['talizman mniejszej masy'],special_power=['zmniejsza masę','auta o 15%'],image_name="items_images/talizman zmniejszenia masy.png"),
        Talisman(500,"legendary",w,h,f_size,410,name=['talizman gadżeciaża'],special_power=['podwaja ilość użyć','wszytskich gadżetów'],image_name="items_images/talizman gadżeciaża.png"),




        Tires(1, 1, 1, 100, 100, "common", w, h, f_size,30,name=["zwykłe opony"],special_power=["jak w passacie","twojego ojca"],image_name="items_images/zwykła opona 2.png"),
        Tires(1.2, 1.2, 1.2, 100, 200, "uncommon", w, h, f_size,33,name=["przyczepne opony"],special_power=["zwiększają tarcie"],image_name="items_images/przyczepna opona.png"), # zwiekszone tarcie
        Tires(0.8, 0.8, 0.8, 100, 200, "uncommon", w, h, f_size,34,name=["śliskie opony"],special_power=["zmniejszają tarcie"],image_name="items_images/sliska opona.png"), # zmniejszone tarcie # zwykłe
        Tires(1.38, 1, 1, 100, 300, "rare", w, h, f_size,31,name=["zimowe opony"],special_power=["odporne na lód"],image_name="items_images/lodowa opona.png"), # śniegowe
        Tires(1, 0.49, 1, 100, 300, "rare", w, h, f_size,32,name=["pustynne opony"],special_power=["odporne na piasek"],image_name="items_images/opona_piaskowa.png"), # piaskowe
        Tires(1, 1, 1, 100, 200, "rare", w, h, f_size,38,name=["sztutrowe opony"],special_power=["są odporne na sztutr"],image_name="items_images/sztutrowe opony.png"),
        Tires(1, 1, 1, 300, 300, "epic", w, h, f_size,36,name=["złote opony"],special_power=["50% więcej złota "],image_name="items_images/złota opona.png"), # złote
        Tires(1, 1, 1, 300, 300, "epic", w, h, f_size,37,name=["diamentowe opony"],special_power=["50% więcej diamentów"],image_name="items_images/diamentowa_opona.png"), # diamentowe
        Tires(1.38, 0.49, 1, 100, 1000, "legendary", w, h, f_size,35,name=["profesjonalne opony"],special_power=["idealne na każde warunki"],image_name="items_images/profesjonalne opony.png"), # śniegowo/piaskowe = uniwersalne
]

# "tires":
# Tires(1, 1, 1, 100, 100, "common", 100, 100, f_size,"0"),
#             "talisman": Armor(10, 200, 100, "common", 100, 100, f_size,"0"),
#             "engine": Engine(745*90, 200, 100, "common", 100, 100, f_size,"0"),
#             "nitro": Nitro(20000, 500, 100, 100, "common", 100, 100, f_size,"0")

eq=[]