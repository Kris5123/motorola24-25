import random

import pygame
import math

from banana import *
from settings import *
from assets import *
from mapa import *
from item import *

from barrier import Barrier, barrier_terrain_check
from InventoryDisplay import items_pos

global id_num
id_num = 0

from InventoryDisplay import items_pos
import numpy as np


class Car_():
    def __init__(self):
        self.original_image = pygame.transform.scale(pygame.image.load("car2.png"), (45, 25))

        self.x = 0
        self.y = 0

        # orientation
        self.angle = 0
        self.rects = [
            pygame.Rect(self.x + math.sin(self.angle + 90) * 4, self.y + math.cos(self.angle + 90) * 4, 25, 25),
            pygame.Rect(self.x + math.sin(self.angle - 90) * 4, self.y + math.cos(self.angle - 90) * 4, 25, 25)]
        self.rotation_vel = 4
        self.direction = 0
        self.rect = self.original_image.get_rect()

        self.banana_cooldown = 120
        self.banana_ready = self.banana_cooldown
        self.banana_uses = 3

        self.keybinds = {
            "drive_forwards": pygame.K_w,
            "drive_backwards": pygame.K_s,
            "turn_left": pygame.K_a,
            "turn_right": pygame.K_d,
            "use_nitro": pygame.K_LCTRL,
            "spawn_banana": pygame.K_SPACE,
            "spawn_barrier": pygame.K_e,
            "spawn_oil": pygame.K_q
        }

        self.items = {
            "tires": items[-1].copy(),
            "talisman": items[20].copy(),
            "engine": items[10].copy(),
            "nitro": items[7].copy()
        }

        for i in self.items:
            self.items[i].rect.x, self.items[i].rect.y = items_pos[i][0], items_pos[i][1]

        # self.items['tires'].rect.x, self.items['tires'].rect.y = items_pos['tires'][0], items_pos['tires'][1]
        # self.items['armor'].rect.x, self.items['armor'].rect.y = items_pos['armor'][0], items_pos['armor'][1]
        # self.items['engine'].rect.x, self.items['engine'].rect.y = items_pos['engine'][0], items_pos['engine'][1]
        # self.items['nitro'].rect.x, self.items['nitro'].rect.y = items_pos['nitro'][0], items_pos['nitro'][1]

        self.bounce_vector = pygame.math.Vector2(0, 0)

        # velocity vectors
        self.vel_vector = pygame.math.Vector2(0, 0)
        self.accelerate_vector = pygame.math.Vector2(0, 0)

        # moc
        # self.items["engine"].power
        self.boost_power = 1000
        self.curr_boost = 0
        # masa auta
        self.masa_karoserii = 1600

        self.mass = self.masa_karoserii + self.items["tires"].mass + self.items["engine"].mass + self.items[
            "nitro"].mass
        # siły:
        self.force_vec = pygame.Vector2(0, 0)
        # siła napędu
        self.drive_force = pygame.Vector2(0, 0)

        # siły tarcia
        self.friction = 0.1

        self.brakes_speed = 0.1
        self.curr_brakes = 0
        self.brakes_max_friction = 150

        # siła ciężkości
        self.weight = self.mass * 10
        # siła odśrodkowa
        self.centrifugal_force = pygame.Vector2(0, 0)

        self.speed = 4
        self.max_vel = 8
        self.max_acc = 8

        self.bouncy = 1
        self.acc = 0
        # particles
        # nitro
        self.nitro_duration = 0
        self.nitro_delay = self.items["nitro"].dur
        self.nitro_vector = pygame.math.Vector2(0, 0)
        self.nitro_uses = 3

        self.particles = []
        self.particle_random = 20

        self.bullets = []
        self.bullet_delay = 10

        self.previous_pos = [self.x, self.y]
        self.agro = 0
        self.type = 0
        # type 1

        global id_num
        self.id = id_num
        id_num += 1
        self.wall = wall
        self.barrier_wall = barrier

    def set_item_pos(self):
        for i in self.items:
            self.items[i].rect.x, self.items[i].rect.y = items_pos[i][0], items_pos[i][1]

    def initialise(self, check_points, x, y, angle, type, laps, name="", max_v=0, max_t_v=0, slowing_speed=0, target=0,
                   biome='normal', items=0):
        self.previous_items = self.items.copy()
        print(items, "CZarnuch")
        if items:
            self.items = items
        self.a = type
        self.type = type
        self.laps = laps
        # if self.type == 3:
        #     print("sdfhdfssdfsd")
        #     self.tires.rect.x, self.tires.rect.y = tires_pos[0], tires_pos[1]
        #     self.armor.rect.x, self.armor.rect.y = armor_pos[0], armor_pos[1]
        #     self.engine.rect.x,self.engine.rect.y = engine_pos[0], engine_pos[1]
        #     self.nitro.rect.x, self.nitro.rect.y = nitro_pos[0], nitro_pos[1]
        self.in_snow=0
        self.in_snow_max=60*3
        self.name = name
        self.font = pg.font.SysFont("Arial", 10)
        name = text(self.font, self.name, (255, 255, 255))
        self.name_surface = pg.surface.Surface((name[1], name[2]), pg.SRCALPHA)
        self.name_surface.fill((0, 0, 0, 100))
        self.name_surface.blit(name[0], (0, 0))
        if self.type == 1:
            if max_v:
                self.max_v = max_v
            else:
                self.max_v = 8
            self.min_dist = 70
        # type2
        if self.type == 2:
            print(max_v, max_t_v)
            if max_v:
                self.max_v = max_v
            else:
                self.max_v = 20
            if max_t_v:
                self.max_turn_v = max_t_v
            else:
                self.max_turn_v = 15
            self.turn = 0
            self.min_dist = 50
            self.turn_dist = 20
        if self.type == 4:
            if max_v:
                self.max_v = max_v
            else:
                self.max_v = 10
            if max_t_v:
                self.max_turn_v = max_t_v
            else:
                self.max_turn_v = 5
            self.turn = 0
            self.min_dist = 50
            self.turn_dist = 100
            self.agro_angle = 100
            self.agro_target = target
        if self.type == 5:
            if max_v:
                self.max_v = max_v
            else:
                self.max_v = 5
            self.min_dist = 70
            if slowing_speed:
                self.slowing_speed = slowing_speed
            else:
                self.slowing_speed = 2
            self.slowing_speed2 = 1
            self.agro2 = 0
            self.agro_target = target
        self.check_point = 1
        target_r = 50
        self.targets = [Circle(i.centerx, i.centery, target_r) for i in check_points.check_points]
        self.target = 1
        # track
        self.lap = 0
        self.laps_time = []
        self.lap_time = pygame.time.get_ticks()
        self.time_lap_list = Simple_list([1000, 0], 200, [], 40, (255, 0, 0))
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.update_rects()
        self.banana = False
        self.count_tick = fps
        self.cur_tick = self.count_tick
        self.vel_sum = [0, 0]
        self.highest_vel = 0
        self.hv = []
        self.average_v = []

        self.explosion_vector=pg.math.Vector2(0,0)

        self.replay = [[]]
        self.replay_cooldown = 2
        self.cur_replay_cooldown = 0

        self.banana_cooldown = 60 * 5
        self.banana_ready = self.banana_cooldown
        self.banana_uses = 2

        self.oil_cooldown = 60 * 5
        self.oil_ready = self.oil_cooldown
        self.oil_uses = 3
        self.oil_duration = 60 * 5

        self.barrier = False
        self.barrier_cooldown = 1200
        self.barrier_ready = 0
        self.barrier_uses = 2
        self.level = 0
        self.wall = wall
        self.barrier_wall = barrier
        self.nitro_uses = 3
        self.r=0
        # Items Variables

        self.using_nitro = False

        self.mass = self.masa_karoserii + self.items["tires"].mass + self.items["engine"].mass + self.items[
            "nitro"].mass

        self.gem_multiplier = 0
        self.coin_multiplier = 0

        self.biome = biome  # normal/snow/sand

        self.power_multiplier = 1

        self.ticks = 0

        self.banana_immunity = False

        self.un = False
        self.additional_power = 0

        self.banana_effect_duration = 60*1
        self.banana_effect = 0

        self.oil_effect_duration = 30
        self.oil_effect = 0
        self.oil_effect_angle = 5

        self.banana_effect_angle = 4
        self.go_back = False

        self.using_nitro = False
        self.oil = False

        self.nitro_delay = self.items["nitro"].delay
        self.curr_boost = 0
        self.vamp_nitro_max=self.items["nitro"].power
        self.loading_nitro_max=self.items["nitro"].power
        self.sztutr=False
        self.sztutr_immunity = False
        self.calculate_onetime_items_effects()
    def finish_race(self):
        self.items = self.previous_items.copy()

    def calculate_onetime_items_effects(self):
        for i in self.items:
            if self.items[i].id == 14:  # nieskończone nitro
                self.nitro_uses = 99999

            if self.items[i].id == 21:  # zimowy silnik
                if self.biome == 'snow':
                    self.power_multiplier += 0.15

            elif self.items[i].id == 22:  # piaskowy silnik
                if self.biome == 'sand':
                    self.power_multiplier += 0.15

            elif self.items[i].id == 25:  # złoty silnik
                self.coin_multiplier += 0.5
            elif self.items[i].id == 26:  # gemowy silnik

                self.gem_multiplier += 0.5
            elif self.items[i].id == 36:  # złoty opony
                self.coin_multiplier += 0.5
            elif self.items[i].id == 37:  # gemowy opony
                self.gem_multiplier += 0.5
            elif self.items[i].id == 38:  # sztutrowe opony
                self.sztutr_immunity = True
            elif self.items[i].id == 35:  # profesjonalne opony
                self.sztutr_immunity = True
            elif self.items[i].id == 41:  # tazliman mocy
                self.power_multiplier += 0.15
            elif self.items[i].id == 42:  # tazliman bananowoskórkowej odpornośći
                self.banana_immunity = True
            elif self.items[i].id == 43:  # tazliman golda
                self.coin_multiplier += 0.5
            elif self.items[i].id == 44:  # tazliman diamenów
                self.gem_multiplier += 0.5
            elif self.items[i].id == 45:  # tazliman złoto-diamentowy
                self.coin_multiplier += 0.5
                self.gem_multiplier += 0.5
            elif self.items[i].id == 48:  # tazliman mniejszej masy
                self.mass *= 0.85
            elif self.items[i].id == 49:  # tazliman większej masy
                self.mass *= 1.15
            elif self.items[i].id == 47:  # tazliman nitra daje nitro uses *2 INNE NITROWE ITEMY MUSZĄ BYĆ WYŻEJ!!!!
                self.nitro_uses *= 2
            elif self.items[i].id == 46:  # tazliman banana daje banana uses *2 i cooldown/2
                self.banana_uses *= 2
                self.banana_cooldown /= 2
            elif self.items[i].id == 410:  # tazliman banana daje banana uses *2 i cooldown/2
                self.banana_uses *= 2
                self.nitro_uses *= 2
                self.barrier_uses *= 2
                self.oil_uses_uses *= 2


    def calculate_dynamic_items_effects(self, keys, players, map):
        self.ticks += 1
        for i in self.items:
            # bananowenitro
            if self.items[i].id == 16:

                if self.using_nitro and banana_terrain_check([int(self.x + (self.x - self.rects[0].centerx) * 6) - 25,
                                                              int(self.y + (self.y - self.rects[0].centery) * 6) - 25],
                                                             map):
                    self.banana = Banana([int(self.x + (self.x - self.rects[0].centerx) * 6) - 25,
                                          int(self.y + (self.y - self.rects[0].centery) * 6) - 25])
            if self.items[i].id == 18:
                if self.nitro_duration == 0:
                    if self.additional_power < self.loading_nitro_max:
                        self.additional_power += 745 / 60
            if self.items[i].id == 17:
                if self.nitro_duration == 0:
                    if self.additional_power < self.vamp_nitro_max:
                        self.r = 200
                        for j in players:
                            if j.id != self.id and pythagoras2(self.x - j.x, self.y - j.y) < self.r ** 2:
                                self.additional_power += 745 / 60 * 5




            elif self.items[i].id == 23:  # bananowy silnik
                if self.ticks % (60 * 10) == 0:
                    self.banana_uses += 1

            elif self.items[i].id == 24:  # stolarski silnik
                if self.ticks % (60 * 15) == 0:
                    self.barrier_uses += 1
    def explosion(self,x,y):
        r=pythagoras(x-self.x,y-self.y)
        power=2000000/r
        self.explosion_vector.x=math.cos((self.x-x)/(self.y-y))*power*-1
        self.explosion_vector.y=math.sin((self.x-x)/(self.y-y))*power*-1
        print(self.explosion_vector)
    def boost(self, keys,enemies):
        if self.type == 3:
            if self.nitro_delay > 0:
                self.nitro_delay -= 1
            elif self.un == False and self.nitro_duration == 0 and keys[
                self.keybinds['use_nitro']] and self.nitro_uses > 0:
                self.nitro_uses -= 1
                self.curr_boost = self.items["nitro"].power + self.additional_power
                self.nitro_duration = self.items["nitro"].dur
                if self.items["nitro"].id==19:
                    for i in enemies:
                        if i.id!=self.id and i.type!=0:
                            i.explosion(self.x,self.y)
                self.using_nitro = True
                self.un = True
            if self.nitro_duration == 0:
                if self.un:
                    self.curr_boost = 0
                    self.nitro_delay = self.items["nitro"].delay
                    self.additional_power = 0
                    self.un = False
            else:
                self.nitro_duration -= 1

    def update(self, keys, screen, enemys, map, check_points, under_ways,snow,console:Console,map_pick):
        # print(self.curr_boost)
        if self.type != 0:
            self.banana = False
            self.oil = False
            if self.type in [1, 2, 4, 5]:
                self.target_update(check_points)
            if self.type == 5 and enemys[self.agro_target].lap != self.laps - 1:
                self.check_agro(enemys[self.agro_target])
            self.calculate_dynamic_items_effects(keys, enemys, map)
            self.rotate(keys, map, enemys,console)
            self.drive(keys, map, enemys, under_ways,console,snow)

            self.spawn_banana(keys, map,console,map_pick)
            self.spawn_barrier(screen, keys, map,console,map_pick)
            self.spawn_oil(keys, map,console,map_pick)
            self.spawn_particles()
            self.update_info()

            a = self.lap_update(check_points)
            if a:
                return a
            l=self.explosion_vector.length()
            if l!=0:
                self.explosion_vector.scale_to_length(max(l-500,0))
        return False

    def spawn_particles(self):
        if random.randint(0, 100) < max(self.drive_force.length_squared() / 500, 5):
            self.particles.append(Particle(self.rect.center[0], self.rect.center[1], 15, (255, 165, 0), math.radians(
                self.angle + random.randint(0, self.particle_random) - 90 - self.particle_random / 2), 10, 10))

    def update_info(self):
        if self.cur_tick == 0:
            self.vel_sum[0] += self.vel_vector.length()
            self.vel_sum[1] += 1
            self.highest_vel = max(self.highest_vel, self.vel_vector.length())
            self.cur_tick = self.count_tick
        else:
            self.cur_tick -= 1
        if self.cur_replay_cooldown == 0:
            self.replay[-1].append([int(self.x), int(self.y)])
            self.cur_replay_cooldown = self.replay_cooldown
        else:
            self.cur_replay_cooldown -= 1

    def check_agro(self, player):
        if player.lap > self.lap:
            self.agro2 = 0
        elif player.lap == self.lap:
            if player.check_point > self.check_point:
                self.agro2 = 0
            elif player.check_point == self.check_point:
                angle = self.angle_to((player.x, player.y))
                if self.angles_overlap(self.angle - 180, angle, 45):
                    if pythagoras2(self.x - player.x, self.y - player.y) < 100 ** 2:
                        self.agro2 = 1
                    else:
                        self.agro2 = 0
                else:
                    self.agro2 = 0
            elif self.check_point - player.check_point <= 2:
                self.agro2 = 2
            else:
                self.agro2 = 3
        else:
            self.agro2 = 3

    def angles_overlap(self, angle1, angle2, diff):
        angle1 %= 360
        angle2 %= 360
        return abs(angle2 - angle1) <= diff or angle1 + 360 - angle2 <= diff or angle2 + 360 - angle1 <= diff

    def spawn_barrier(self, screen, keys, map,console,map_pick):
        self.barrier_ready = max(self.barrier_ready - 1, 0)
        barrier_pos=[int(self.x + math.cos(math.radians(self.angle - 180)) * 50),
                 int(self.y - math.sin(math.radians(self.angle - 180)) * 50)]
        if keys[self.keybinds[
            'spawn_barrier']] and self.barrier_ready == 0 and self.barrier == False and self.type == 3 and self.barrier_uses > 0 and barrier_terrain_check(
                [int(self.x + math.cos(math.radians(self.angle - 180)) * 50),
                 int(self.y - math.sin(math.radians(self.angle - 180)) * 50)], self.angle, map, level=self.level):
            self.barrier_uses -= 1
            console.add_system_text(f"{self.name} spawned barrier at: {barrier_pos}")

            self.barrier_ready = self.barrier_cooldown
            self.barrier = Barrier([int(self.x + math.cos(math.radians(self.angle - 180)) * 50),
                                    int(self.y - math.sin(math.radians(self.angle - 180)) * 50)], self.angle, map,
                                   self.barrier_wall, level=self.level)

        elif self.barrier:
            if self.barrier.update(screen, map):
                self.barrier = False

        if self.barrier_ready == 0 and self.type != 3 and random.randint(0,60*10)<1 and map_pick==2:
            self.barrier_ready = self.barrier_cooldown
            self.barrier = Barrier([int(self.x + math.cos(math.radians(self.angle - 180)) * 50),
                                    int(self.y - math.sin(math.radians(self.angle - 180)) * 50)], self.angle, map,
                                   self.barrier_wall, level=self.level)
            console.add_system_text(f"{self.name} spawned barrier at: {barrier_pos}")

    def spawn_banana(self, keys, map, console,map_pick):
        self.banana_ready = max(self.banana_ready - 1, 0)
        banana_pos = [int(self.x + math.sin(math.radians(self.angle - 90)) * 70),
                      int(self.y + math.cos(math.radians(self.angle - 90)) * 70)]
        if keys[self.keybinds['spawn_banana']] and self.banana_ready == 0 and self.type == 3 and banana_terrain_check(
                banana_pos, map) and self.banana_uses > 0:
            console.add_system_text(f"{self.name} spawned banana at: {banana_pos}")
            self.banana_uses -= 1
            self.banana_ready = self.banana_cooldown
            self.banana = Banana(banana_pos, level=self.level)
        elif self.type != 3 and self.banana_ready == 0 and banana_terrain_check(banana_pos, map) and random.randint(0,60*5)<1:
            self.banana_ready = self.banana_cooldown
            self.banana = Banana(banana_pos, level=self.level)
            console.add_system_text(f"{self.name} spawned banana at: {banana_pos}")

    def spawn_oil(self, keys, map,console,map_pick):
        self.oil_ready = max(self.oil_ready - 1, 0)
        oil_pos = [int(self.x + math.sin(math.radians(self.angle - 90)) * 70),
                   int(self.y + math.cos(math.radians(self.angle - 90)) * 70)]
        # print(self.oil_ready)
        if keys[self.keybinds['spawn_oil']] and self.oil_ready == 0 and self.type == 3 and oil_terrain_check(oil_pos,
                                                                                                             map) and self.oil_uses > 0:
            console.add_system_text(f"{self.name} spawned oil at: {oil_pos}")
            self.oil_uses -= 1
            print(1)
            self.oil_ready = self.oil_cooldown
            self.oil = Oil_stain(oil_pos, self.oil_duration, level=self.level)
        elif self.type != 3 and self.oil_ready == 0  and oil_terrain_check(oil_pos,map) and random.randint(0,60*30)<1  and map_pick>=1:
            self.oil_ready = self.oil_cooldown
            self.oil = Oil_stain(oil_pos,self.oil_duration)
            console.add_system_text(f"{self.name} spawned oil at: {oil_pos}")

    def draw_name(self, screen):
        screen.blit(self.name_surface,
                    (self.x - self.name_surface.get_width() // 2, self.y - self.name_surface.get_height() // 2))

    def lap_update(self, check_points):
        if check_points.check(self.rect, self.check_point):
            if self.check_point == 0:
                self.lap += 1
                self.average_v.append(int(self.vel_sum[0] / self.vel_sum[1] * 1000) / 1000)
                self.hv.append(int(self.highest_vel * 1000) / 1000)
                self.replay.append([])
                self.vel_sum[0] = 0
                self.vel_sum[1] = 0
                self.highest_vel = 0
                if self.lap == self.laps:
                    if self.type == 3:
                        return 2
                    self.type = 0
                    return 1
            self.check_point += 1
            self.check_point %= check_points.len
        return False

    def target_update(self, check_points):
        if self.type == 1 or self.type == 5:
            if self.targets[self.target].collide_point(self.x, self.y):
                self.target += 1
                self.target %= check_points.len
        if self.type == 2 or self.type == 4:
            if self.targets[self.target].collide_point(self.x, self.y):
                self.target += 1
                self.target %= check_points.len
            if self.check_targets():
                self.turn = 1
            else:
                self.turn = 0

    def check_targets(self):
        for n in self.targets:
            if n.collide_circle(Circle(self.x, self.y, self.turn_dist)):
                return True
        return False

    def check_level(self, under_ways):
        self.update_rects()
        a = under_ways.check(self.rect)
        # print(a)
        if a == 1:
            self.level = -1
            self.wall = underway
            self.barrier_wall = underway_barrier
        elif a == 0:
            self.level = 0
            self.wall = wall
            self.barrier_wall = barrier

    def simple_player_col(self, players, rects):
        for p in players:
            if p.id != self.id and p.type != 0 and self.level == p.level:
                for i in range(2):
                    for j in range(2):
                        if rects[i].colliderect(p.rects[j]):
                            return True
        return False

    def elastic_collision_2d(self, m1, v1, m2, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)

        # Compute the final velocities using conservation of momentum and kinetic energy
        u1 = v1 * (m1 - m2) / (m1 + m2) + v2 * (2 * m2) / (m1 + m2)
        u2 = v2 * (m2 - m1) / (m1 + m2) + v1 * (2 * m1) / (m1 + m2)

        return u1, u2

    def collide_players(self, players, map,console, rects=0):
        self.bounce_vector *= 0
        if not rects:
            rects = self.rects
        for p in players:
            if p.id != self.id and p.type != 0 and self.level == p.level:
                for i in range(2):
                    for j in range(2):
                        if rects[i].colliderect(p.rects[j]):
                            vs = self.elastic_collision_2d(self.mass, self.vel_vector.copy(), p.mass,
                                                           p.vel_vector.copy())
                            self.vel_vector.x = vs[0][0]
                            self.vel_vector.y = vs[0][1]
                            p.vel_vector.x = vs[1][0]
                            p.vel_vector.y = vs[1][1]
                            self.angle %= 360
                            p.angle %= 360
                            dir = self.calculate_col_dir(p)
                            self.calculate_col_effect(p, i, j, dir, 0, map, players)
                            console.add_system_text(f"{self.name} collided with {p.name}")
                            return True

    def calculate_col_dir(self, p):
        if self.angle > p.angle:
            if 360 + p.angle - self.angle < self.angle - p.angle:
                return -1
            else:
                return 1
        elif self.angle < p.angle:
            if 360 + self.angle - p.angle < p.angle - self.angle:
                return 1
            else:
                return -1
        elif self.angle != p.angle:
            return 1
        return 0

    def return_rects(self, rect, angle):
        rects = self.rects.copy()
        rects[0].center = rect.centerx + math.sin(math.radians(angle + 90)) * 10, rect.centery + math.cos(
            math.radians(angle + 90)) * 10
        rects[1].center = rect.centerx + math.sin(math.radians(angle - 90)) * 10, rect.centery + math.cos(
            math.radians(angle - 90)) * 10
        return rects

    def calculate_col_effect(self, p, i, j, dir, bounce, map, players):
        c_angle = 5
        angle1 = c_angle * self.mass / (self.mass + p.mass)
        angle2 = c_angle * self.mass / (self.mass + p.mass)
        if i == 0:
            if j == 0:
                if dir == 1:
                    self.col_assist(p, angle1, angle2, -1, map, bounce, players)
                elif dir == -1:
                    self.col_assist(p, angle1, angle2, 1, map, bounce, players)
            else:
                if dir == 1:
                    self.col_assist(p, angle1, angle2, 1, map, bounce, players)
                elif dir == -1:
                    self.col_assist(p, angle1, angle2, -1, map, bounce, players)
        else:
            if j == 0:
                if dir == 1:
                    self.col_assist(p, angle1, angle2, 1, map, bounce, players)
                elif dir == -1:
                    self.col_assist(p, angle1, angle2, -1, map, bounce, players)
            else:
                if dir == 1:
                    self.col_assist(p, angle1, angle2, -1, map, bounce, players)
                elif dir == -1:
                    self.col_assist(p, angle1, angle2, 1, map, bounce, players)

    def col_assist(self, p, a1, a2, a, map, bounce, players):
        self.col_rotate(a1 * a, map, players)
        p.col_rotate(a2 * a * -1, map, players)
        self.bounce_off(bounce, self.angle + 180 if a == 1 else 0)
        p.bounce_off(bounce, self.angle + + 180 if a == -1 else 0)

    def bounce_off(self, px, angle):
        self.centrifugal_force.x += math.sin(math.radians(angle)) * px
        self.centrifugal_force.y += math.cos(math.radians(angle)) * px

    def collide_map(self, pos, image, map, accuarcy=1):

        mask = pygame.mask.from_surface(image)
        mask_rect = mask.get_rect()
        if pos[0] < 0 or pos[0] + mask_rect.w > screen_width or pos[1] < 0 or pos[1] + mask_rect.h > screen_height:
            return True
        t = 1

        for i in range(mask_rect.width // accuarcy):
            for j in range(mask_rect.height // accuarcy):

                if mask.get_at((i * accuarcy, j * accuarcy)):
                    tile = [int(pos[0] + i * accuarcy) // tile_size, int(pos[1] + j * accuarcy) // tile_size]
                    if t:
                        if map[tile[0]][tile[1]] == ice:
                            self.friction = ice_friction
                            t = 0
                        elif map[tile[0]][tile[1]] == sand:
                            self.friction = sand_friction
                            t = 0
                    if map[tile[0]][tile[1]] == self.wall or map[tile[0]][tile[1]] == self.barrier_wall:
                        return True

        if t:
            self.friction = asphalt_friction
        return False

    def col_rotate(self, angle, map, players):
        temp_img = pygame.transform.rotate(self.original_image, self.angle + angle)
        temp_rect = temp_img.get_rect()
        temp_rect.center = (self.x, self.y)
        rects = self.return_rects(temp_rect, self.angle + angle)
        if not self.collide_map(temp_rect.topleft, temp_img, map, 5) and not self.simple_player_col(players, rects):
            self.angle += angle
            self.angle %= 360
            self.accelerate_vector.rotate_ip(angle)
            self.vel_vector.rotate_ip(angle)
            self.image = temp_img.copy()
            self.rect = temp_rect.copy()
            self.update_rects()

    def particles_draw(self, screen):
        for particle in self.particles:
            particle.move()
            particle.fading()
            particle.draw(screen)
            if particle.parpop:
                self.particles.remove(particle)

    def accelerate(self, keys):
        self.drive_force *= 0
        f_l = (self.items["engine"].power * self.power_multiplier + self.curr_boost) / max(
            self.vel_vector.length() / 2.2, 2.2)

        v_l = self.vel_vector.length()
        # if f_l / self.mass-self.friction*self.weight<0:
        # print(f_l,self.type)
        l = v_l + f_l / self.mass + self.centrifugal_force.length() / self.mass - self.friction * 10
        # f_l = self.weight * f
        #         print(l)
        if self.go_back:
            direction = -1
        else:
            direction = 1
        if self.type == 1:
            if l < self.max_v:
                self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
            else:
                f_l = (self.max_v + self.friction * 10 - v_l) * self.mass
                self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
        elif self.type == 2 or self.type == 4:
            if self.turn:
                if self.agro or l < self.max_turn_v:
                    self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                    self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
                else:
                    f_l = (self.max_turn_v + self.friction * 10 - v_l) * self.mass

                    self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                    self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
            else:
                if self.agro or l < self.max_v:
                    self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                    self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
                else:
                    f_l = (self.max_v + self.friction * 10 - v_l) * self.mass
                    self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                    self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction

        elif self.type == 3:
            if keys[self.keybinds['drive_forwards']]:
                self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l
                self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l
            elif keys[self.keybinds['drive_backwards']]:
                self.drive_force.x = math.sin(math.radians(self.angle - 90)) * f_l
                self.drive_force.y = math.cos(math.radians(self.angle - 90)) * f_l
        elif self.type == 5:

            if self.agro2 == 1 or self.agro2 == 0:
                max_v = self.max_v
            elif self.agro2 == 2:
                max_v = self.slowing_speed
            elif self.agro2 == 3:
                max_v = self.slowing_speed2
            if l < max_v:
                self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction
            else:
                f_l = (max_v + self.friction * 10 - v_l) * self.mass
                self.drive_force.x = math.sin(math.radians(self.angle + 90)) * f_l * direction
                self.drive_force.y = math.cos(math.radians(self.angle + 90)) * f_l * direction

            # return self.drive_force
        #     self.accelerate_vector.x = math.sin(math.radians(self.angle + 90)) * self.speed
        #     self.accelerate_vector.y = math.cos(math.radians(self.angle + 90)) * self.speed
        #
        #
        #

        # self.accelerate_vector*=self.speed**0.5

    def calculate_friction(self, vel, keys):
        f = self.friction

        if self.friction == asphalt_friction:
            self.friction *= self.items['tires'].asphalt_friction
        elif self.friction == sand_friction:
            self.friction *= self.items['tires'].sand_friction
        elif self.friction == ice_friction:
            self.friction *= self.items['tires'].ice_friction

        # if self.type == 2 or self.type == 4:
        #     if self.turn:
        #         if self.vel_vector.length_squared() > self.max_turn_v ** 2:
        #             self.curr_brakes = min(self.brakes_speed * self.brakes_max_friction + self.curr_brakes,
        #                                    self.brakes_max_friction)
        #             f += self.curr_brakes
        #         else:
        #             self.curr_brakes = 0
        f_l = self.weight * f
        friction = vel.copy()
        friction *= -1
        if vel.length_squared() <= (f_l / self.mass) ** 2:
            return 0
        else:
            if friction.length_squared() > 0.1:
                friction.scale_to_length(f_l)
        return friction

    def calculate_acceleration(self, force):
        return force / self.mass

    def terrain_check(self, pos, mask, map,snow=False):
        self.sztutr=False
        mask_rect = mask.get_rect()
        self.in_snow=max(self.in_snow-1,0)
        for i in range(mask_rect.width):
            for j in range(mask_rect.height):
                if mask.get_at((i, j)):
                    tile = [int(pos[0] + i) // tile_size, int(pos[1] + j) // tile_size]
                    if map[tile[0]][tile[1]] == ice:
                        self.friction = ice_friction * self.items['tires'].ice_friction
                        return 1
                    elif map[tile[0]][tile[1]] == sand:
                        self.friction = sand_friction * self.items['tires'].sand_friction
                        if snow:
                            self.in_snow=min(self.in_snow+2,self.in_snow_max)
                        return 1
                    elif map[tile[0]][tile[1]] == sztutr:
                        self.sztutr=True
                        self.friction=asphalt_friction
                        return 1
        self.friction = asphalt_friction * self.items['tires'].asphalt_friction
        return False

    def simple_col_check(self, pos, mask, map, accuarcy=1):
        mask_rect = self.rect
        if pos[0] < 0 or pos[0] + mask_rect.w > screen_width or pos[1] < 0 or pos[1] + mask_rect.h > screen_height:
            return True
        for i in range(mask_rect.width // accuarcy):
            for j in range(mask_rect.height // accuarcy):
                if (mask.get_at((i * accuarcy, j * accuarcy)) and map[int(pos[0] + i * accuarcy) // tile_size][
                    int(pos[1] + j * accuarcy) // tile_size] == self.wall or
                        map[int(pos[0] + i * accuarcy) // tile_size][
                            int(pos[1] + j * accuarcy) // tile_size] == self.barrier_wall):
                    return True
        return False

    def update_rects(self):
        self.rect.center = self.x, self.y
        self.rects[0].center = self.x + math.sin(math.radians(self.angle + 90)) * 10, self.y + math.cos(
            math.radians(self.angle + 90)) * 10
        self.rects[1].center = self.x + math.sin(math.radians(self.angle - 90)) * 10, self.y + math.cos(
            math.radians(self.angle - 90)) * 10

    def distance_to_check_point(self):
        return pythagoras2(self.x - self.targets[self.target].x, self.y - self.targets[self.target].y)

    def drive(self, keys, map, players, under_ways,console,snow=False):
        self.boost(keys,players)
        self.accelerate(keys)
        accuarcy = 2
        print(self.explosion_vector)
        force = self.drive_force + self.centrifugal_force+self.explosion_vector
        acc = self.calculate_acceleration(force)
        friction = self.calculate_friction(self.vel_vector + acc, keys)
        if friction:
            force += friction
            acc = self.calculate_acceleration(force)
            self.vel_vector += acc
        else:
            self.vel_vector *= 0
        l = 1  # int(self.vel_vector.length())//3 + 1
        cx = int(self.vel_vector.x / l * 1000) / 1000
        cy = int(self.vel_vector.y / l * 1000) / 1000
        if self.type in [1, 2, 4, 5]:
            if pythagoras2(cx, cy) > self.distance_to_check_point()**2:
                cx = self.targets[self.target].x - self.x
                cy = self.targets[self.target].y - self.y
        mask = pygame.mask.from_surface(self.image)
        self.update_rects()
        self.go_back = False
        for i in range(l):
            self.check_level(under_ways)
            if self.simple_col_check((self.rect.x + cx, self.rect.y), mask, map, accuarcy):
                self.vel_vector.x = -self.vel_vector.x * self.bouncy
                cx = self.vel_vector.x / l
                self.go_back = True
                print("col")
            else:
                self.x += cx
                self.update_rects()
                self.check_level(under_ways)
                if self.collide_players(players, map,console):
                    self.x -= cx
                    mask = pygame.mask.from_surface(self.image)
            self.update_rects()
            self.check_level(under_ways)
            # break
            self.update_rects()
            if self.simple_col_check((self.rect.x, self.rect.y + cy), mask, map, accuarcy):
                self.vel_vector.y = -self.vel_vector.y * self.bouncy
                cy = self.vel_vector.y / l
                self.go_back = True
                print("col")
            else:
                self.y += cy
                self.update_rects()
                self.check_level(under_ways)
                if self.collide_players(players, map,console):
                    self.y -= cy
            self.update_rects()
            self.check_level(under_ways)
        self.terrain_check(self.rect.topleft, mask, map,snow)
        self.update_rects()

    def angle_to_checkpoint(self):
        dx = self.x - self.targets[self.target].x
        dy = self.y - self.targets[self.target].y
        if dx == 0:
            if dy > 0:
                return 270
            return 90
        if self.x <= self.targets[self.target].x:
            angle = int(math.degrees(math.atan(dy / dx))) * -1
        else:
            angle = 180 - int(math.degrees(math.atan(dy / dx)))
        return angle % 360

    def angle_to(self, point):
        dx = self.x - point[0]
        dy = self.y - point[1]
        if dx == 0:
            if dy > 0:
                return 270
            return 90
        if self.x <= point[0]:
            angle = int(math.degrees(math.atan(dy / dx))) * -1
        else:
            angle = 180 - int(math.degrees(math.atan(dy / dx)))
        return angle % 360

    def angles_right(self, angle1, angle2):
        if angle1 > angle2:
            if 360 + angle2 - angle1 < angle1 - angle2:
                left = 1
                return False
            else:
                right = 1
                return True
        elif angle1 < angle2:
            if 360 + angle1 - angle2 < angle2 - angle1:
                right = 1
                return True
            else:
                left = 1
                return False

    def rotate(self, keys, map, players,console):
        # print(self.angle)
        self.agro = 0
        self.centrifugal_force *= 0
        self.angle %= 360
        # print(self.vel_vector.length_squared())
        left = 0
        right = 0
        # self.x=119
        # self.y=700
        self.update_rects()
        if self.type == 4:
            if self.check_point == players[self.agro_target].check_point:
                point = (players[self.agro_target].x, players[self.agro_target].y)
                angle = self.angle_to(point)
                if abs(angle - self.angle) <= self.agro_angle or self.angle + 360 - angle <= self.agro_angle or angle + 360 - self.angle <= self.agro_angle:
                    print("skibidi")
                    self.agro = 1
                else:
                    point = (self.targets[self.target].x, self.targets[self.target].y)
            else:
                point = (self.targets[self.target].x, self.targets[self.target].y)
            angle = self.angle_to(point)
            angle %= 360
            if self.angle > angle:
                if 360 + angle - self.angle < self.angle - angle:
                    left = 1
                else:
                    right = 1
            elif self.angle < angle:
                if 360 + self.angle - angle < angle - self.angle:
                    right = 1
                else:
                    left = 1
            elif self.angle != angle:
                right = 1
        if self.type == 5:
            # if keys[pg.K_LEFT]:
            #     left = 1
            # elif keys[pg.K_RIGHT]:
            #     right = 1
            if self.agro2 != 1:
                angle = self.angle_to_checkpoint()
                if self.angles_right(self.angle, angle):
                    right = 1
                else:
                    left = 1
            else:
                angle = self.angle_to_checkpoint()
                angle2 = players[self.agro_target].angle_to_checkpoint()
                if self.angles_right(angle, angle2):
                    left = 1
                else:
                    right = 1
            # left=0
            # right=0

        if self.type == 1 or self.type == 2:
            angle = self.angle_to_checkpoint()
            if self.angle > angle:
                if 360 + angle - self.angle < self.angle - angle:
                    left = 1
                else:
                    right = 1
            elif self.angle < angle:
                if 360 + self.angle - angle < angle - self.angle:
                    right = 1
                else:
                    left = 1
            elif self.angle != angle:
                right = 1
            # self.image=pygame.transform.rotate(self.original_image, self.angle)
            # self.rect=self.image.get_rect()
            # #print(self.angle)
            # self.update_rects()
        if self.type == 3:
            if keys[self.keybinds['turn_right']]:
                right = 1
            elif keys[self.keybinds['turn_left']]:
                left = 1
        rotation_vel = 0
        if self.banana_effect:
            # rotation_vel = self.banana_effect_angle
            # if random.randint(0,1):
            #     left=1
            #     right=0
            # else:
            #     right=1
            #     left=0
            self.banana_effect -= 1
            left = 0
            right = 0
        else:
            rotation_vel = self.rotation_vel
        if self.sztutr and not self.sztutr_immunity:
            a=3
        else:
            a = 1
        if self.oil_effect:
            print(1)
            right = 1
            rotation_vel = self.oil_effect_angle * self.vel_vector.length() / 10
            self.oil_effect -= 1
        if rotation_vel:  # :
            if right:
                temp_img = pygame.transform.rotate(self.original_image, (self.angle - rotation_vel) % 360)
                temp_rect = temp_img.get_rect()
                temp_rect.center = (self.x, self.y)
                rects = self.return_rects(temp_rect, (self.angle - rotation_vel) % 360)
                if not self.collide_map(temp_rect.topleft, temp_img, map) and not self.collide_players(players, map,console,
                                                                                                       rects):
                    vl = self.vel_vector.length()
                    r = max(vl / math.radians(rotation_vel),
                            1)
                    f_l = self.mass * vl ** 2 / r * a
                    self.centrifugal_force.x = math.sin(math.radians(self.angle + 180)) * f_l
                    self.centrifugal_force.y = math.cos(math.radians(self.angle + 180)) * f_l

                    self.angle -= rotation_vel
                    self.accelerate_vector.rotate_ip(rotation_vel)
                    self.image = temp_img.copy()
                    self.rect = temp_rect.copy()
                    self.update_rects()
            elif left:
                temp_img = pygame.transform.rotate(self.original_image, (self.angle + rotation_vel) % 360)
                temp_rect = temp_img.get_rect()
                temp_rect.center = (self.x, self.y)
                rects = self.return_rects(temp_rect, (self.angle + rotation_vel) % 360)
                if not self.collide_map(temp_rect.topleft, temp_img, map) and not self.collide_players(players, map,console,
                                                                                                       rects):
                    vl = self.vel_vector.length()
                    r = max(vl / math.radians(rotation_vel),
                            1)
                    f_l = self.mass * vl ** 2 / r * a
                    self.centrifugal_force.x = math.sin(math.radians(self.angle)) * f_l
                    self.centrifugal_force.y = math.cos(math.radians(self.angle)) * f_l

                    self.angle += rotation_vel
                    self.accelerate_vector.rotate_ip(-rotation_vel)
                    self.image = temp_img.copy()
                    self.rect = temp_rect.copy()
                    self.update_rects()
        self.angle %= 360

    def draw(self, screen):
        if self.type != 0:
            screen.blit(self.image, self.rect)
            self.draw_name(screen)
            if self.items["nitro"].id == 17 and self.type==3:
                pg.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r, width=5)

