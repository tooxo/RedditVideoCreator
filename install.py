from urllib.request import urlretrieve
import urllib
import zipfile
import os
import subprocess

print("Installing all the dependencies.")
url_sox = "https://downloads.sourceforge.net/project/sox/sox/14.4.2/sox-14.4.2-win32.zip?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fsox%2Ffiles%2Fsox%2F14.4.2%2Fsox-14.4.2-win32.zip%2Fdownload%3Fuse_mirror%3Dautoselect&ts=1553364475&use_mirror=autoselect" #yes
url_imagemagick = "ftp://ftp.imagemagick.org/pub/ImageMagick/binaries/ImageMagick-6.9.10-34-portable-Q16-x64.zip" #yes
url_ffmpeg = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v4.1/ffmpeg-4.1-win-64.zip" #yes
url_voice = "https://drive.google.com/uc?authuser=0&id=15j8nEpu3D4ezbTy2Hz_Tr7PjOYKPPKFM&export=download" #yes
url_selenium = "https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_win32.zip" #yes
url_lame = "https://drive.google.com/uc?authuser=0&id=1AIDh9smIQrtDzXQyjEnjTLZd3c0ca9pG&export=download" #yes

user_agents = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11', 'Opera/9.25 (Windows NT 5.1; U; en)', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)', 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12', 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9']

print("Downloading SOX")
urlretrieve(url_sox, './temp/sox.zip')

print("Downloading SOX-Lame")
urlretrieve(url_lame, './temp/lame.zip')

print("Downloading ImageMagick")
urlretrieve(url_imagemagick, './temp/im.zip')

print("Downloading FFMPEG")
urlretrieve(url_ffmpeg, './temp/ffmpeg.zip')

print("Downloading Chrome Driver")
urlretrieve(url_selenium, './temp/chrome.zip')

print("Installing...")
print("Extracting FFMPEG")
if not os.path.exists("./assets/bin/ffmpeg/"):
    os.mkdir("./assets/bin/ffmpeg")
zip = zipfile.ZipFile("./temp/ffmpeg.zip", "r")
zip.extractall("./assets/bin/ffmpeg/")
zip.close()

print("Extracting Chrome Driver")
if not os.path.exists("./assets/bin/chromedriver/"):
    os.mkdir("./assets/bin/chromedriver/")
zip = zipfile.ZipFile("./temp/chrome.zip", "r")
zip.extractall("./assets/bin/chromedriver/")
zip.close()

print("Installing Selenium Python Module")
pyinst = ["py", "-m", "pip", "install", "selenium"]
subprocess.call(pyinst)
pyinst = ["py", "-m", "pip", "install", "lxml"]
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

urlretrieve(url_voice, './temp/Daniel.exe')
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")
print("Install the Daniel.exe from the temp directory, folder isnt important.")

print("Removing Temporary Files.")
os.remove("./temp/sox.zip")
os.remove("./temp/im.zip")
os.remove("./temp/chrome.zip")
os.remove("./temp/lame.zip")
os.remove("./temp/ffmpeg.zip")

input("Press Any Key to close...")
