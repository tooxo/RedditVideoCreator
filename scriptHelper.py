from lxml import etree
import lxml.html
import io
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import random

def modify(file, output, dark_mode):
	print ("File: " + file + " Output: " + output)
	parser = etree.XMLParser(recover=True)
	f = io.open(output, mode="wb")
	dom = etree.parse(file, parser)
	body = dom.find('body')
	body.attrib['style'] = 'overflow: hidden !important;'
	divs = dom.findall('.//div')
	scripts = dom.findall('.//script')
	for div in divs:
		if div.get('class'):
			if "Post" in div.get('class'):
				test = div
		if div.get('id'):
			if "2x-container" == div.get('id'):
				big = div
	for script in scripts:
		if script.get('src'):
			if "runtime" in script.get('src'):
				script.getparent().remove(script)
	for child in big:
		child.getparent().remove(child)
	big.append(test)
	if dark_mode == "true":
		styles = etree.Element('style')
		styles.text = '[id="2x-container"]{ background: #1A1A1B; color: #B3B5B7 !important} h2,i,span,a {color: #B3B5B7 !important} .Post {transition: none !important; -webkit-transition: none !important}'
		body.append(styles)
	f.write(lxml.html.tostring(dom))	
	f.close()
	os.remove(file)

def lengthSwitch(length, dark_mode):
	if dark_mode == "true":
		mode = "dark"
	else: 
		mode = "white"

	length = float(length)
	if length < 10.0:
		return "./assets/prerendered/10" + mode + ".mp4"
	elif length < 20.0:
		return "./assets/prerendered/20" + mode + ".mp4"
	elif length < 40.0:
		return "./assets/prerendered/40" + mode + ".mp4"
	elif length < 60.0:
		return "./assets/prerendered/60" + mode + ".mp4"
	elif length < 100.0:
		return "./assets/prerendered/100" + mode + ".mp4"
	elif length < 120.0:
		return "./assets/prerendered/120" + mode + ".mp4"
	elif length < 180.0:
		return "./assets/prerendered/180" + mode + ".mp4"
	else:
		return "./assets/prerendered/600" + mode + ".mp4"
	
def modifyComment(num, dark_mode):
	file = "./temp/" + str(num) + ".html"
	output = "./screenshot/" + str(num) + ".html"
	parser = etree.XMLParser(recover=True)
	f = io.open(output, mode="wb")
	dom = etree.parse(file, parser)
	body = dom.find('body')
	body.attrib['style'] = 'overflow-x: hidden !important; min-height: 0 !important'
	divs = dom.findall('.//div')
	scripts = dom.findall('.//script')
	for div in divs:
		if div.get("class"):
			if "top-level" in div.get("class"):
				test = div
				test.attrib['style'] = "margin-top: 0 !important; margin-left: 0 !important;"
		if div.get("id"):
			if "2x-container" == div.get("id"):
				big = div
	for script in scripts:
		if script.get('src'):
			if "runtime" in script.get('src'):
				script.getparent().remove(script)
	for child in big:
		child.getparent().remove(child)
	big.append(test)
	if dark_mode == "true":
		styles = etree.Element('style')
		styles.text = '.top-level {background: #1A1A1B;} span,h1,h2,a,p{color: #B3B5B7 !important} .Comment {transition: none !important; -webkit-transition: none !important; border-radius: 0 !important}'
		body.append(styles)
	f.write(lxml.html.tostring(dom))
	f.close()
	os.remove(file)

def screenshot(list, title, chrome_driver):	
	chrome = chrome_driver.replace('/', '\\')
	_start = time.time()
	options = Options()
	options.add_argument("--headless") 
	options.add_argument('--no-sandbox') 
	options.add_argument('start-maximized')
	options.add_argument('disable-infobars')
	options.add_argument("--disable-extensions")
	options.add_argument("--log-level=3")
	options.add_argument("--window-size=2560,1440")
	driver = webdriver.Chrome(chrome_options=options, executable_path=chrome)
	removelist = []
	for comment in list:
		driver.get(os.getcwd() + '\\screenshot\\' + list[comment]["ID"] + '.html')
		driver.execute_script("document.body.style.zoom='350%'")
		if driver.execute_script("return document.documentElement.clientWidth") == 2560:
			driver.save_screenshot(os.getcwd() + '\\screenshot\\' + list[comment]["ID"] + '.png')
			print("Done: " + list[comment]["ID"] + " / " + str(len(list)))
		else:
			removelist.append(comment)
	driver.get(os.getcwd() + '\\assets\\temp\\title.html')
	driver.execute_script("document.body.style.zoom='350%'")
	driver.save_screenshot(os.getcwd() + '\\assets\\temp\\title.png')
	driver.quit()
	
	for i in removelist:
		del list[i]
	_end = time.time()
	print ('Total time for Screenshot. {}'.format(_end - _start))
	return list
	
def cropAndMove(magick, list, title):
	for comment in list:
		crop = [magick, "./screenshot/" + list[comment]["ID"] + ".png", "-resize", "1900x", "-bordercolor", "white", "-border", "1x1", "-trim", "+repage", "-gravity", "South", "-chop", "x1+0+0", "+repage", "./assets/images/" + list[comment]["ID"] + ".png"]
		subprocess.call(crop)
		print("Done: " + list[comment]["ID"] + " / " + str(len(list)))
	mod = [magick, title, "-resize", "1900x", "-bordercolor", "white", "-border", "1x1", "-trim", "+repage", "-gravity", "South", "-chop", "x1+0+0", "+repage", "./assets/images/title.png"]
	subprocess.call(mod)

	
