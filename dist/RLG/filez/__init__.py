import requests as request
from tkinter import messagebox
import json, time
ID = "notset"
DEVELOPER = False
VERSION = "1.1.0"
baseurl = 'http://example.com'
DeprecatedMessages = 0
def SetUrl(URL):
    global baseurl
    baseurl = "http://"+str(URL)+":8081/"
def _colorit(rgb, text):
    r, g, b = rgb
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)
def _check():
    global DeprecatedMessages
    if ID != "notset" and DeprecatedMessages < 2:
        DeprecatedMessages += 1
        print(_colorit((255, 0, 0), "ID Is Deprecated\n will soon be taken out"))
    
    if baseurl == "http://example.com":
        errortext = """
               filez.SetUrl(), not set,
               please set and make sure that You have A Server Running
               Create on at File The FILEZ/
              """

        _senderror(errortext)
        return False
    else:
        return True
def _senderror(text):
    print(_colorit((255, 0, 0), text))
    messagebox.showerror("Error", text)

def fread(file):
    if _check():
        try:
            Rfile = json.loads(str(request.get(baseurl+"?filez=read&filename="+file).text))
        except:
            time.sleep(1)
            return
        if Rfile == "notexist":
            _senderror("""
                     Please Make Sure That The Project/Folder Your Trying To Read From Exists,
                     http://magma-mc.net/projects.php
                    """)
            return False
        return Rfile
    else:
        raise
def scan(folder="/", ReadFile=False):
    if _check():
        try:
            Rfolder = str(request.get(str(baseurl)+"?filez=scan&filename="+str(folder)).text)
        except:
            time.sleep(2)
            return
        
        if Rfolder == "notexist":
            _senderror("""
                        Please Make Sure That The Project/Folder Your Trying To Read From Exists,
                        http://magma-mc.net/projects.php
                       """)
            return False
        elif ReadFile:
            if DEVELOPER == True:
                eval('print(Rfolder, "BEFORE SNIP", "\\n")')
            Rfolder = list([i.strip() for i in Rfolder.split('"') if len(i.strip().strip(',').strip(']').strip('['))>0])
            if DEVELOPER == True:
                eval('print(Rfolder, "AFTER SNIP", "\\n")')

            files = {}
            for filename in Rfolder:
                if DEVELOPER == True:
                    eval('print(str(fread(folder+filename)), "STR.FREAD.FOLDER+FILENAME", "\\n")')
                file = json.loads(str(fread(folder+filename)))
                files.update({filename: (json.dumps(file))})
            return files
        return json.loads(Rfolder)
    else:
        raise
def fwrite(file, data, type="c"):
    if _check():
        try:
            # check if data is json
            temp = json.loads(data)
        except:
            _senderror("""Please Make Sure That The data your Trying To Save Is Json""")
            raise
        try:
            Wfile = str(request.post(baseurl+"?filez=write&content="+data+"&filename="+file+"&type="+type).text)
        except:
            time.sleep(2)
            return
        if Wfile == "notexist":
            _senderror("""
                        Please Make Sure That The Project Your Trying To Write To Exists,
                        http://magma-mc.net/projects.php
                       """)
            return False
        return True
    else:
        raise
def send(file, data, key="null", type="=", stringit = False):
    if _check():
        try:
            File = fread(file)
            if key == "null":
                File = data
            else:
                if type == "=":
                    File[key] = data
                elif type == "+":
                    if stringit:
                        File[key] = str( int(File[key]) + int(data) )
                    else:
                        File[key] = int(File[key]) + int(data)
                elif type == "-":
                    File[key] = int(File[key]) - int(data)
            fwrite(file, json.dumps(File))
        except:
            pass
def delete(file):
    if _check():
        try:
            request.post(baseurl+"?filez=delete&filename="+file)
        except:
            pass
def upload(file, filename):
    files = {'file': open(file, 'rb')}
    r = request.post(baseurl+"?filez=upload&filename="+filename, files=files)
def download(filename, file):
    response = request.get(baseurl+"?filez=download&filename="+filename)
    if response.status_code == 200:
        with open('images/'+file, 'wb') as f:
            f.write(response.content)

print("\nFilez Successfully Started.\n")