import pygame, os
import commentjson as json
import filez
import pgzrun
import time
from tkinter import messagebox, simpledialog
from random import randint
import logging
import threading

try:
    filez.SetUrl('http://localhost:8081/')
    from files.Class_Functions import SpriteSheet
    try:
        if os.path.getsize('Log.log') > 10 * 1024:
            os.remove('Log.log')
    except:
        pass
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    # define file handler and set formatter
    file_handler = logging.FileHandler('Log.log')
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    
except:
    pass


isweb = True
TITLE = "Dungeons"
FPS = 30
spawn_pos = (64, 128)
cell_scale = 64
block = Actor('default')
item = Actor('default', pos=(100, 100))
player = Actor('default', pos=(spawn_pos[0], spawn_pos[1]))
playbutton = Actor('default', pos=(300, 200))
playbutton = Actor('default', pos=(300, 200))
box = "a"
gameMode = "Menu"
CurrentWave = 1
players = []
enemies = []
hearts = []
displayerrors = []

damage_boosts = []
leaderboard = []
userdata = "Null"
username = "Null"
inputpass = "Null"
kills = 0
playersdelay = 0

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



def DownloadImages():
    images = filez.scan('images/')
    for image in images:
        filez.download("images/"+image, image)
def getplayer():
    global players, leaderboard, enemies
    if gameMode == "Game":
        try:
            playerdata = filez.scan('Saves/')
        except:
            return
        try:
            tempplayers = []
        except:
            pass
        for playerfilename in playerdata:
            if playerfilename != username+".json" and playerfilename != ".json" and playerfilename != '[':
                playerfile = filez.fread("Saves/"+str(playerfilename))
                try:
                    
                    otherplayer = Actor('player'+playerfile["randomskin"], bottomleft=(float(playerfile["x"]), float(playerfile["y"])) )
                    otherplayer._orig_surf = pygame.transform.scale(otherplayer._orig_surf, (otherplayer.width*0.6, otherplayer.height*0.6))
                    otherplayer._update_pos()
                    otherplayer.bottom = float(playerfile["y"])
                    otherplayer.left = float(playerfile["x"])
                    otherplayer.username = playerfile["username"]
                except Exception as e:
                    logger.info(str(e))
                if float(playerfile["numb"]) > time.time():
                    tempplayers.append(otherplayer)
        players = tempplayers
playerdelay = 0
def saveplayer():
    global kills
    try:
        if gameMode == "Game":
            killList = filez.scan("Kills/"+username)
            getplayer = filez.fread("Saves/"+username+".json")
            kills = int(getplayer["Kills"])
            for kill in killList:
                kills += 1
                filez.delete("Kills/"+username+"/"+kill)
            if player.DAMAGE/5 < 5:
                items.loads(item, (42+player.DAMAGE/5, 6, 2, "sword"))
            elif player.DAMAGE/5 < 8:
                items.loads(item, (42, player.DAMAGE/5-5, 2, "staff"))
            else:
                items.loads(item, (42, 3, 2, "staff"))
            global userdata
            userdata["y"] = str(player.bottom)
            userdata["x"] = str(player.left)
            userdata["numb"] = str(time.time()+5.0)
            userdata["Damage"] = str(player.DAMAGE)
            userdata["Health"] = str(player.HP)
            userdata["Kills"] = str(kills)
            filez.fwrite("Saves/"+username+'.json', json.dumps(userdata, sort_keys=True, indent=4), "c")
    except Exception as e:
        logger.info(str(e))
def playerdead():
    global player, CurrentWave
    player.bottom = 128
    player.left = 64
    player.DAMAGE = 5
    player.HP = 100




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


# Default sheets


items = SpriteSheet("items", (17, 17), 16, 16)
ens = SpriteSheet("Enemies", (17, 17), 16, 16, 0)
char = SpriteSheet("character", (96, 128), 96, 126, 0)
char.loads(player, (3, 2, 0.6, "idle"))
try:
    player.bottom = a_top
    player.left = a_left
except:
    player.left = spawn_pos[0]
    player.bottom = spawn_pos[1]


try:
    player.HP = a_health
    player.DAMAGE = a_damage
