import requests
import zipfile
import io
import os
import shutil


def update():
    url = 'https://api.github.com/repos/itstheguy4873/restrap/releases/latest'

    def getlatest():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for asset in data.get('assets', []):
                if asset['name'].endswith('.zip'):
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
        else:
            print('failed to download zip, status:', response.status_code)

    zipurl = getlatest()
    if zipurl:
        print('downloading and extracting')
        downloadextract(zipurl, os.getcwd())
        print('done')