def imageToVideo(ffmpeg, list, length, dark_mode):
	for comment in list:
		video = lengthSwitch(list[comment]["LENGTH"], dark_mode)
		call = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", video, "-i", "./assets/images/" + list[comment]["ID"] + ".png", "-filter_complex", "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2", "-codec:a", "copy", "./assets/video_silent/" + list[comment]["ID"] + ".mp4"]
		subprocess.call(call)
	if dark_mode == "true":
		mode = "dark"
	else:
		mode = "white"
	call = [ffmpeg,  "-v", "quiet", "-stats", "-y", "-i", "./assets/prerendered/40" + mode + ".mp4", "-i", "./assets/images/title.png", "-filter_complex", "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2", "-codec:a", "copy", "./assets/video_silent/title.mp4"]
	subprocess.call(call)

		
def addTheAudio(ffmpeg, list, audio_title, video_title):
	for comment in list:
		video = "./assets/video_silent/" + list[comment]["ID"] + ".mp4"
		audio = "./assets/audio/" + list[comment]["ID"] + ".mp3"
		combine = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", video, "-i", audio, "-shortest", "-c", "copy", "./assets/video/" + list[comment]["ID"] + ".mp4"]
		subprocess.call(combine)
		convert = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", "./assets/video/" + list[comment]["ID"] + ".mp4", "-q", "0", "./assets/video/" + list[comment]["ID"] + ".MTS"]
		subprocess.call(convert)
	combine = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", video_title, "-i", audio_title, "-shortest", "-c", "copy", "./assets/video/title.mp4"]
	subprocess.call(combine)
	convert = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", "./assets/video/title.mp4", "-q", "0", "./assets/video/title.MTS"]
	subprocess.call(convert)

def stringTitle(string):
	result = ''.join([i for i in string if (i.isalnum() or i == " ")])
	return result
		
def renderComplete(ffmpeg, list, isshuffle):
	f = io.open("./assets/tempfile.txt", mode="w+")
	if isshuffle == "true":
		t = []
		for x in list:
			t.append(x)
		random.shuffle(t)
		for b in t:
			f.write("file " + "video/" + str(b) + ".MTS" + "\n")
			f.write("file " + "prerendered/censor.MTS" + "\n")
	else:
		for comment in list:
			f.write("file " + "video/" + list[comment]["ID"] + ".MTS\n")
			f.write("file " + "prerendered/censor.MTS" + "\n")
	
	f.close()
	makeitgreat = [ffmpeg, "-v", "quiet", "-stats", "-y", "-f", "concat", "-safe", "0", "-i", "./assets/tempfile.txt", "-vcodec", "libx264", "-c", "copy", "./assets/temp/nomusic.MTS"]
	subprocess.call(makeitgreat)
	
def createDescription(list, folder, threadlink, title):
	f = io.open("./output/" + folder + "/description.txt", "w+")
	
	f.write(title + "\n\n")
	f.write("im a bot beep boop, crazy, right?\n")
	f.write("this video is part of a proof of concept channel for the script that creates this videos fully automatic. check it out here: https://github.com/tooxo/RedditVideoCreator\n")
	f.write("\n\n")
	f.write("Links to original posts: \n")
	f.write("Original Thread: " + threadlink + "\n")
	f.write("\n")
	f.write("Comments by: \n")
	for comment in list:
		f.write(list[comment]["AUTHOR"] + "\n")
	f.close()
		
		
def addMusicAndOutro(ffmpeg, folder):
	musicToAdd = "./assets/music/music" + str(random.randrange(7)) + ".mp3"
	addMusic = [ffmpeg, "-v", "quiet", "-stats", "-y", "-i", "./assets/temp/nomusic.MTS", "-i", musicToAdd, "-b:v", "4M", "-shortest", "-filter_complex", "[0:a]amix[out]", "-map", "0:v", "-map", "[out]", "./assets/temp/audio.MTS"]
	subprocess.call(addMusic)

	f = io.open("./assets/tempfile.txt", mode="w+")
	f.write("file video/title.MTS\n")
	f.write("file temp/audio.MTS\n")
	if os.path.isfile("./assets/prerendered/outro.MTS"):
		f.write("file prerendered/outro.MTS\n")
	f.close()
	
	#Creating Thumbnail
	thumb = [ffmpeg, "-v", "quiet", "-stats", "-i", "./assets/video/title.MTS", "-vf", 'select=eq(n\,0)', "-vframes", "1", "./output/" + folder + "/thumbnail.png"]
	subprocess.call(thumb)
	
	finishup = [ffmpeg, "-v", "quiet", "-stats", "-y", "-f", "concat", "-safe", "0", "-i", "./assets/tempfile.txt", "-vcodec", "libx264", "-c", "copy", "./output/" + folder + "/" + "video.MTS"]
	subprocess.call(finishup)
	
def cleanUP():
	folder_to_clean = ["./temp/", "./screenshot/", "./assets/audio/", "./assets/images/", "./assets/temp/", "./assets/video/", "./assets/video_silent/"]
	for folder in folder_to_clean:
		files_to_delete = os.listdir(folder)
		for file in files_to_delete:
			if ".git" not in file:
				os.remove(folder + file)