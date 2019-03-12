import json
import time
import subprocess
import urllib.request
import urllib.parse
from scriptHelper import *
import os

def countdown(time_d):
	while time_d > 0:
		if (time_d < 100):
			if(time_d < 10):
				print ("Waiting: " + str(time_d), end="\r")
			else:
				print ("Waiting: " + str(time_d), end="\r")
		else:
			print("Waiting: " + str(time_d), end="\r")
		time.sleep(1)
		time_d = time_d - 1

with open('configuration.json') as f:
	data = json.load(f)
	
ffmpeg_location = data["ffmpeg_location"]
sox_location = data["sox_location"]
thread_raw = data["thread"]
magick_location = data["magick_location"]
chrome_location = data["chrome_driver_location"]

print ("FFMPEG LOCATION: " + ffmpeg_location)
print ("SOX LOCATION: " + sox_location)
print ("THREAD URL: " + thread_raw)
print ("MAGICK LOCATION" + magick_location)
		
if not thread_raw.endswith("/"):
	thread = thread_raw + "/.json"
else:
	thread = thread_raw + ".json"
print ("Using: " + thread)

request = urllib.request.Request(
	thread,
	data=None,
	headers={
		'User-Agent': 'Crawl-Bot by tooxo'
	}
)
	
callback = urllib.request.urlopen(request).read()
json = json.loads(callback)
title = json[0]["data"]["children"][0]["data"]["title"]
	
comments = json[1]["data"]["children"]
linklist = []
textlist = []
for comment in comments: 
	try:
		permalink = "https://www.reddit.com" + comment["data"]["permalink"]
		linklist.append(permalink)
		body = comment["data"]["body"]
		body = body.replace("&amp;#x200B;", "")
		textlist.append(body)
	except:
		continue

print ("Length: " + str(len(linklist)))

o = 0

voice_check = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "-o", "./test.mp3", "a"]
output = subprocess.check_output(voice_check)
if "Invalid" in str(output):
	use = "backup"
else:
	use = "main"

os.remove("./test.mp3")

lengthlist = []	

for text in textlist:
	if use == "main":
		voice = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "-o", "./assets/audio/" + str(o) + ".wav", text]
	else:
		voice = ["./assets/voice.exe", "-n", "Microsoft David Desktop", "-o", "./assets/audio/" + str(o) + ".wav", text]
	subprocess.call(voice)
	
	convert = [sox_location, "--norm", "./assets/audio/" + str(o) + ".wav", "./assets/audio/" + str(o) + "_a.mp3"]
	subprocess.call(convert)
	
	padding = [sox_location, "--norm", "./assets/audio/" + str(o) + "_a.mp3", "./assets/audio/" + str(o) + ".mp3", "pad", "0", "0.5"]
	subprocess.call(padding)
	
	check_length = [sox_location, "--i", "-D", "./assets/audio/" + str(o) + "_a.mp3"]
	length = subprocess.check_output(check_length)
	lengthlist.append(length.decode('utf-8'))
	
	o = o + 1

if use == "main":
	voice = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "-o", "./assets/audio/title.wav", title]
else: 
	voice = ["./assets/voice.exe", "-n", "Microsoft David Desktop", "-o", "./assets/audio/title.wav", title]

subprocess.call(voice)
convert = [sox_location, "--norm", "./assets/audio/title.wav", "./assets/audio/title_a.mp3"]
padding = [sox_location, "--norm", "./assets/audio/title_a.mp3", "./assets/audio/title.mp3", "pad", "0", "2"]
subprocess.call(convert)
subprocess.call(padding)
	
c = 0
for link in linklist:
	countdown(3)
	filename = c
	wget = ["curl", "--progress-bar", "-o", "temp/" + str(filename) + ".html", "-A", "CraWlER bY ToXoo", link]
	subprocess.call(wget)
	print ("Done:" + str(c + 1) + " / " + str(len(linklist)))
	c = c + 1
print ("Finished downloading Comments. Going to modify.")

for x in range(0, len(linklist)):
	try:
		modifyComment(x)
	except:
		break



countdown(2)
wget = ["curl", "-o", "./assets/temp/title_temp.html", "-A", "CRAwL TooxO", thread_raw]
subprocess.call(wget)
modify("./assets/temp/title_temp.html", "./assets/temp/title.html")

screenshot(linklist, "./assets/temp/title.html", chrome_location)
cropAndMove(magick_location, linklist, "./assets/temp/title.png")
imageToVideo(ffmpeg_location, linklist, lengthlist)
addTheAudio(ffmpeg_location, linklist, "./assets/audio/title.mp3", "./assets/video_silent/title.mp4")
renderComplete(ffmpeg_location, linklist)

addMusicAndOutro(ffmpeg_location)

print("CLEANING UP IN 10")
countdown(9)
cleanUP()