from lxml import etree
import lxml.html
import io
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import random

def modify(file, output):
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
	f.write(lxml.html.tostring(dom))	
	f.close()
	os.remove(file)

def lengthSwitch(length):
	length = float(length)
	if length < 10.0:
		return "./assets/prerendered/10white.mp4"
	elif length < 20.0:
		return "./assets/prerendered/20white.mp4"
	elif length < 40.0:
		return "./assets/prerendered/40white.mp4"
	elif length < 60.0:
		return "./assets/prerendered/60white.mp4"
	elif length < 100.0:
		return "./assets/prerendered/100white.mp4"
	elif length < 120.0:
		return "./assets/prerendered/120white.mp4"
	elif length < 180.0:
		return "./assets/prerendered/180white.mp4"
	else:
		return "./assets/prerendered/600white.mp4"
	
def modifyComment(num):
	file = "./temp/" + str(num) + ".html"
	output = "./screenshot/" + str(num) + ".html"
	parser = etree.XMLParser(recover=True)
	f = io.open(output, mode="wb")
	dom = etree.parse(file, parser)
	body = dom.find('body')
	body.attrib['style'] = 'overflow: hidden !important;'
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
	f.write(lxml.html.tostring(dom))
	f.close()
	os.remove(file)
				
def screenshot(list, title):
	print ('Headless')
	_start = time.time()
	options = Options()
	options.add_argument("--headless") # Runs Chrome in headless mode.
	options.add_argument('--no-sandbox') # # Bypass OS security model
	options.add_argument('start-maximized')
	options.add_argument('disable-infobars')
	options.add_argument("--disable-extensions")
	options.add_argument("--log-level=3")
	options.add_argument("--window-size=1920,1080")
	driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver.exe')
	for x in range(0, len(list)):
		driver.get(os.getcwd() + '\\screenshot\\' + str(x) + '.html')
		driver.execute_script("document.body.style.zoom='250%'")
		driver.save_screenshot(os.getcwd() + '\\screenshot\\' + str(x) + '.png')
		print("Done: " + str(x) + " / " + str(len(list)))
	driver.get(os.getcwd() + '\\assets\\temp\\title.html')
	driver.execute_script("document.body.style.zoom='250%'")
	driver.save_screenshot(os.getcwd() + '\\assets\\temp\\title.png')
	driver.quit()
	_end = time.time()
	print ('Total time for headless {}'.format(_end - _start))
	
def cropAndMove(magick, list, title):
	for x in range(0, len(list)):
		crop = [magick, "./screenshot/" + str(x) + ".png", "-resize", "1900x", "-trim", "./assets/images/" + str(x) + ".png"]
		subprocess.call(crop)
		print("Done: " + str(x) + " / " + str(len(list)))
	crop_title = [magick, title, "-trim", "./assets/temp/title_b.png"]
	subprocess.call(crop_title)
	mod = [magick, "./assets/temp/title_b.png", "-bordercolor", "white", "-border", "2%x10%", "./assets/images/title.png"]
	subprocess.call(mod)

	
def imageToVideo(ffmpeg, list, length):
	for x in range(0, len(list)):
		video = lengthSwitch(length[x])
		call = [ffmpeg, "-y", "-i", video, "-i", "./assets/images/" + str(x) + ".png", "-filter_complex", "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2", "-codec:a", "copy", "./assets/video_silent/" + str(x) + ".mp4"]
		subprocess.call(call)
	call = [ffmpeg, "-y", "-i", "./assets/prerendered/40white.mp4", "-i", "./assets/images/title.png", "-filter_complex", "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2", "-codec:a", "copy", "./assets/video_silent/title.mp4"]
	subprocess.call(call)

		
def addTheAudio(ffmpeg, list, audio_title, video_title):
	for x in range(0, len(list)):
		video = "./assets/video_silent/" + str(x) + ".mp4"
		audio = "./assets/audio/" + str(x) + ".mp3"
		combine = [ffmpeg, "-y", "-i", video, "-i", audio, "-shortest", "-c", "copy", "./assets/video/" + str(x) + ".mp4"]
		subprocess.call(combine)
		convert = [ffmpeg, "-y", "-i", "./assets/video/" + str(x) + ".mp4", "-q", "0", "./assets/video/" + str(x) + ".MTS"]
		subprocess.call(convert)
	combine = [ffmpeg, "-y", "-i", video_title, "-i", audio_title, "-shortest", "-c", "copy", "./assets/video/title.mp4"]
	convert = [ffmpeg, "-y", "-i", "./assets/video/title.mp4", "-q", "0", "./assets/video/title.MTS"]
	subprocess.call(combine)
	subprocess.call(convert)

		
def renderComplete(ffmpeg, list):
	f = io.open("./assets/tempfile.txt", mode="w+")
	for x in range(0, len(list)):
		f.write("file " + "video/" + str(x) + ".MTS" + "\n")
		if x != len(list) - 1:
			f.write("file " + "prerendered/censor.MTS" + "\n")
	f.close()
	makeitgreat = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", "./assets/tempfile.txt", "-vcodec", "libx264", "-c", "copy", "./assets/temp/nomusic.MTS"]
	subprocess.call(makeitgreat)
	
def addMusicAndOutro(ffmpeg):
	musicToAdd = "./assets/music/music" + str(random.randrange(7)) + ".mp3"
	addMusic = [ffmpeg, "-y", "-i", "./assets/temp/nomusic.MTS", "-i", musicToAdd, "-c:v", "copy", "-shortest", "-filter_complex", "[0:a]amix[out]", "-map", "0:v", "-map", "[out]", "./assets/temp/audio.MTS"]
	subprocess.call(addMusic)

	f = io.open("./assets/tempfile.txt", mode="w+")
	f.write("file video/title.MTS\n")
	f.write("file temp/audio.MTS\n")
	f.write("file prerendered/outro.MTS\n")
	f.close()
	
	finishup = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", "./assets/tempfile.txt", "-vcodec", "libx264", "-c", "copy", "./output/video.MTS"]
	subprocess.call(finishup)
	
def cleanUP():
	folder_to_clean = ["./temp/", "./screenshot/", "./assets/audio/", "./assets/images/", "./assets/temp/", "./assets/video/", "./assets/video_silent/"]
	for folder in folder_to_clean:
		files_to_delete = os.listdir(folder)
		for file in files_to_delete:
			os.remove(folder + file)