import requests
import zipfile
import io
import os
import shutil
import stat
import subprocess
import tkinter as tk
import sys
import json
import threading
import psutil
from tkinter import ttk

def readconfig():
    with open('config.json', 'r') as f:
        print('read config')
        return json.load(f)

configure = readconfig()

def getconfigval(read):
    print('returned config val')
    return configure.get(read)

tktheme = getconfigval('tktheme')
themever = getconfigval('tkthemever')

main = tk.Tk()
main.title('restrap Updater')
main.geometry('400x75')
main.tk.call("source", f"{tktheme}.tcl")
main.tk.call("set_theme", themever)
main.iconbitmap('update_icon.ico')
main.resizable(False,False)

progress = ttk.Progressbar(main, length=100)
progress.place(y=5, x=150)

url = 'https://api.github.com/repos/itstheguy4873/restrap/releases/latest'

def getlatest():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for asset in data.get('assets', []):
            if asset['name'].endswith('.zip'):
                main.after(0, lambda: progress.step(25))
                main.update()
                return asset['browser_download_url']
    print('could not fetch latest release')
    return None

def downloadextract(url, extractto='.'):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zipped:
            temppath = os.path.join(extractto, 'upd_restrap_temp')
            zipped.extractall(temppath)
            print('extracted files to temp path')
            extracted = [f for f in os.listdir(temppath) if os.path.isdir(os.path.join(temppath, f))]
            if extracted:
                subpath = os.path.join(temppath, extracted[0])
                print('preparing to move files')
                for item in os.listdir(subpath):
                    srcpath = os.path.join(subpath, item)
                    destpath = os.path.join(extractto, item)

                    if os.path.exists(destpath):
                        if os.path.isdir(destpath):
                            shutil.rmtree(destpath)
                        else:
                            os.remove(destpath)
                    
                    shutil.move(srcpath, extractto)
                    print('updated file')
                
            shutil.rmtree(temppath)
            print('cleaned up')
            main.after(0, lambda: progress.step(25))
            main.update()
    else:
        print('failed to download zip, status:', response.status_code)

def update():
    main.after(0, lambda: progress.step(25))
    zipurl = getlatest()
    if zipurl:
        version = open('version.info', 'r').read()
        def getgithubtag():
            try:
                url = 'https://api.github.com/repos/itstheguy4873/restrap/releases/latest'
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                tag = data.get('tag_name')
                if tag:
                    return tag
                else:
                    print('could not fetch tag')
                    return None
            except requests.exceptions.RequestException as e:
                print('could not fetch release')
                return None
        latestver = getgithubtag()
        if not version == latestver:
            print('downloading and extracting')
            downloadextract(zipurl, os.getcwd())
            print('done')
            exedir = os.path.join(os.getcwd(), 'restrap.exe')
        
            for proc in psutil.process_iter(['pid', 'name']):
                process_name = 'restrap.exe'
                if proc.info['name'] and process_name.lower() in proc.info['name']:
                    proc.terminate()
                    proc.wait(timeout=2)

            os.chmod(exedir, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
            
            subprocess.Popen([exedir])
            main.after(0, lambda: progress.step(25))
            main.update()
            main.after(5000, main.destroy)
        else:
            exedir = os.path.join(os.getcwd(), 'restrap.exe')
        
            for proc in psutil.process_iter(['pid', 'name']):
                process_name = 'restrap.exe'
                if proc.info['name'] and process_name.lower() in proc.info['name']:
                    proc.terminate()
                    proc.wait(timeout=2)

            os.chmod(exedir, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
            
            subprocess.Popen([exedir])

threading.Thread(target=update, daemon=True).start()
main.mainloop()
