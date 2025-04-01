import pygame as pg
import pygame.mixer
pygame.mixer.init()
screen_width=1200
screen_height=800
tile_size=2
display_info = pg.display.Info()
show_width= 1200#display_info.current_w
show_height=800#display_info.current_h
scale_x=screen_width/show_width
scale_y=screen_height/show_height
fps=60
tw=screen_width//tile_size
th=screen_height//tile_size
run=True

wall=1
asphalt_friction=0.69
ice_friction=0.5
ice = 2
sand = 3
sztutr = 4
underway=-1
sand_friction=1.4
barrier = 1.5
underway_barrier = -1.5

start_musik_volume = 0.1
start_sfx_volume = 0.3

items_pos = {
    'tires': [300, 100],
    'talisman': [500,100],
    'engine': [700,100],
    'nitro': [900,100],

}
# tires_pos = [300,100]
# armor_pos = [500,100]
# engine_pos = [700,100]
# nitro_pos = [900,100]

sounds = {
    'buying': pygame.mixer.Sound('buying.wav'),
    'click': pygame.mixer.Sound('click.wav'),
    'equipping': pygame.mixer.Sound('equipping.wav'),
    'slots': pygame.mixer.Sound('slots.wav'),
    'start_countdown': pygame.mixer.Sound('start_countdown.wav'),
    'ending': pygame.mixer.Sound('ending.wav'),
}

pygame.mixer.music.load('tycoon_ahh_music.mp3')
new_replay_save="NewReplaySave "
next_lap="NextLap "
new_player="NewPlayer "
save_snippet="SaveSnippet "
general_info="GeneralInfo "