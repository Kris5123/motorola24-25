import pygame as pg
pg.init()
print(99999/100*100)
import random
def text(font, txt, color):
    font = font.render(txt, 1, color)
    return font, font.get_width(), font.get_height()


def text_down(txt, font, width):
    textr = []
    pointer = 0
    l = len(txt)
    while pointer < l:
        a = ""
        while text(font, a, 0, )[1] < width and txt[pointer]!=';':
            a += txt[pointer]
            pointer += 1
            if pointer == l:
                break
        if pointer != l or text(font, a, 0, )[1] >= width:
            if txt[pointer]==';':
                pointer += 1
            else:
                a = a[:-1]
                pointer -= 1
        textr.append(a)
    return textr
def get_background(image,width,height):
    return pg.transform.scale(pg.image.load(image), (width, height)).convert_alpha()
def get_player_info(place,enemys,laps,game_results,time_table,players_q,map,gold_rewards,gold_time_bonuses,gem_rewards,gem_time_bonuses,game_mode,map_pick):
    players_info = []
    names = []
    items=[]
    for j, k in enumerate(enemys):
        print(k.a)
        if k.a != 0:
            players_info.append([])
            names.append(k.name)
            items.append([k.items[i] for i in k.items])
            for n in range(laps):
                players_info[-1].append([])
                try:
                    players_info[-1][-1].append(time_table.lap_times[j][n])
                    players_info[-1][-1].append(k.average_v[n])
                    players_info[-1][-1].append(k.hv[n])
                    players_info[-1][-1].append(k.replay[n])
                except:
                    players_info[-1][-1].append(0)
                    players_info[-1][-1].append(int(k.vel_sum[0]/k.vel_sum[1]*1000)/1000)
                    players_info[-1][-1].append(int(k.highest_vel*1000)/1000)
                    players_info[-1][-1].append(k.replay[n])
                    break
        if k.a==3:
            if game_mode==0:
                gold_income=[gold_rewards[map_pick][place],int(gold_time_bonuses[map_pick][0]*gold_time_bonuses[map_pick][1]/sum(time_table.lap_times[j]))]
                gold_income.append(int((gold_income[0]+gold_income[1])*(k.coin_multiplier)))
                gem_income=[gem_rewards[map_pick][place],int(gem_time_bonuses[map_pick][0]*gem_time_bonuses[map_pick][1]/sum(time_table.lap_times[j]))]
                gem_income.append(int((gem_income[0]+gem_income[1])*(k.gem_multiplier)))
            else:
                gold_income=[0,0,0]
                gem_income=[0,0,0]
        k.finish_race()

    game_results.intialise(place,names,players_info,players_q,[("Place ",gold_income[0]),("Time ",gold_income[1]),("Items",gold_income[2])]
                           ,[("Place ",gem_income[0]),("Time ",gem_income[1]),("Items",gem_income[2])],laps,map,enemys[0].replay_cooldown,items)
def pythagoras(a,b):
    return (a**2+b**2)**0.5
def pythagoras2(a,b):
    return a**2 + b**2
itemki="items: "
ekwipunek="eq: "
def save(gold,gems,items,maps,eq):
    with open("save.txt", "w") as file:
        file.write(str(gold)+"\n")
        file.write(str(gems)+"\n")
        file.write(itemki)
        [file.write(str(i)+" ") for i in items]
        file.write("\n")
        file.write(str(maps)+"\n")
        file.write(ekwipunek)
        [file.write(str(i)+" ") for i in eq]
def load():
    with open("save.txt", "r", encoding="utf-8") as file:
        info=[]
        for line in file:
            line = line.strip().split()
            if line[0]==itemki.strip() or line[0]==ekwipunek.strip():
                if len(line)>1:
                    info.append([int(i) for i in line[1:]])
                else:
                    info.append([])
            else:
                info.append(int(line[0]))
    print(info)
    return info
def id_to_items(ids,all_items):
    items=[]
    for i in ids:
        for j in all_items:
            if j.id==i:
                items.append(j.copy())
    return items
sorted_items={
            "tires": [],
            "talisman": [],
            "engine": [],
            "nitro": []}
items_rarities={
            "tires": [0,0,0,0,0],
            "talisman": [0,0,0,0,0],
            "engine": [0,0,0,0,0],
            "nitro": [0,0,0,0,0]
}
rarities_to_i={
    "common":0,
    "uncommon":1,
    "rare":2,
    "epic":3,
    "legendary":4
}
def sort_items(items):
    for i in items:
        print(i.rarity,i.type)
        sorted_items[i.type].append(i.id)
        items_rarities[i.type][rarities_to_i[i.rarity]]+=1
    print(items_rarities)
def give_items(map):
    chosen_items=[{
            "tires": 0,
            "talisman": 0,
            "engine": 0,
            "nitro": 0
        },{
            "tires": 0,
            "talisman": 0,
            "engine": 0,
            "nitro": 0
        },{
            "tires": 0,
            "talisman": 0,
            "engine": 0,
            "nitro": 0
        },{
            "tires": 0,
            "talisman": 0,
            "engine": 0,
            "nitro": 0
        }]
    for i in range(4):
        item=random.randint(0,sum(items_rarities["tires"][map:map+3])-1)
        for j in sorted_items["tires"]:
            if item==0:
                chosen_items[i]["tires"]=j
                break
            else:
                item-=1
        item=random.randint(0,sum(items_rarities["talisman"][map:map+3])-1)
        for j in sorted_items["talisman"]:
            if item==0:
                chosen_items[i]["talisman"]=j
                break
            else:
                item-=1
        item=random.randint(0,sum(items_rarities["engine"][map:map+3])-1)
        for j in sorted_items["engine"]:
            if item==0:
                chosen_items[i]["engine"]=j
                break
            else:
                item-=1
        item=random.randint(0,sum(items_rarities["nitro"][map:map+3])-1)
        for j in sorted_items["nitro"]:
            if item==0:
                chosen_items[i]["nitro"]=j
                break
            else:
                item-=1
    print(chosen_items)
    return chosen_items
def dict_ids_to_items(ids,items):
    for i in ids:
        for j in items:
            if j.id==ids[i]:
                ids[i]=j.copy()
    return ids

