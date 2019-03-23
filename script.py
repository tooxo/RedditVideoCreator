import json
import time
import subprocess
import urllib.request, urllib.parse
from scriptHelper import *
import os
import threading

def countdown(time_d):
	while time_d > 0:
		print("                                                                   ", end="\r")
		print ("Waiting: " + str(time_d), end="\r")
		time.sleep(1)
		time_d = time_d - 1

with open('configuration.json') as f:
	data = json.load(f)

ffmpeg_location = data["ffmpeg_location"]
sox_location = data["sox_location"]
thread_raw = data["thread"]
magick_location = data["magick_location"]
chrome_location = data["chrome_driver_location"]
dark_mode = data["dark_mode"]
shuffle = data["shuffle"]

collection = dict()

print ("FFMPEG LOCATION: " + ffmpeg_location)
print ("SOX LOCATION: " + sox_location)
print ("THREAD URL: " + thread_raw)
print ("MAGICK LOCATION: " + magick_location)

thread = thread_raw + ".json"

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

index = 0

for comment in json[1]["data"]["children"]:
	if comment["kind"] == "more":
		break
	collection[index] = {}
	collection[index]["ID"] = str(index)
	try:
		collection[index]["LINK"] = "https://www.reddit.com" + comment["data"]["permalink"]
	except:
		break

	body = comment["data"]["body"]

	try:
		body = body.replace("&amp;#x200B;", "")
	except Exception:
		pass

	try:
		body = body.replace("&amp", "")
	except Exception:
		pass

	collection[index]["TEXT"] = body
	collection[index]["AUTHOR"] = comment["data"]["author"]
	index = index+1


print ("Length: " + str(len(collection)))

o = 0

voice_check = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "-o", "./test.mp3", "a"]
output = subprocess.check_output(voice_check)
if "Invalid" in str(output):
	use = "backup"
else:
	use = "main"

os.remove("./test.mp3")

lengthlist = []
threadlist = []

titlefolder = stringTitle(title)[:20]

if not os.path.exists(("./output/" + titlefolder)):
	os.mkdir("./output/" + titlefolder)

if use == "main":
	voice = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "--khz", "48", "-o", "./assets/audio/" + "title" + ".wav", title]
else:
	voice = ["./assets/voice.exe", "-n", "Microsoft David Desktop", "--khz", "48", "-o", "./assets/audio/title.wav", title]

subprocess.call(voice)
convert = [sox_location, "--norm", "./assets/audio/title.wav", "./assets/audio/title_a.mp3"]
subprocess.call(convert)
padding = [sox_location, "--norm", "./assets/audio/title_a.mp3", "./assets/audio/title.mp3", "pad", "0", "0.5"]
subprocess.call(padding)



def voiceThread(text, sox_location, o):
	if use == "main":
		voice = ["./assets/voice.exe", "-n", "ScanSoft Daniel_Full_22kHz", "--khz", "48", "-o", "./assets/audio/" + str(o) + ".wav", text]
	else:
		voice = ["./assets/voice.exe", "-n", "Microsoft David Desktop", "--khz", "48", "-o", "./assets/audio/" + str(o) + ".wav", text]
	subprocess.call(voice)

	convert = [sox_location, "--norm", "./assets/audio/" + str(o) + ".wav", "./assets/audio/" + str(o) + "_a.mp3"]
	subprocess.call(convert)

	padding = [sox_location, "--norm", "./assets/audio/" + str(o) + "_a.mp3", "./assets/audio/" + str(o) + ".mp3", "pad", "0", "0.5"]
	subprocess.call(padding)
	print ("                                                     ", end="\r")
	print ("Done: Thread " + str(o), end="\r")

for comment in collection:
	th = threading.Thread(target=voiceThread, args=(collection[comment]["TEXT"], sox_location,collection[comment]["ID"]))
	threadlist.append(th)

for thread in threadlist:
	thread.start()
	time.sleep(0.5)

for thread in threadlist:
	thread.join()


for comment in collection:
	check_length = [sox_location, "--i", "-D", "./assets/audio/" + collection[comment]["ID"] + "_a.mp3"]
	length = subprocess.check_output(check_length)
	collection[comment]["LENGTH"] = length.decode('utf-8')

def downloadComments(link, c):
	wget = ["curl", "--silent", "-o", "temp/" + str(c) + ".html", "-A", "CraWlER bY ToXoo", link]
	subprocess.call(wget)
	print ("                                                     ", end="\r")
	print ("Done: Comment Thread " + str(c), end="\r")

_start = time.time()
c = 0
threadlist = []

for comment in collection:
	th = threading.Thread(target=downloadComments, args=(collection[comment]["LINK"], c))
	threadlist.append(th)
	c = c + 1

for thread in threadlist:
	thread.start()
	time.sleep(1)

for thread in threadlist:
	thread.join()

_end = time.time()
print ('Total Time for Comment Downloading: {}'.format(_end - _start))
print ("Finished downloading Comments. Going to modify.")

for x in collection:
		modifyComment(collection[x]["ID"], dark_mode)

countdown(2)
wget = ["curl", "--silent", "-o", "./assets/temp/title_temp.html", "-A", "CRAwL TooxO", thread_raw]
subprocess.call(wget)
modify("./assets/temp/title_temp.html", "./assets/temp/title.html", dark_mode)

collection = screenshot(collection, "./assets/temp/title.html", chrome_location)
cropAndMove(magick_location, collection, "./assets/temp/title.png")
imageToVideo(ffmpeg_location, collection, lengthlist, dark_mode)
addTheAudio(ffmpeg_location, collection, "./assets/audio/title.mp3", "./assets/video_silent/title.mp4")
renderComplete(ffmpeg_location, collection, shuffle)

addMusicAndOutro(ffmpeg_location, titlefolder)
createDescription(collection, titlefolder, thread_raw, title)

print("CLEANING UP IN 10")
countdown(10)
cleanUP()
