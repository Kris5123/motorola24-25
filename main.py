import random
import pygame as pg

pg.init()  # Ensure Pygame is initialized first
from Car import Car_
from assets import *
from functions import *
from mapa import *
from settings import *
from item import *
from InventoryDisplay import *
import pygame.mixer

clock = pg.time.Clock()

# Show screen
show_screen = pg.display.set_mode((show_width, show_height))

screen = pg.surface.Surface((screen_width, screen_height), pg.FULLSCREEN)
pygame.display.set_caption("Szybkie Sigmy")
# Variables

sec = 1000  # Update slots every 1 second

# Pages
page = 2

items_chooser = Item_chooser(items, 540, 520, 150, 500 - 25, 350)
pause_screen = Pause_screen(150, 100, 900, 600, (0, 0, 125), start_musik_volume, start_sfx_volume)
settings_screen = Settings_screen(150, 100, 900, 600, (0, 0, 125), start_musik_volume, start_sfx_volume)
console = Console(150, 100, 900, 600, 40, 10, 10)
player_slots = Player_slots(120, 25, 5, [items[10].copy(), items[0].copy(), items[19].copy(), items[29].copy()])
bug_font = pg.font.SysFont("Arial", 50)
bug_message = Bug_message(bug_font)
time_table = Timetable(5, 300, 900, 0, 17)
game_results = Game_result(console)
replays_snippets = Replay_snippets(650, 50, 275, 50)
replay = Replay()
# Images
coinimg = pg.transform.scale(pg.image.load("coin 2.png"), (40, 40))
gemimg = pg.transform.scale(pg.image.load("gem.png"), (40, 40))

# Car
#
# Car
# ,,Car_(2,100,700)
enemys = [Car_(), Car_(), Car_(), Car_(), Car_()]

# loading save
load_save = load()

coinamount = load_save[0]

gemamount = load_save[1]

load_items = id_to_items(load_save[2], items)
load_items = {"tires": load_items[0],
              "talisman": load_items[1],
              "engine": load_items[2],
              "nitro": load_items[3]}
enemys[0].items = load_items
enemys[0].set_item_pos()

a = load_save[3]
unlocked_maps = [0, 0, 0, 0, 0]
for i in range(a):
    unlocked_maps[i] = 1
load_eq = id_to_items(load_save[4], items)
eq = load_eq


rfps_label = Simple_label([0, 0], 200, "Sigma", 50, (0, 255, 0))
start_label = Simple_label((screen_width / 2, 100), 400, "Szybkie Sigmy", 200, (200, 200, 200), pos_type=1)
coin_label = Simple_label((50, 12), 0, f"{coinamount}", 40, (255, 255, 255))
gem_label = Simple_label((50, 63), 0, f"{gemamount}", 40, (255, 255, 255))

startt_label = Simple_label([600, 600], 200, "START!", 300, (0, 255, 128), pos_type=1)
three_label = Simple_label([300, 250], 200, "3", 400, (0, 0, 255), pos_type=1)
two_label = Simple_label([600, 250], 200, "2", 400, (0, 128, 255), pos_type=1)
one_label = Simple_label([900, 250], 200, "1", 400, (0, 255, 255), pos_type=1)

