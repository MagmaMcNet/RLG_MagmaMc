import os, threading, time, random, shutil, keyboard, sys

print("\n")
print("\n")
Updates = 0
print("PRESS Q TO STOP")
time.sleep(2)
threads = []

try:
    shutil.rmtree('dist/Data')
except:
    pass
try:
    shutil.rmtree('dist/Server')
except:
    pass
try:
    shutil.rmtree('dist/RLG')
except:
    pass


def defclient():
    global Updates
    os.system('cmd /c "call _Compile_\client.bat"')



    Updates += 1


def defserver():
    global Updates
    os.system('cmd /c "call _Compile_\server.bat"')


    Updates += 1

def zip():
    global per
    os.system(f'cmd /c "7Zip\\7z.exe'+' a dist/Build_Windows.zip dist/"')
    per = 98

client = threading.Thread(target=defclient)
server = threading.Thread(target=defserver)

client.start()
server.start()

threads.append(client)
threads.append(server)



per = 0
printp = 0

while True:
    time.sleep(0.02)
    if keyboard.is_pressed('q'):
        sys.exit(0)
        
    if printp >= 1:
        printp = 0
        print(str(per)+"%")
    else:
        printp += 1
    if random.randint(1, 18) == 1 and per != 100:
        per += 1
    if per == 100:
        print("100%")
        sys.exit(0)
    if Updates == 4:
        break
    elif Updates == 2:
        os.chdir("dist/")
        shutil.move('Server', 'Data')
        os.chdir("../")
        Updates += 1
    elif Updates == 3:
        threading.Thread(target=zip).start()
        Updates = 5
        
        


