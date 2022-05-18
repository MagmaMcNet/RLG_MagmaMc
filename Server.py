
# imported files http://magma-mc.net/Share/MagmaMc_RLG/files/
import time, threading, uuid
import filez
import pgzrun
from pgzero.builtins import Actor, keys, clock
from pypresence import Presence
from random import randint
from tkinter import messagebox
import pygame
import Modloader
import logging
import commentjson as json
import os, requests

localip = requests.get('https://api.ipify.org').text


root = "Null"
try:
    settings = json.load(open("../ServerConfig.json"))
    root = "../"
except:
    settings = json.load(open("ServerConfig.json"))
    root = ""
try:
    if os.path.getsize(root+'ServerLog.log') > 10 * 1024:
        os.remove(root+'ServerLog.log')
except:
    pass
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# define file handler and set formatter
file_handler = logging.FileHandler(root+'ServerLog.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
# add file handler to logger
logger.addHandler(file_handler)
if root == "":
    logger.info("Server Uncompiled Is Running In Dev Mode")
from files.Class_Functions import SpriteSheet
filez.SetUrl(localip)
isonline = False
try:
    if server["Online"] > time.time():
        messagebox.showerror("Error", "Server ID Is Currently Already In Use")
        isonline = True
        raise
except:
    if isonline:
        raise



TITLE = "Dungeons Server"
spawn_pos = (64, 128)
cell_scale = 64
block = Actor('default')
item = Actor('default', pos=(100, 100))
player = Actor('default', pos=(spawn_pos[0], spawn_pos[1]))

currentfps = 5
fps = 0
def getfps():
    global fps
    fps += 1
    return str(currentfps)

updatedelay = 0
def updatefps():
    global fps, currentfps, updatedelay
    if updatedelay == 10:
        updatedelay = 0
        currentfps = fps
        fps = 0
    else:
        updatedelay += 1

clock.schedule_interval(updatefps, 0.1)

servertime = 10.0
CurrentWave = 2
PlayerAmount = 0
players = []
enemies = []
hearts = []
damage_boosts = []
start_time=time.time()
RPCupdate = 0
Modloader.UploadImages()
Modloader.DownloadImages()
def RPC_update():
    global RPCupdate
    if RPCupdate == 150:
        RPCupdate = 0
        print(
            RPC.update(
                large_image="gameicon",
                large_text="Wave: " + str(CurrentWave),
                
                small_image="playericon",
                small_text="Players: " + str(len(players)),
                start=start_time,
                state="Hosting Server"
                
                    )
            )
    else:
        RPCupdate += 1
if settings["DiscordRichPresence"]:
    client_id = '972147407582285925'  # Fake ID, put your real one here
    RPC = Presence(client_id)  # Initialize the client class
    RPC.connect() # Start the handshake loop
    
    clock.schedule_interval(RPC_update, 0.1)
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def getplayer():
    global players, enemies
    playerdata = filez.scan('Saves/')
    try:
        tempplayers = []
    except:
        pass
    cls()
    print("Enemies Remaining:", len(enemies))
    print("Players:")
    for playerfilename in playerdata:
        
        if playerfilename != ".json" and playerfilename != '[':
            playerfile = filez.fread("/"+str(playerfilename))
            try:
                
                otherplayer = Actor('player'+playerfile["randomskin"], bottomleft=(float(playerfile["x"]), float(playerfile["y"])) )
                char.loads(otherplayer, (3, 2, 0.6, "idle"))
                otherplayer._update_pos()
                otherplayer.bottom = float(playerfile["y"])
                otherplayer.left = float(playerfile["x"])
                otherplayer.username = playerfile["username"]
                otherplayer.kills = playerfile["Kills"]
            except Exception as e:
                print(e)
            try:
                if float(playerfile["numb"]) > time.time():
                    print(" "+playerfilename.strip(".json"))
                    tempplayers.append(otherplayer)
            except:
                pass
    players = tempplayers
char = SpriteSheet("character", (96, 128), 96, 126, 0)

ens = SpriteSheet("Enemies", (17, 17), 16, 16, 0)

level = 1
sprites = {
    "tiles": {
        0: (16, 16, 4, "border1"),
        1: (17, 16, 4, "border2"),
        2: (18, 16, 4, "border3"),
        3: (19, 16, 4, "border4"),
        4: (16, 10, 4, "floor1"),
        5: (17, 10, 4, "floor2"),
        6: (18, 10, 4, "floor3"), 
    },
    "entitys": {
        0: (0, 0, 4, "zombie"),
        1: (1, 0, 4, "skeleton"),
    },
    "objects": {
        0: (),
        1: (14, 10, 4, "coal ore"),
        2: (14, 10, 4, "coal ore"),
        3: (14, 10, 4, "coal ore"),
        4: (14, 13, 4, "copper ore"),
        5: (14, 13, 4, "copper ore"),
        6: (15, 12, 4, "gold ore"),
        7: (15, 13, 4, "emerald ore"),
        8: (9, 3, 4, "crack1"),
        9: (9, 3, 4, "crack1"),
        10: (9, 3, 4, "crack1"),
        11: (10, 3, 4, "crack2"),
        12: (10, 3, 4, "crack2"),
        13: (10, 3, 4, "crack2"),
    }
}


map_tiles = [
    { # 1
        "tiles": [
            [3, 2, 0, 2, 2, 0, 1, 2, 3, 0, 3, 2, 0, 2, 2, 0, 3, 0],
            [1, 4, 4, 5, 5, 4, 4, 5, 4, 6, 4, 4, 4, 5, 6, 4, 4, 1],
            [1, 4, 6, 4, 5, 5, 4, 6, 4, 5, 5, 4, 6, 4, 5, 5, 4, 3],
            [0, 4, 4, 5, 4, 5, 4, 4, 5, 4, 6, 4, 4, 5, 4, 6, 4, 3],
            [2, 4, 6, 4, 4, 6, 4, 5, 4, 4, 4, 6, 4, 5, 4, 4, 5, 0],
            [3, 4, 4, 4, 5, 4, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 1],
            [0, 4, 5, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 4, 4, 5, 4, 3],
            [3, 4, 4, 4, 4, 4, 4, 5, 4, 4, 6, 4, 4, 5, 4, 4, 4, 1],
            [0, 4, 4, 4, 4, 4, 4, 5, 4, 4, 6, 4, 4, 4, 4, 5, 6, 3],
            [0, 0, 3, 0, 1, 2, 0, 2, 2, 0, 3, 0, 1, 2, 0, 2, 3, 3],
        ],
        "Objects": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 1 = disable Objects
            
        ],
    }
]
WIDTH = 1152 #len(map_tiles[0]["tiles"][1]) * cell_scale
HEIGHT = 640 #len(map_tiles[0]["tiles"]) * cell_scale
map_level = []
map_level_obj = []



