from requests import get
import socket, threading, os, webbrowser, ctypes, sys

port = 43210
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _colorit(rgb, text):
    r, g, b = rgb
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

hostname = socket.gethostname()  
localip = socket.gethostbyname(hostname)
ip = get('https://api.ipify.org').text

def PHPStart():
	print(_colorit((255, 0, 200),'Starting PHP FILEZ Server'))
	os.system(f'cmd /c "PHP -S {localip}:8081 FILEZ.php"')
def AddPort():
	os.system(f'cmd /c "call FirstTimeRun.bat"')

threading.Thread(target=AddPort).start()
threading.Thread(target=PHPStart).start()

print(f'Local IP address is:   {localip}:8081')
print(f'public IP address is:  {ip}:8081')

webbrowser.open(f'http://{ip}:8081')
