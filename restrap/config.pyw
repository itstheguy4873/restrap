import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import os
import subprocess
import psutil
import json
import sys

def openwindow():

    robloxprocesses = ['RobloxPlayerBeta.exe', 'RobloxCrashHandler.exe', 'RobloxStudio.exe', 'RobloxPlayerLauncher.exe']
    
    if any(i.name() in robloxprocesses for i in psutil.process_iter()):
        if messagebox.askquestion('Warning', 'ROBLOX Must be closed to edit settings.\nClose ROBLOX?', icon='warning') == "no":
            sys.exit()

    main = tk.Tk()
    
    def readconfig():
        with open('config.json', 'r') as f:
            print('read config')
            return json.load(f)

    config = readconfig()

    def getconfigval(read):
        print('returned config val')
        return config.get(read)

    tktheme = getconfigval('tktheme')
    themever = getconfigval('tkthemever')

    try:

        subprocess.call("taskkill /IM RobloxPlayerBeta.exe", shell=True)
        print('killed roblox client')
        subprocess.call("taskkill /IM RobloxCrashHandler.exe", shell=True)
        print('killed roblox crash handler')
        subprocess.call("taskkill /IM RobloxStudio.exe", shell=True)
        print('killed roblox studio')
        subprocess.call("taskkill /IM RobloxPlayerLauncher.exe", shell=True)
        print('killed roblox launcher')
        
    except subprocess.CalledProcessError as e:

        pass
    
    main.tk.call("source", f"{tktheme}.tcl")
    main.tk.call("set_theme", themever)
    main.geometry("600x400")
    main.resizable(False, False)
    main.iconbitmap("restrap_logo.ico")
    main.title('restrap')
    main.attributes('-topmost', True)
    print('created window')

    def injectfastflags():
        for file in sorted(Path(os.path.expandvars(r'%LOCALAPPDATA%\Roblox\Versions')).iterdir(), key=os.path.getmtime):
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
                            json.dump({}, f)
                            print('dumped json!')
                            clientappsettings = os.path.join(path, 'ClientSettings', 'ClientAppSettings.json')
                            subprocess.Popen(['notepad.exe', clientappsettings])
                            print('opened json!')

    def changetheme(theme, tktheme, ver):
        with open('config.json', 'r+') as f:
            data = json.load(f)
            data['theme'] = theme
            data['tktheme'] = tktheme
            data['tkthemever'] = ver
            messagebox.showinfo('Notice', 'Settings must be closed to apply settings.')
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def openrobloxfile():
        def getrblxpath():
            for file in sorted(Path(os.path.expandvars(r'%LOCALAPPDATA%\Roblox\Versions')).iterdir(), key=os.path.getmtime):
                print('in for loop')
                path = os.path.abspath(file)
                if os.path.exists(os.path.join(path, 'RobloxCrashHandler.exe')):
                    return path
        rblxpath = getrblxpath()
        subprocess.Popen(f'explorer {rblxpath}')

    themeboxtext = tk.Label(text='restrap Theme')
    themeboxtext.place(x='30', y='5')

    themebox = ttk.Combobox(main, values=['Azure Light', 'Azure Dark'])
    themebox.pack(anchor='nw', pady='30', padx='30')
    themebox.set(getconfigval('theme'))

    themebox.bind('<<ComboboxSelected>>',
                  lambda event: changetheme(themebox.get(),
                                            'azure',
                                            'light' if themebox.get() == 'Azure Light' else 'dark'))  # 'light' or 'dark' for themeve
    
    rbxinstallbtn = tk.Button(main, text='Open Roblox Installation', command=openrobloxfile)
    rbxinstallbtn.pack(anchor='nw', pady='30', padx='30')

    fastflagbutton = tk.Button(main, text='Open FastFlag List', command=injectfastflags)
    fastflagbutton.pack(anchor='nw', pady='30', padx='30')

    main.mainloop()