c1 = 0
player.HP = 100

textpos = 5
def FixServer():
    data = {
                "Online": time.time()+servertime,
                "WaveTime": saywave,
                "Wave": CurrentWave-1
            }
    filez.fwrite("Server/Server.json", json.dumps(data))


class ServerConnection:
    def Update():
        global saywave, CurrentWave, enemies, ens
        filez.send("Server/Server.json", time.time()+servertime, "Online", "=")
        try:
            GameSave = filez.fread("Server/Server.json")
            CurrentWave = GameSave["Wave"]
            saywave = GameSave["WaveTime"]
        except Exception as e:
            FixServer()
        try:
            server = filez.scan("Enemies/")
        except Exception as e:
            logger.error( e )
        tempEnemies = []
        for i in server:
            try:
                File = filez.fread("/Enemies/"+i)
                en = Actor('default')
                en.HP = int(File["HP"])
                en.DAMAGE = int(File["DAMAGE"])
                en._surf = pygame.image.load(File["IMAGE"]).convert()
                en._surf = pygame.transform.scale(en._surf, (en.width * File["Scale"], en.height * File["Scale"]))
                en._surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
                en._update_pos()
                en.top = int(File["TOP"])
                en.left = int(File["LEFT"])
                en.Status = File["Status"]
                en.Attack = File["Attack"]
                en.Name = i.strip(".json")
                pygame.PixelArray(en._surf).replace(16711780, pygame.Color(File["Color"][0], File["Color"][1], File["Color"][2], 0))
                R = int(File["Color"][0]//1.5) if File["Color"][0] > 0 else File["Color"][0]
                G = int(File["Color"][1]//1.5) if File["Color"][1] > 0 else File["Color"][1]
                B = int(File["Color"][2]//1.5) if File["Color"][2] > 0 else File["Color"][2]
                pygame.PixelArray(en._surf).replace(6553700, pygame.Color(R, G, B))
                pygame.PixelArray(en._surf).replace(6553855, pygame.Color(0, 30, 30, 30))
                if en.HP > 0:
                    tempEnemies.append(en)
                else:
                    filez.delete("Enemies/"+en.Name+".json")
                    filez.fwrite("Kills/"+en.Attack+"/"+en.Name+".json", json.dumps({"A":"B"}))
            except Exception as e:
                logger.warning(e)
                filez.delete("Enemies/"+i)
        enemies = tempEnemies


class Functions:
    def quicktext(text, color=(10, 10, 10), size=25):
        global textpos
        screen.draw.text(text, pos=(5, textpos), color=color, bold="true", fontsize=size)
        textpos += 20
    def draw_test():
        global textpos
        textpos = 5
        Functions.quicktext(text = "Wave: " + str(CurrentWave-1))
        Functions.quicktext(text = "Players: " + str(len(players)))
        Functions.quicktext(text = "Uptime: " + str(int(time.time() - start_time)))
        Functions.quicktext(text = "fps: " + getfps())
        
        Functions.quicktext(text = "")
        Functions.quicktext(text = "Mods", color = (10, 10, 100))
        for Mod in Modloader.GetMods():
            Functions.quicktext(text = Mod.upper(), size = 20, color = (10, 10, 60))
        
        
    def wave(wave):
        global enemies
        filez.send("Server/"+"Server.json", 20, "WaveTime", "=")
        filez.send("Server/"+"Server.json", 1, "Wave", "+")
        tempenemies = []
        UsableEnemies = []
        for ModEnemy in Modloader.GetModdedEnemies():
            for Mod in ModEnemy:
                if Mod["Wave"] <= wave and Mod["StopWave"] >= wave:
                    UsableEnemies.append(Mod)
        for _ in range((20 if wave > 20 else wave+1)):
            enemy = Actor('default')
            enemy.numb = randint(0, len(UsableEnemies)-1)
            enemy.STRENGTH = randint(0,1)+1
            enemy.rand = randint(0,1)
            enemy._surf = pygame.image.load(Modloader.GetImage(UsableEnemies[enemy.numb]["Image"])).convert()
            enemy.Scale = Modloader.GetScale(UsableEnemies[enemy.numb]["Image"])
            enemy.Status = "Idle"
            enemy.HP = enemy.STRENGTH*20
            enemy.DAMAGE = enemy.STRENGTH*5
            enemy.top = 64*randint(2,8)
            enemy.left = 64*randint(2,16)
            enemy.Name = str(uuid.uuid4())
            enemy.Color = UsableEnemies[enemy.numb]["Color"]
            tempenemies.append(enemy)
            data = {
                "STRENGTH": enemy.STRENGTH,
                "IMAGE": Modloader.GetImage(UsableEnemies[enemy.numb]["Image"]),
                "Status": "Idle",
                "HP": enemy.HP,
                "DAMAGE": enemy.DAMAGE,
                "TOP": enemy.top,
                "LEFT": enemy.left,
                "Attack": "Nooneshouldhavethisusername",
                "Color": enemy.Color,
                "Scale": enemy.Scale
                
            }
            filez.send("Enemies/"+enemy.Name+".json", data)
        enemies = tempenemies
    def taken_damage(subject, other):
        other.HP -= subject.DAMAGE
        other.Status = "Attacked"
        if other.HP <= 0:
            other.Status = "Dead"
            if randint(1,6) == 1:
                Heal = Actor('health', pos=other.pos)
                hearts.append(Heal)
            elif randint(1,12) == 1:
                Heal = Actor('damage_boost', pos=other.pos)
                damage_boosts.append(Heal)
                
            other.pos = (-100, -100)

    def current_level(readlevel):
        global map_level
        sheet = SpriteSheet("map", (17, 17), 16, 16)
        try:
            del map_level[:]
        except:
            pass
        for h in range(len(map_tiles[readlevel-1]["tiles"])):
            for w in range(len(map_tiles[readlevel-1]["tiles"][1])):
                cell = Actor('default')
                sheet.loads(cell, sprites["tiles"][map_tiles[readlevel-1]["tiles"][h][w]])
                cell.left = cell.width * w
                cell.top = cell.height * h
                if randint(0, 7) == 0 and map_tiles[readlevel-1]["Objects"][h][w] == 0:
                    cell_object = Actor('default')
                    sheet.loads(cell_object, sprites["objects"][randint(1,13)])
                    cell_object.left = cell_object.width * w
                    cell_object.top = cell_object.height * h
                    map_level_obj.append(cell_object)
                map_level.append(cell)
saywave = 0
Functions.current_level(1)
def DoWaves():
    global c1, CurrentWave, saywave
    ch = 0
    for i in enemies:
        ch += i.HP
    if ch <= 0:
        if c1 >= 2:
            Functions.wave(CurrentWave)
            c1 = 0
        else:
            c1 += 1



#
GetplayersDelay = 0
ServerConnectionDelay = 0
PathDelay = 0
class FunctionCall:
    def GetPlayers():
        global GetplayersDelay
        if GetplayersDelay == 90:
            GetplayersDelay = 0
            threading.Thread(target=getplayer).start()
        else:
            GetplayersDelay += 1
    def ServerConnection():
        global ServerConnectionDelay
        if ServerConnectionDelay == 35:
            ServerConnectionDelay = 0
            threading.Thread(target=ServerConnection.Update).start()
        else:
            ServerConnectionDelay += 1
    def WaveUpdate():
        global PathDelay
        if PathDelay != 5:
            PathDelay += 1
            return
        PathDelay = 0
        threading.Thread(target=DoWaves).start()

clock.schedule_interval(FunctionCall.GetPlayers, 0.015)
clock.schedule_interval(FunctionCall.WaveUpdate, 0.1)
clock.schedule_interval(FunctionCall.ServerConnection, 0.015)


#

def on_mouse_down(pos, button):
    for en in enemies:
        if en.collidepoint(pos):
            filez.delete('Enemies/'+en.Name+".json")

#


def collects():
    global hearts, damage_boosts
    CurrentDamage = []
    CurrentHearts = []
    for heart in hearts:
        heart.draw()
        if heart.x > 0:
            CurrentHearts.append(heart)
    hearts = CurrentHearts
    for boost in damage_boosts:
        boost.draw()
        if boost.x > 0:
            CurrentDamage.append(boost)
    damage_boosts = CurrentDamage

def draw():

    screen.clear()
    for tile in map_level:
        tile.draw()
    for tile in map_level_obj:
        tile.draw()
    for other in players:
        try:
            
            other.draw()
            if "Magma" in other.username:
                screen.draw.text(other.username, center=(other.x-15, other.top-5), fontsize=15, color=(232, 185, 35), bold="true")
            else:
                screen.draw.text(other.username, center=(other.x-15, other.top-5), fontsize=15, color="black", bold="true")
            
            screen.draw.text(other.kills, center=(other.x-15, other.top+4), fontsize=15, color="black", bold="true")
        except:
            pass
    
    for en in enemies:
        en.draw()
    collects()
    Functions.draw_test()
    if saywave > 0:
        filez.send("Server/Server.json", 1, "WaveTime", "-")
        screen.draw.text("Wave "+str(CurrentWave-1), fontsize=35, color="black", bold="true", center=(WIDTH/2, HEIGHT/2))

def splashscreen():
    pyi_splash.close()
# Screen Loaded
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    clock.schedule(splashscreen, 0.5)
except:
    pass
    
#Splash end

pgzrun.go()