keybind_labels = [
    Simple_label((screen_width / 7 * 1, screen_height / 5 * 1), 150, "drive_forwards", 30, (200, 200, 200), pos_type=1),
    Simple_label((screen_width / 7 * 1, screen_height / 5 * 2), 150, "drive_backwards", 30, (200, 200, 200),
                 pos_type=1),
    Simple_label((screen_width / 7 * 1, screen_height / 5 * 3), 150, "turn_left", 30, (200, 200, 200), pos_type=1),
    Simple_label((screen_width / 7 * 1, screen_height / 5 * 4), 150, "turn_right", 30, (200, 200, 200), pos_type=1),
    Simple_label((screen_width / 7 * 4, screen_height / 5 * 1), 150, "use_nitro", 30, (200, 200, 200), pos_type=1),
    Simple_label((screen_width / 7 * 4, screen_height / 5 * 2), 150, "spawn_banana", 30, (200, 200, 200), pos_type=1),
    Simple_label((screen_width / 7 * 4, screen_height / 5 * 3), 150, "spawn_barrier", 30, (200, 200, 200), pos_type=1),
Simple_label((screen_width / 7 * 4, screen_height / 5 * 4), 150, "spawn_oil", 30, (200, 200, 200), pos_type=1),
]
keybind_buttons = [
    Keybind_button("drive_forwards", [keybind_labels[2].rect.x + 170, keybind_labels[0].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "w"),
    Keybind_button("drive_backwards", [keybind_labels[2].rect.x + 170, keybind_labels[1].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "s"),
    Keybind_button("turn_left", [keybind_labels[2].rect.x + 170, keybind_labels[2].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "a"),
    Keybind_button("turn_right", [keybind_labels[2].rect.x + 170, keybind_labels[3].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "d"),
    Keybind_button("use_nitro", [keybind_labels[4].rect.x + 170, keybind_labels[4].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "left ctrl"),
    Keybind_button("spawn_banana", [keybind_labels[4].rect.x + 170, keybind_labels[5].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "space"),
    Keybind_button("spawn_barrier", [keybind_labels[4].rect.x + 170, keybind_labels[6].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "f"),
Keybind_button("spawn_oil", [keybind_labels[4].rect.x + 170, keybind_labels[7].rect.y], 150, (50, 200, 0),
                   (0, 0, 255), 30, "q"),
]

# lists
# Buttons

start_button = Button("Start", 400, 120, (screen_width // 2, 600), 5, 50, (200, 200, 0), (125, 125, 0), pos_type=1,
                      font_color=(0, 0, 255))

play_button = Button("Play", 500, 75, (screen_width // 2, 400), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
                     font_color=(0, 0, 255))
shop_button = Button("Shop", 500, 75, (screen_width // 2, 500), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
                     font_color=(0, 0, 255))
replays_button = Button("Replays", 500, 75, (screen_width // 2, 600), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
                        font_color=(0, 0, 255))
inventory_button = Button("Inventory", 500, 75, (screen_width // 2, 700), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
                          font_color=(0, 0, 255))
settings_button = Button("Settings", 200, 30, (screen_width - 100, 30), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
                         font_color=(0, 0, 255))

roll = Button("Roll (10 coins)", 400, 100, (screen_width // 2, 300), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=1,
              font_color=(0, 0, 255))
back_button = Button("Back", 200, 50, (1075, 50), 5, 40, (50, 200, 0), (25, 100, 0), pos_type=1, font_color=(0, 0, 255))
campaign_button = Button("Campaign", 300, 75, (200, 600), 5, 50, (50, 200, 0), (25, 100, 0), pos_type=0,
                         font_color=(0, 0, 255))
custom_button = Button("Custom;match", 300, 75, (700, 600), 5, 40, (50, 200, 0), (25, 100, 0), pos_type=0,
                       font_color=(0, 0, 255))
next_button = Button("Next", 200, 50, (1075, 750), 5, 40, (50, 200, 0), (25, 100, 0), pos_type=1,
                     font_color=(0, 0, 255))
#
slots = Slots(250, 500, 100, 100, items, 4,[30,40,20,8,2], gap=100)


snow = Snowfall(screen,"snow.png")

maps=         ["luźny lasek.png","pustynna przeszkoda.png","białe bezdroża.png"]
backgrounds = [["luźny_lasek.png",False],["pustynna_przeszkoda.png","pustynna przeszkoda most.png"],["białe_bezdroża.png","białe bezdroża most.png"]]

check_points = [Check_points([pg.Rect(39, 379, 160, 58), pg.Rect(250, 560, 120, 120),
                              pg.Rect(825, 130, 120, 120), pg.Rect(1000, 379, 160, 58), pg.Rect(825, 540, 120, 140),
                              pg.Rect(250, 130, 120, 120)]),

                Check_points([pg.Rect(200, 600, 30, 200), pg.Rect(1000, 600, 180, 180), pg.Rect(800, 240, 120, 120),
                              pg.Rect(280, 440, 120, 140), pg.Rect(10, 280, 200, 50), pg.Rect(180, 10, 80, 200)
                                 , pg.Rect(1000, 10, 180, 180), pg.Rect(1000, 280, 200, 50),
                              pg.Rect(800, 440, 120, 140), pg.Rect(280, 240, 120, 120), pg.Rect(10, 550, 200, 30)
                              ]),
                Check_points([pg.Rect(1000, 650, 30, 140), pg.Rect(180, 650, 30, 140), pg.Rect(-10, 600, 200, 30),
                              pg.Rect(20, 200, 170, 30), pg.Rect(200, 25, 30, 180)
                                 , pg.Rect(830, 420, 30, 230), pg.Rect(880, 360, 150, 30),
                              pg.Rect(870, 185, 30, 160),pg.Rect(385, 470, 30, 170),pg.Rect(180, 475, 170, 30),
                              pg.Rect(330, 260, 30, 210),pg.Rect(785, 20, 30, 150),pg.Rect(1005, 20, 30, 170),
                              pg.Rect(1035, 170, 150, 30),pg.Rect(1035, 615, 150, 30)])]

under_ways = [Under_points([], []), Under_points(
    [pg.Rect(1000, 210, 200, 20), pg.Rect(850, 430, 20, 160), pg.Rect(0, 210, 200, 20), pg.Rect(330, 430, 40, 160)],
    [pg.Rect(1000, 180, 220, 30), pg.Rect(830, 400, 20, 200), pg.Rect(0, 180, 220, 30), pg.Rect(370, 400, 20, 200)]),
    Under_points(
    [pg.Rect(210, 16, 20, 200), pg.Rect(870, 420, 20, 230)],
    [pg.Rect(190, 16, 30, 200), pg.Rect(890, 420, 20, 230)])]

start_positions = [[(60, 405), (110, 405), (170, 405), (85, 330), (155, 330)],
                   [(100, 700), (100, 735), (100, 770), (50, 770), (50, 735)], [(1000, 675), (1000, 720), (1000, 770),(1080, 690), (1080, 750)]]
angles = [-90, 0,180]
inventory_display = Inventory_Display([0, 400], [1200, 400], eq, 8, 0, 50, 50, 50, "black", (204, 229, 255), 0)
laps = [1, 1, 4]

gold_rewards = [[100, 50, 20,0,0], [100 * 2, 50 * 2, 20 * 2,0,0], [100 * 3, 50 * 3, 20 * 3,0,0]]
gem_rewards = [[10, 5, 2,0,0], [10 * 2, 5 * 2, 2 * 2,0,0], [10 * 3, 5 * 3, 2 * 3,0,0]]
gold_time_bonuses = [(100, 6), (200, 20), (100, 6)]
gem_time_bonuses = [(10, 6), (20, 20), (10, 6)]
lock_img = pg.transform.scale(pg.image.load("lock.png"), (40, 60))
best_times = []
map_snippets = Map_snippets(230, 300, 300, 200, [i[0] for i in backgrounds], laps, gold_rewards, gem_rewards, unlocked_maps, lock_img, gap=130)

bananas = []

oil_stains=[]

nitro_uses_label = Simple_label([480, 750], 200, "x6", 50, (0, 255, 0),pos_type=1)
nitro_icon= pg.Surface((100,100))
pg.draw.circle(nitro_icon,(150,150,150),(50,50),50)
nitro_icon.blit(pygame.transform.scale(pygame.image.load('nitro_icon.png'),[100,100]),(0,0))


barier_icon= pg.Surface((100,100))
pg.draw.circle(barier_icon,(150,150,150),(50,50),50)
pygame.draw.rect(barier_icon, (25,5,0), ((38, 5), (25, 90)))
barrier_uses_label = Simple_label([680, 750], 200, "x6", 50, (0, 255, 0),pos_type=1)



banana_icon = pygame.Surface((100,100))
pg.draw.circle(banana_icon,(150,150,150),(50,50),50)
banana_icon.blit(pygame.transform.scale(pygame.image.load('banana_peel.png'), [100,100]),(0,0))
banana_uses_label = Simple_label([880, 750], 200, "x6", 50, (0, 255, 0),pos_type=1)


oil_icon = pygame.Surface((100,100))
pg.draw.circle(oil_icon,(150,150,150),(50,50),50)
oil_icon.blit(pygame.transform.scale(pygame.image.load('Oil.png'), [100,100]),(0,0))
oil_uses_label = Simple_label([880, 750], 200, "x6", 50, (0, 255, 0),pos_type=1)

biomes = ["normal","sand","snow"]
vamp_icon,load_icon=id_to_items([17,18],items)
icons=Icons([vamp_icon.surf,load_icon.surf,oil_icon,barier_icon,banana_icon,nitro_icon],[100,100],[(100,680),(100,680),(300,680),(500,680),(700,680),(900,680)],["","","","","","",""])

previous_page = 0


pygame.mixer.music.play(-1)

# 0.3 at the beginning
pygame.mixer.music.set_volume(adjust_volume(start_musik_volume))
set_sfx_volume(start_sfx_volume)

start_cooldown = 180

enemies_stats=[[[5],[8,4],[],[8,4,0],[7,3,0]],[[7],[10,5],[],[10,5,0],[8.5,3,0]],[[8],[10,5],[],[10,5,0],[8,3,0]]]

sort_items(items)

run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    keys = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()
    mouse_pos = mouse_pos[0] * scale_x, mouse_pos[1] * scale_y
    # Check events
    for event in events:
        if event.type == pg.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            if page == 7:
                # inventory_display.scroll -= event.y * 15

                inventory_display.scroll = max(inventory_display.scroll - event.y * 10, 0)
                if inventory_display.eq != []:
                    inventory_display.scroll = min(
                        inventory_display.scroll + inventory_display.eq[-1].rect.y + inventory_display.eq[-1].h -
                        inventory_display.pos[1] - inventory_display.h + inventory_display.end_gap,
                        inventory_display.scroll)

    # if keys[pg.K_ESCAPE]:
    #     run = False

    # Start screen
    if page == 2:

        screen.fill((0, 0, 0))
        play_button.check_click(mouse_pos, mouse_pressed)
        shop_button.check_click(mouse_pos, mouse_pressed)
        inventory_button.check_click(mouse_pos, mouse_pressed)
        settings_button.check_click(mouse_pos, mouse_pressed)
        replays_button.check_click(mouse_pos, mouse_pressed)
        if play_button.do:
            page = 5
            previous_page = 2
            bananas = []

            oil_stains=[]

        if replays_button.do:
            page = 12
            previous_page = 2
            replays_snippets.load()
        elif shop_button.do:
            page = 4
            # slots.roll(10)
            previous_page = 2
        elif inventory_button.do:
            page = 7
            inventory_page = 0
            previous_page = 2
        elif settings_button.do:
            settings_screen.active = True
            previous_page = 2
            page = 14


        start_label.draw(screen)
        play_button.draw(screen)
        shop_button.draw(screen)
        inventory_button.draw(screen)
        settings_button.draw(screen)
        replays_button.draw(screen)
    elif page == 12:
        screen.fill(0)
        a = replays_snippets.update(mouse_pos, mouse_pressed)
        if a != -1:
            page = 13
            replay.load(a)
            previous_page = 12
        replays_snippets.draw(screen)
        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = 2
        back_button.draw(screen)
    elif page == 13:
        screen.fill(0)
        replay.update(mouse_pos, mouse_pressed, keys)
        if replay.Quit:
            page = 12
        replay.draw(screen)

    # Shop
    elif page == 4:
        screen.fill((0, 0, 0))
        screen.blit(coinimg, (0, 5))
        coin_label.update_text(f": {coinamount}")
        coin_label.draw(screen)

        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = previous_page
        back_button.draw(screen)

        screen.blit(gemimg, (-2, 55))
        gem_label.update_text(f": {gemamount}")
        gem_label.draw(screen)

        roll.check_click(mouse_pos, mouse_pressed)
        if roll.do and coinamount >= 10:
            coinamount-=10
            slots.roll(15)
        roll.draw(screen)
        slots.update()
        bought = slots.sell(mouse_pressed, mouse_pos)
        if bought:
            if bought.type == "talisman" and gemamount >= bought.price:
                gemamount-=bought.price
                slots.roll(15)
                sounds['buying'].play()
                inventory_display.eq.append(bought)
            elif coinamount >= bought.price and bought.type!="talisman":
                coinamount -= bought.price
                slots.roll(15)
                sounds['buying'].play()
                inventory_display.eq.append(bought)


        slots.draw(screen, mouse_pos)

        slots.draw(screen, mouse_pos)
    elif page == 5:
        screen.fill((0, 0, 0))
        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = 2

        campaign_button.check_click(mouse_pos, mouse_pressed)
        if campaign_button.do:
            page = 5.5
            map_snippets.campaign()
            game_mode = 0
        custom_button.check_click(mouse_pos, mouse_pressed)
        if custom_button.do:
            page = 8
            previous_page = 5
            map_snippets.custom()
            game_mode = 1
        back_button.draw(screen)
        campaign_button.draw(screen)
        custom_button.draw(screen)


    elif page == 5.5:

        screen.fill((60, 0, 100))
        map_pick = map_snippets.update(mouse_pos, mouse_pressed)
        if map_pick != -1:
            sounds['start_countdown'].play()
            background = get_background(backgrounds[map_pick][0], screen_width, screen_height)
            bridge = 0
            if backgrounds[map_pick][1]:
                bridge = pygame.transform.scale(pygame.image.load(backgrounds[map_pick][1]),

                                                [screen_width, screen_height]).convert_alpha()

            map = mapping(maps[map_pick], screen_width, screen_height, tile_size)
            page = 6
            types = [3, 1, 2, 4, 5]
            names = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]
            time_table.intialise(laps[map_pick], names)
            enemys_items=give_items(map_pick)
            enemys_items=[dict_ids_to_items(i ,items) for i in enemys_items]
            for j, i in enumerate(enemys):
                if types[j] == 0:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j])
                if types[j] == 1:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j],
                                 max_v=enemies_stats[map_pick][types[j] - 1][0],
                                 items=enemys_items[j-1])
                if types[j] == 2:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j],
                                 max_v=enemies_stats[map_pick][types[j] - 1][0],
                                 max_t_v=enemies_stats[map_pick][types[j] - 1][1], items=enemys_items[j-1])
                if types[j] == 3:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j])
                    player = j
                if types[j] == 4:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j],
                                 max_v=enemies_stats[map_pick][types[j] - 1][0],
                                 max_t_v=enemies_stats[map_pick][types[j] - 1][1], target=0, items=enemys_items[j-1])
                if types[j] == 5:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], types[j], laps[map_pick], name=names[j],
                                 max_v=enemies_stats[map_pick][types[j] - 1][0],
                                 slowing_speed=enemies_stats[map_pick][types[j] - 1][1], target=0, items=enemys_items[j-1])
            current_check_points = check_points[map_pick]
            current_under_ways = under_ways[map_pick]
            place = 0
            players_q = sum([1 if i != 0 else 0 for i in types])
            start_cooldown = 180
            if enemys[0].items["nitro"].id==17:
                icons.set_active([1,0,1, 1, 1, 1])
            elif enemys[0].items["nitro"].id==16:
                icons.set_active([0,1,1, 1, 1, 1])
            else:
                icons.set_active([0,0,1, 1, 1, 1])
            icons.set_max_values([enemys[0].vamp_nitro_max,enemys[0].loading_nitro_max,enemys[0].oil_cooldown, enemys[0].barrier_cooldown, enemys[0].banana_cooldown,
                                  enemys[0].items["nitro"].delay])
            player = 0

        map_snippets.draw(screen, mouse_pos)
        back_button.check_click(mouse_pos, mouse_pressed)

        if back_button.do:
            page = previous_page
        back_button.draw(screen)

    elif page == 9:
        screen.fill((60, 0, 100))
        map_pick = map_snippets.update(mouse_pos, mouse_pressed)
        if map_pick != -1:
            background = get_background(backgrounds[map_pick][0], screen_width, screen_height)
            bridge = 0
            if backgrounds[map_pick][1]:
                bridge = pygame.transform.scale(pygame.image.load(backgrounds[map_pick][1]),
                                                [screen_width, screen_height])
                print(bridge)
            map = mapping(maps[map_pick], screen_width, screen_height, tile_size)
            page = 6
            player=-1
            for j, i in enumerate(enemys):
                if info[j][0] == 0:

                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1])
                if info[j][0] == 1:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1], max_v=info[j][2],
                                 items=info[j][5])
                if info[j][0] == 2:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1], max_v=info[j][2],
                                 max_t_v=info[j][3], items=info[j][5])
                if info[j][0] == 3:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1], items=info[j][5])
                    player=j
                if info[j][0] == 4:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1], max_v=info[j][2],
                                 max_t_v=info[j][3], target=info[j][4], items=info[j][5])
                if info[j][0] == 5:
                    i.initialise(check_points[map_pick], start_positions[map_pick][j][0],
                                 start_positions[map_pick][j][1],
                                 angles[map_pick], info[j][0], laps[map_pick], name=info[j][1], max_v=info[j][2],
                                 slowing_speed=info[j][3], target=info[j][4], items=info[j][5])
            names = [i[1] for i in info]
            types = [i[0] for i in info]
            print(names)
            time_table.intialise(laps[map_pick], names)
            current_check_points = check_points[map_pick]
            current_under_ways = under_ways[map_pick]
            place = 0
            players_q = sum([1 if i != 0 else 0 for i in types])
            if player!=-1:
                if enemys[player].items["nitro"].id==18:
                    icons.set_active([1,0,1, 1, 1, 1])
                elif enemys[player].items["nitro"].id==17:
                    icons.set_active([0,1,1, 1, 1, 1])
                else:
                    icons.set_active([0,0,1, 1, 1, 1])
                icons.set_max_values([enemys[player].vamp_nitro_max,enemys[player].loading_nitro_max,enemys[player].oil_cooldown, enemys[player].barrier_cooldown, enemys[player].banana_cooldown,
                                      enemys[player].items["nitro"].delay])
            else:
                icons.set_active([0,0,0, 0, 0, 0])
        map_snippets.draw(screen, mouse_pos)

        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = 8
        back_button.draw(screen)

    # Game screen (Car & FPS)
    elif page == 6:
        screen.blit(background, (0, 0))
        zero = []
        # start_cooldown = max(start_cooldown - 1, -5)
        # if start_cooldown > -5:
        #     if start_cooldown <= 179:
        #         three_label.draw(screen)
        #     if start_cooldown <= 130:
        #         two_label.draw(screen)
        #     if start_cooldown <= 80:
        #         one_label.draw(screen)
        #     if start_cooldown <= 20:
        #         startt_label.draw(screen)
        # current_check_points.draw(screen)
        # current_under_ways.draw(screen)
        if start_cooldown:
            if pause_screen.active == False:
                if console.active == 0:
                    for i in enemys:
                        a = i.update(keys, screen, enemys, map, current_check_points, current_under_ways,True if biomes[map_pick]=="snow" else False,console,map_pick)
                        time_table.update(enemys,console)
                        if a == 2:
                            page = 10
                            sounds['ending'].play()

                            get_player_info(place, enemys, laps[map_pick], game_results, time_table, players_q,
                                            backgrounds[map_pick][0], gold_rewards, gold_time_bonuses
                                            , gem_rewards, gem_time_bonuses, game_mode, map_pick)
                            if game_mode == 0:
                                map_snippets.update_records(time_table.lap_times[0], map_pick)
                                if place == 0:
                                    if map_pick != len(maps):
                                        map_snippets.unlock(map_pick + 1)
                                        unlocked_maps[map_pick + 1] = 1
                            break
                        elif a == 1:
                            place += 1
                            # print(place)
                            if place == players_q:
                                page = 10
                                sounds['ending'].play()
                                get_player_info(place, enemys, laps[map_pick], game_results, time_table, players_q,
                                                backgrounds[map_pick][0], gold_rewards, gold_time_bonuses
                                                , gem_rewards, gem_time_bonuses, game_mode, map_pick)
                                break
                        # print(i.type)

                        if i.banana:
                            bananas.append(i.banana)
                        if i.oil:
                            oil_stains.append(i.oil)
                    time_table.draw(screen)
            else:
                console.active = 0

        for b in bananas.copy():
            if b.update(enemys):
                bananas.remove(b)
            else:
                if b.level == 0:
                    b.draw(screen)
                else:
                    zero.append(b)

        for b in oil_stains.copy():
            if b.update(screen, enemys):
                oil_stains.remove(b)
            else:
                if b.level == 0:
                    b.draw(screen)
                else:
                    zero.append(b)

        for i in enemys:
            if i.level == 0:
                i.draw(screen)
                if i.barrier:
                    i.barrier.draw(screen)
            else:
                zero.append(i)
                if i.barrier:
                    zero.append(i.barrier)
        if bridge:
            screen.blit(bridge,[0,0])
        for z in zero:
            z.draw(screen)

        if biomes[map_pick] == "snow":
            snow.update()
            snow.draw()

        if player!=-1:
            if enemys[player].in_snow:
                snow_surface=pg.Surface((screen_width,screen_height))
                snow_surface.fill((255,255,255))
                snow_surface.set_alpha(int(255*enemys[player].in_snow/enemys[player].in_snow_max))
                screen.blit(snow_surface,(0,0))
            icons.check_collisions(enemys)
            icons.update_labels(["","",f"{enemys[player].oil_uses}x",f"{enemys[player].barrier_uses}x",
                                 f"{enemys[player].banana_uses}x",f"{enemys[player].nitro_uses}x"])
            icons.draw(screen,[(enemys[player].vamp_nitro_max - enemys[player].additional_power),(enemys[player].loading_nitro_max - enemys[player].additional_power),enemys[player].oil_ready,enemys[player].barrier_ready,enemys[player].banana_ready,
                               enemys[player].nitro_delay if not enemys[player].nitro_duration else enemys[player].items["nitro"].delay])
        pause_screen_val = pause_screen.update(keys, mouse_pos, mouse_pressed)

        settings_screen.musik_slider.value = pause_screen.musik_slider.value
        settings_screen.musik_slider.ppos = pause_screen.musik_slider.ppos

        settings_screen.SFX_slider.value = pause_screen.SFX_slider.value
        settings_screen.SFX_slider.ppos = pause_screen.SFX_slider.ppos

        pygame.mixer.music.set_volume(adjust_volume(pause_screen.musik_slider.value / 100))
        set_sfx_volume(pause_screen.SFX_slider.value / 100)
        if pause_screen_val == 1:
            page = 2
        elif pause_screen_val == 2:
            console.active = 1
        elif pause_screen_val == 3:
            page = 11
            previous_page = 6



        console.update(mouse_pos, mouse_pressed, keys, enemys)
        if console.unlock_everything:
            inventory_display.eq = items
        elif console.give_gold:
            coinamount+=999999
        elif console.give_gems:
            gemamount+=999999
        console.draw(screen)
        pause_screen.draw(screen)
    elif page == 10:
        screen.fill((0, 0, 0))
        game_results.update(mouse_pos, mouse_pressed, keys, enemys)
        if game_results.console.unlock_everything:
            inventory_display.eq=items
        elif game_results.console.give_gold:
            coinamount+=999999
        elif game_results.console.give_gems:
            gemamount+=999999

        if game_results.quit:
            page = 2
            coinamount += game_results.total_coins
            gemamount += game_results.total_gems
            console.clear()
        game_results.draw(screen,mouse_pos)
    elif page == 8:
        screen.fill((0, 0, 0))
        a = -1
        if items_chooser.active == False:
            a = player_slots.update(mouse_pos, mouse_pressed, keys)
        b = items_chooser.update(mouse_pos, mouse_pressed)
        if a != -1:
            items_chooser.initialise(a[0], (screen_width // 2 - 250, screen_height // 2 - 350), a[1])
        if b:
            player_slots.switch_items(b[0], b[1])
        player_slots.draw(screen, mouse_pos)
        items_chooser.draw(screen, mouse_pos)
        back_button.draw(screen)
        next_button.draw(screen)

        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = previous_page
        next_button.check_click(mouse_pos, mouse_pressed)
        if next_button.do:
            a, j = player_slots.check()
            if a:
                if a == 1:
                    bug_message.initialise(screen_width // 2, 50, 500, f"Car {j + 1} does;not have a name", 600)
                elif a == 2:
                    bug_message.initialise(screen_width // 2, 50, 500, f"Car {j + 1} does;not have a max speed", 600)
                elif a == 3:
                    bug_message.initialise(screen_width // 2, 50, 500, f"Car {j + 1} does;not have a max turn speed",
                                           600)
                elif a == 4:
                    bug_message.initialise(screen_width // 2, 50, 500, f"Car {j + 1} does;not have a slowing speed",
                                           600)
                elif a == 5:
                    bug_message.initialise(screen_width // 2, 50, 500, f"Car {j + 1} has;target of type None", 600)
                elif a == 6:
                    bug_message.initialise(screen_width // 2, 50, 500, f"There are too;many players", 600)
            else:
                info = player_slots.ret_info()
                page = 9



    elif page == 7:

        screen.fill("black")

        print(enemys[0].items['tires'].rect.x, enemys[0].items['tires'].rect.x)

        inventory_display.update(mouse_pos, mouse_pressed)

        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = previous_page
            inventory_display.scroll = 0

        inventory_display.set_pos(mouse_pressed, mouse_pos, enemys[0])

        inventory_display.draw(screen, mouse_pos, enemys[0])

        back_button.draw(screen)

    elif page == 11:
        screen.fill("black")
        for label in keybind_labels:
            label.draw(screen)

        back_button.check_click(mouse_pos, mouse_pressed)
        if back_button.do:
            page = previous_page
            if previous_page == 14:
                settings_screen.active = True

        back_button.draw(screen)

        for keybind_button in keybind_buttons:
            keybind_button.update(enemys[0], mouse_pos, mouse_pressed, keys)
            keybind_button.draw(screen)



    elif page == 14:
        pygame.draw.rect(screen, "black", ([screen_width, screen_height], [0, 0]))
        # start_cooldown = max(start_cooldown - 1, -5)
        # if start_cooldown > -5:
        #     if start_cooldown <= 179:
        #         three_label.draw(screen)
        #     if start_cooldown <= 130:
        #         two_label.draw(screen)
        #     if start_cooldown <= 80:
        #         one_label.draw(screen)
        #     if start_cooldown <= 20:
        #         startt_label.draw(screen)
        # current_under_ways.draw(screen)
        # current_check_points.draw(screen)

        if settings_screen.active == False:
            if console.active == 0:
                page = 2
        else:
            console.active = 0

        pause_screen_val = settings_screen.update(keys, mouse_pos, mouse_pressed)
        pygame.mixer.music.set_volume(adjust_volume(settings_screen.musik_slider.value / 100))
        pause_screen.musik_slider.value = settings_screen.musik_slider.value
        pause_screen.musik_slider.ppos = settings_screen.musik_slider.ppos
        set_sfx_volume(settings_screen.SFX_slider.value / 100)
        pause_screen.SFX_slider.value = settings_screen.SFX_slider.value
        pause_screen.SFX_slider.ppos = settings_screen.SFX_slider.ppos

        if pause_screen_val == 2:
            console.active = 1
        elif pause_screen_val == 3:
            page = 11
            previous_page = 14

        console.update(mouse_pos, mouse_pressed, keys, enemys)
        if console.unlock_everything:
            inventory_display.eq = items
        elif console.give_gold:
            coinamount+=999999
        elif console.give_gems:
            gemamount+=999999

        console.draw(screen)
        settings_screen.draw(screen)

    bug_message.draw(screen)
    if console.show_fps:
        rfps = clock.get_fps()
        rfps_label.update_text(f"fps: {int(rfps)}")
        rfps_label.draw(screen)

    show_screen.blit(pg.transform.scale(screen, (show_width, show_height)), (0, 0))
    pg.display.flip()
save(coinamount, gemamount, [enemys[0].items[i].id for i in enemys[0].items], sum(unlocked_maps), [i.id for i in eq])
pg.quit()