except:
    player.HP = 100
    player.DAMAGE = 15
    
player.isidle = 20


items.loads(item, (42, 6, 2, "sword"))

level = 1


item_pos = (0, 0)
item_angle = 0
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
WIDTH = len(map_tiles[0]["tiles"][1]) * cell_scale
HEIGHT = len(map_tiles[0]["tiles"]) * cell_scale

playbutton = Actor('default', pos=(WIDTH//2, HEIGHT//2))
changenamebutton = Actor('default',pos=(WIDTH//2, 50+HEIGHT//2))



map_level = []
map_level_obj = []

c1 = 0
textpos = 10
class Functions:
    def quicktext(text, color=(10, 10, 10), size=25):
        global textpos
        screen.draw.text(text, pos=(5, textpos), color=color, bold="true", fontsize=size)
        textpos += 30
    def draw_test():
        global textpos
        textpos = 5
        Functions.quicktext(text = "Wave: " + str(CurrentWave-1))
        Functions.quicktext(text = "Players: " + str(len(players)+1))
        Functions.quicktext(text = str(player.HP)+"HP")
        Functions.quicktext(text = "Kills: "+str(kills))
        Functions.quicktext(text = "Fps: "+getfps())

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


class MultiThreading:
    def on_key_down(key):
        global box, gameMode
        if gameMode == "Menu":
            if key == keys.RETURN:
                
                ConnectToServer()
            elif key == keys.SPACE:
                messagebox.showerror("Error", "Open tab does not work on windows version please manually launch the server")
            return
        if key == keys.W or key == keys.UP:
            
            if player.image != "up":
                char.loads(player,(0, 1, 0.6, "up"))
            player.isidle = 0
            if player.y > (cell_scale):
                player.y -= cell_scale
        elif key == keys.S or key == keys.DOWN:
            if player.image != "down":
                char.loads(player,(0, 0, 0.6, "down"))
            player.isidle = 0
            if player.y < HEIGHT-(cell_scale*3):
                player.y += cell_scale
        elif key == keys.A or key == keys.LEFT:
            if player.image != "left":
                char.loads(player,(0, 4, 0.6, "left"))
                player._orig_surf = pygame.transform.flip(player._orig_surf, True, False)
                player._surf = pygame.transform.flip(player._surf, True, False)
            player.isidle = 4
            if player.x > (cell_scale*2):
                player.x -= cell_scale
        elif key == keys.D or key == keys.RIGHT:
            if player.image != "right":
                char.loads(player,(0, 4, 0.6, "right"))
            player.isidle = 4
            if player.x < WIDTH-(cell_scale*2):
                player.x += cell_scale

    def draw():
        global saywave, CurrentWave, enemies, ens, gameMode, item_pos, item_angle, textpos
        for tile in map_level:
            tile.draw()
        for tile in map_level_obj:
            tile.draw()
        for other in players:
            try:
                if "Magma" in other.username:
                    screen.draw.text(other.username, center=(other.x, other.y-45), fontsize=15, color=(232, 185, 35), bold="true")
                else:
                    screen.draw.text(other.username, center=(other.x, other.y-45), fontsize=15, color="black", bold="true")
            except Exception as e:
                displayerrors.append(str(e))
            other.draw()
        if player.image == "up":
            item.draw()
            player.draw()
        else:
            player.draw()
            item.draw()
        
        for en in enemies:
            en.draw()
        collects()
        Functions.draw_test()
        if saywave > 0:
            screen.draw.text("Wave "+str(CurrentWave-1), fontsize=35, color="black", bold="true", center=(WIDTH/2, HEIGHT/2))
        if player.HP <= 0:
            screen.fill("black")
            screen.draw.text("You Lose", color="red", fontsize=35, center=(WIDTH/2, HEIGHT/2))
            clock.schedule(playerdead, 2)
        if player.image == "idle":
            item_pos = (player.x+18, player.y+8)
            item_angle = 0
        elif player.image == "up":
            item_pos = (player.x-6, player.y+10)
            item_angle = 0
        elif player.image == "down":
            item_pos = (player.x+12, player.y+22)
            item_angle = 70
        elif player.image == "right":
            item_pos = (player.x+34, player.y+28)
            item_angle = -50
        elif player.image == "left":
            item_pos = (player.x-12, player.y+14)
            item_angle = 50
            
        item.pos = item_pos
        item.angle = item_angle
        
        textpos = 150
        for error in displayerrors:
            Functions.quicktext(text = error, color = (200, 0, 0))

    def on_mouse_down(button, pos):
        global enemies
        try:
            for en in enemies:
                if en.collidepoint(pos):
                    filez.send("Enemies/"+en.Name+".json", username, 'Attack', '=')
                    filez.send("Enemies/"+en.Name+".json", 'Attacked', 'Status', '=')
                    filez.send("Enemies/"+en.Name+".json", player.DAMAGE, 'HP', '-')
                    if randint(1, 2) == 1:
                        sounds.hit_1.play()
                    else:
                        sounds.hit_2.play()
                        
        except Exception as e:
            displayerrors.append(str(e))

serverupdatedelay = 0
def draw():
    global saywave, CurrentWave, enemies, ens, gameMode, item_pos, item_angle, serverupdatedelay
    if gameMode == "Menu":
        screen.clear()
        screen.draw.text('PRESS ENTER TO START', center=(WIDTH//2, HEIGHT//2+100), fontsize=40)
        screen.draw.text('PRESS SPACE TO HOST', center=(WIDTH//2, HEIGHT//2+150), fontsize=40)
        
    elif gameMode == "Game":
        try:
            if serverupdatedelay == 10:
                serverupdatedelay = 0
                if not ServerConnect.ServerOnline():
                        gameMode = "Menu"
            else:
                serverupdatedelay += 1
            threading.Thread(target=MultiThreading.draw).start()
        except Exception as e:
            displayerrors.append(str(e))
            logger.info(str(e))
            
        


def takeClosest(lst, numb):
    newlst = []
    for i in lst:
        newlst.append(i - numb)
    lstt = [abs(ele) for ele in newlst]
    return lst[lstt.index(min(lstt))]

pathdelay = 0
def path_enemies():
    global pathdelay
    
    for en in enemies:
        time.sleep(0.2)
        if en.Status == "Attacked" and en.Attack == username:
            if en.left != player.left:
                list_x = [en.left+cell_scale, en.left-cell_scale]
                left = takeClosest(list_x, player.left)
                filez.send("Enemies/"+en.Name+".json", left, "LEFT", "=")
            elif en.bottom != player.bottom:
                list_x = [en.top+cell_scale, en.top-cell_scale]
                left = takeClosest(list_x, player.top)
                filez.send("Enemies/"+en.Name+".json", left, "TOP", "=")
                
            if en.left == player.left and en.bottom == player.bottom:
                Functions.taken_damage(en, player)


    

def update(dt):
    global item_pos, item_angle, gameMode
    
    
    if player.isidle != 8:
        player.isidle += 1
    elif player.image != "idle":
        player.isidle = 0
        char.loads(player,(3, 2, 0.6, "idle"))
    """for heart in hearts:
        if player.colliderect(heart):
            player.HP += randint(1,2)*10
            heart.pos = (-100, -100)
    
    for boost in damage_boosts:
        if player.colliderect(boost):
            if player.DAMAGE/5 < 8:
                player.DAMAGE += 5
            boost.pos = (-100, -100)
            items.loads(item, (42+int(player.DAMAGE/5), 6, 2, "sword"))"""
    
def on_mouse_down(button, pos):
    threading.Thread(target=MultiThreading.on_mouse_down, args=(button, pos,)).start()


def on_key_down(key):
    threading.Thread(target=MultiThreading.on_key_down, args=(key,)).start()


class ServerConnect:
    
    def ServerOnline():
        global gameMode
        try:
            Server = filez.fread("Server/Server.json")
        except:
            time.sleep(0.1)
            return True
        try:
            if Server["Online"] > time.time():
                return True
            else:
                return False
        except:
            return True
    def Update():
        try:
            global CurrentWave, saywave, enemies, ens
            GameSave = filez.fread("Server/Server.json")
            CurrentWave = GameSave["Wave"]
            saywave = GameSave["WaveTime"]
            server = filez.scan("Enemies/")
            tempenemies = []
            try:
                for i in server:
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
                    pygame.PixelArray(en._surf).replace(6553855, pygame.Color(30, 30, 30))
                    if en.HP > 0:
                        tempenemies.append(en)
                enemies = tempenemies
            except Exception as e:
                try:
                    en.Name 
                    filez.delete("Enemies/"+en.Name+".json")
                except:
                    pass
        except Exception as e:
            displayerrors.append(str(e))
            logger.critical(e)
        


def ConnectToServer():
    global gameMode, userdata, username, inputpass
    try:
        offline = False
        ServerExist = False
        ServerId = simpledialog.askstring('Server', "Enter Server Ip\nLeave Empty To Join Local Ip\n")
        if ServerId != "":
            filez.SetUrl(ServerId)
        try:
            isonline = filez.fread("Server/Server.json")
        except:
            time.sleep(1)
            return

        try:
            if isonline["Online"] < time.time():
                messagebox.showerror("Error", "Server is offline")
                offline = True
                raise
        except Exception as e:
            logger.warning(str(e))
            if offline:
                pass
            else:
                messagebox.showerror("Error", "Server does not exist")
                ServerExist = True
        if not offline and not ServerExist:
            
            username = simpledialog.askstring('UserData', 'Username: ')
            inputpass = simpledialog.askstring('UserData', 'Password: ')
            
            wrongPass = False
            CreateAccount = False
            try:
                userdatatemp = filez.fread("Saves/"+username+".json")
                savedpass = userdatatemp["password"]
            
                if savedpass == inputpass:
                    userdata = filez.fread("Saves/"+username+".json")
                    a_left = float(userdata["x"])
                    a_top = float(userdata["y"])
                    a_damage = int(userdata["Damage"])
                    a_health = int(userdata["Health"])
                    CurrentWave = int(userdata["Wave"])
                else:
                    messagebox.showerror("Error", "Account Password Does not Match")
                    wrongPass = True
                    raise
            except:
                if wrongPass:
                    raise
                else:
                    try:
                        userdata = filez.fread("Saves/"+username+".json")
                        userdata["y"] = str(player.bottom)
                        userdata["x"] = str(player.left)
                        userdata.update({"password": inputpass})
                        userdata.update({"username": username})
                        userdata.update({"randomskin": str(randint(1, 4))})
                        userdata.update({"numb": str(time.time()+5.0)})
                        userdata.update({"Damage": "5"})
                        userdata.update({"Health": "100"})
                        userdata.update({"Wave": "1"})
                        userdata.update({"Kills": "0"})
                        filez.fwrite("Saves/"+username+".json", json.dumps(userdata, sort_keys=True, indent=4), "c")
                    except:
                        pass

            gameMode = "Game"
    except Exception as e:
        logger.error(e)
saveplayersDelay = 0
GetplayersDelay = 0
ServerConnectionDelay = 0
PathDelay = 0
class FunctionCall:
    def SavePlayer():
        global saveplayersDelay
        if saveplayersDelay != 15:
            saveplayersDelay += 1
            return
        saveplayersDelay = 0
        threading.Thread(target=saveplayer).start()

    def GetPlayers():
        global GetplayersDelay
        if GetplayersDelay != 20:
            GetplayersDelay += 1
            return
        GetplayersDelay = 0
        threading.Thread(target=getplayer).start()
            
    def ServerConnection():
        global ServerConnectionDelay
        if ServerConnectionDelay != 15:
            ServerConnectionDelay += 1
            return
        ServerConnectionDelay = 0
        threading.Thread(target=ServerConnect.Update).start()
    def Enemie_path():
        global PathDelay, displayerrors
        if PathDelay != 30:
            PathDelay += 1
            return
        if len(displayerrors) >= 1:
            if randint(1, 2) == 1:
                del displayerrors[0]
        PathDelay = 0
        threading.Thread(target=path_enemies).start()
        
clock.schedule_interval(FunctionCall.SavePlayer, 0.025)
clock.schedule_interval(FunctionCall.GetPlayers, 0.025)
clock.schedule_interval(FunctionCall.ServerConnection, 0.02)
clock.schedule_interval(FunctionCall.Enemie_path, 0.015)


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
