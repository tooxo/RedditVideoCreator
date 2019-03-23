from urllib.request import urlretrieve
import requests
import zipfile
import os
import subprocess

print("Installing all the dependencies.")
url_sox = "https://downloads.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2-win32.zip?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fsox%2Ffiles%2Fsox%2F14.4.2%2Fsox-14.4.2-win32.zip%2Fdownload%3Fuse_mirror%3Dautoselect&ts=1553364475&use_mirror=autoselect" #yes
url_imagemagick = "ftp://ftp.imagemagick.org/pub/ImageMagick/binaries/ImageMagick-6.9.10-34-portable-Q16-x64.zip" #yes
url_ffmpeg = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.1.1-win64-static.zip" #yes
url_voice = "https://drive.google.com/uc?authuser=0&id=15j8nEpu3D4ezbTy2Hz_Tr7PjOYKPPKFM&export=download" #yes
url_selenium = "https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32.zip" #yes
url_lame = "http://www.rarewares.org/files/mp3/libmp3lame-3.99.5x64.zip" #yes

print("Downloading SOX")
r = requests.get(url_sox, allow_redirects=True)
open("./temp/sox.zip", "wb").write(r.content)

print("Downloading SOX-Lame")
r = requests.get(url_lame, allow_redirects=True)
open("./temp/lame.zip", "wb").write(r.content)

print("Downloading ImageMagick")
urlretrieve(url_imagemagick, './temp/im.zip')

print("Downloading FFMPEG")
r = requests.get(url_ffmpeg, allow_redirects=True)
open("./temp/ffmpeg.zip", "wb").write(r.content)

print("Downloading Chrome Driver")
r = requests.get(url_selenium, allow_redirects=True)
open("./temp/chrome.zip", "wb").write(r.content)

print("Installing...")
print("Extracting FFMPEG")
if os.path.exists("./assets/bin/ffmpeg/"):
    os.remove("./assets/bin/ffmpeg")
zip = zipfile.ZipFile("./temp/ffmpeg.zip", "r")
zip.extractall("./assets/bin/")
zip.close()
os.rename("./assets/bin/ffmpeg-4.1.1-win64-static", "./assets/bin/ffmpeg/")

print("Extracting Chrome Driver")
if not os.path.exists("./assets/bin/chromedriver/"):
    os.mkdir("./assets/bin/chromedriver/")
zip = zipfile.ZipFile("./temp/chrome.zip", "r")
zip.extractall("./assets/bin/chromedriver/")
zip.close()

print("Installing Selenium Python Module")
pyinst = ["py", "-m", "pip", "install", "selenium"]
subprocess.call(pyinst)

print("Extracting ImageMagick")
if not os.path.exists("./assets/bin/imagemagick/"):
    os.mkdir("./assets/bin/imagemagick/")
zip = zipfile.ZipFile("./temp/im.zip", "r")
zip.extractall("./assets/bin/imagemagick/")
zip.close()

print("Installing SOX")
if os.path.exists("./assets/bin/sox/"):
    os.remove("./assets/bin/sox/")
zip = zipfile.ZipFile("./temp/sox.zip", "r")
zip.extractall("./assets/bin/")
zip.close()
os.rename("./assets/bin/sox-14.4.2/", "./assets/bin/sox/")

print("Installing SOX-Lame")
zip = zipfile.ZipFile("./temp/lame.zip", "r")
zip.extractall("./assets/bin/sox/")
zip.close()

txt = input("Do you want to download the Voice? (Y/N) caps is required")
if txt == "Y":
    r = requests.get(url_voice, allow_redirects=True)
    open("./temp/voice.exe", "wb").write(r.content)
    print("Install the Daniel.exe from the temp directory, folder isnt important.")

print("Removing Temporary Files.")
os.remove("./temp/sox.zip")
os.remove("./temp/im.zip")
os.remove("./temp/chrome.zip")
os.remove("./temp/lame.zip")
os.remove("./temp/ffmpeg.zip")

input("Press Any Key to close...")
