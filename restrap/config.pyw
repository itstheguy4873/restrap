import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import os
import subprocess
import time
import psutil
import json
import ctypes
import sys

main = tk.Tk()

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

if "RobloxPlayerBeta.exe" in (i.name() for i in psutil.process_iter()):
    if not messagebox.askyesno('Warning', 'ROBLOX Must be closed to edit settings.\nClose ROBLOX?'):
        sys.exit()
else:
    pass

subprocess.call("taskkill /IM RobloxPlayerBeta.exe", shell=True)
main.tk.call("source", "azure.tcl")
main.tk.call("set_theme", "dark")
main.geometry("600x400")
main.configure(background="black")
main.resizable(False, False)
main.iconbitmap("restrap_logo.ico")
main.title('restrap')

def injectfastflags():
    for file in sorted(Path(os.path.expandvars('%LOCALAPPDATA%\Roblox\Versions')).iterdir(), key=os.path.getmtime):
        print('in for loop')
        path = os.path.abspath(file)
        if os.path.exists(os.path.join(path, 'RobloxCrashHandler.exe')):
            if not os.path.exists(os.path.join(path, 'ClientSettings')):
                os.mkdir(os.path.join(path, 'ClientSettings'))
                paththesecondslonglostcousinremovedtwice = os.path.join(path, 'ClientSettings')
                paththesecond = os.path.join(paththesecondslonglostcousinremovedtwice, 'ClientAppSettings.json')
                print('robloxcrashhandler exists! made clientsettings')
                with open(paththesecond, 'w') as f:
                    subprocess.Popen(["notepad.exe", paththesecond])
            else:
                paththesecondslonglostcousinremovedtwice = os.path.join(path, 'ClientSettings')
                print('clientsettings and robloxcrashhandler exists!')
                with open(os.path.join(paththesecondslonglostcousinremovedtwice, 'ClientAppSettings.json'), 'w') as f:
                    if os.path.exists(os.path.join(path, 'ClientSettings', 'ClientAppSettings.json')):
                        json.dump({},f)
                        print('dumped json!')
                        clientappsettings = os.path.join(path, 'ClientSettings', 'ClientAppSettings.json')
                        subprocess.Popen(['notepad.exe', clientappsettings,])
                        print('opened json!')

                
fastflagbutton = tk.Button(main, text = 'Open FastFlag List', command=injectfastflags)
fastflagbutton.pack(anchor='nw', pady='30', padx='30')
main.mainloop()


