from requests import get
import socket, threading, os, sys
from tkinter import simpledialog
print(sys.version)
def _colorit(rgb, text):
    r, g, b = rgb
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

hostname = socket.gethostname()  
localip = socket.gethostbyname(hostname)
ip = get('https://api.ipify.org').text
PORT = 8081
Name = "Filez"
Start = True
Lines = "\n                                                                           \n                  "
if __name__ == "__main__":
    Start = False
    PORT = simpledialog.askinteger("Port Forwarder", f"{Lines}Enter Port to Forward")
    Name = simpledialog.askstring("Port Forwarder", f"{Lines}Enter Name Of Port")
    if PORT > 20 and PORT < 56533:
        pass
    else:
        print("PORT > 20 and PORT < 56533")
        sys.exit(1)

from colorama import init, Fore, Back, Style
init(autoreset=True)
def PHPStart():
    os.system(f'cmd /c "cd filez/ & PHP -S {localip}:{PORT} FILEZ.php"')
def AddPort():
    os.system(f'cmd /c "cd filez/ & upnpc.exe -e "{Name}_" -a {localip} {PORT} {PORT} TCP"')




threading.Thread(target=AddPort).start()
if Start:
    threading.Thread(target=PHPStart).start()
    print(f'{Fore.GREEN}Starting PHP FILEZ Server')

 

print(f'Local IP address is:{Fore.RED}   {localip}:{PORT}')
print(f'public IP address is:{Fore.RED}  {ip}:{PORT}')

