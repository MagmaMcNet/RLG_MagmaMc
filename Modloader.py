import filez, requests
import commentjson as json
localip = requests.get('https://api.ipify.org').text
filez.SetUrl(localip)

try:
    root = "../"
    Settings = json.load(open("../ServerConfig.json"))
except:
    root = ""
    Settings = json.load(open("ServerConfig.json"))


ModNames = []
if not Settings["Modloader"]["Enabled"]:
    # Load Core
    ModList = ["Core_Enemies.json"]
else:
    # Load Modded
	ModList = Settings["Modloader"]["Mods"]
 
for Mod in ModList:
	f = json.load(open(root+"Mods/"+Mod))
	
	filez.send("Mods/"+Mod, f)

def GetModdedEnemies():
	global ModNames
	Mods = []
	del ModNames[:]
	for Mod in filez.scan('Mods/'):
		mod = filez.fread('Mods/'+Mod)
		if Mod in ModList:
			ModNames.append(mod["Name"])
			Mods.append(mod["Enemies"])
		else:
			filez.delete('Mods/'+Mod)
	return Mods
def GetMods():
	Mods = []
	try:
		for Mod in filez.scan('Mods/'):
			try:
				mod = filez.fread('Mods/'+Mod)
			except:
				pass
				return []
			if Mod in ModList:
				try:
					Mods.append(mod["Name"])
				except:
					pass
	except:
		pass
	return Mods

def UploadImages():
	for Mod in ModList:
		ModFile = json.load(open(root+"Mods/"+Mod))
		for Image in ModFile["Images"]:
			try:
				filez.upload(root+'Mods/Images/'+ModFile["Images"][Image]["FileName"], 'images/'+ModFile["Images"][Image]["FileName"])
			except:
				pass

def GetImage(uuid):
	for Mod in ModList:
		ModFile = json.load(open(root+"Mods/"+Mod))
		for Image in ModFile["Images"]:
			if Image == uuid:
				return root+'Mods/Images/'+ModFile["Images"][Image]["FileName"]
def GetScale(uuid):
	for Mod in ModList:
		ModFile = json.load(open(root+"Mods/"+Mod))
		for Image in ModFile["Images"]:	
			print(Image)
			if Image == uuid:
				return ModFile["Images"][Image]["Scale"]
    
def DownloadImages():
    images = filez.scan('images/')
    print(images)
    for image in images:
        print(image)
        filez.download("images/"+image, image)