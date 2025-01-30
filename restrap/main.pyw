from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
import requests
import os
import subprocess
import sys

main = tk.Tk()

main.tk.call("source", "azure.tcl")
main.tk.call("set_theme", "dark")
main.geometry("400x150")
main.configure(background="black")
main.resizable(False, False)
main.iconbitmap("restrap_logo.ico")
main.title('restrap')

def openroblox():
    main.destroy()
    robloxdir = str(sorted(Path(os.path.expandvars(r'%LOCALAPPDATA%\Roblox\Versions')).iterdir(), key=os.path.getmtime, reverse=True)[0] / 'RobloxPlayerInstaller.exe')
    subprocess.Popen(robloxdir)
    sys.exit()

whatlabel = tk.Label(main, text='What would you like to do?', bg='black')
whatlabel.pack(anchor='nw', padx=5)

openbutton = tk.Button(main, text='Open ROBLOX', width='13', command=openroblox)
openbutton.config(anchor="w", padx=10)
openbutton.pack(anchor='nw', padx=10, pady=20)

def configroblox():
    directory = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(os.path.join(directory, 'config.pyw'), shell=True)
    sys.exit()

configbutton = tk.Button(main, text='Configure ROBLOX', width='16', command=configroblox)
configbutton.config(anchor="w", padx=10)
configbutton.pack(anchor='nw', padx=10, pady=10)

logo = Image.open('restrap_logo.png').resize((100,100))
logotk = ImageTk.PhotoImage(logo)
logolabel = tk.Label(main, image = logotk, background='black')
logolabel.place(x=180,y=25)

restraplabel = tk.Label(main, text='restrap 1.0.0', bg='black')
restraplabel.place(x=300, y=50)

main.mainloop()

