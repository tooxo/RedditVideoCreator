# RedditVideoCreator

This script uses external (non-foss) programs, which are:
	voice.exe https://www.elifulkerson.com/projects/commandline-text-to-speech.php
	sox	http://sox.sourceforge.net/
	imagemagick https://www.imagemagick.org/
	ffmpeg https://www.ffmpeg.org/
	Daniel Voice Microsoft (in this repo, no official site found maybe https://www.microsoft.com)
	
This Script creates a youtube-ready youtube video from a reddit thread link.

# How to use:

1. Open the folder you just downloaded. (You can simply clone)

2. Modify the configuration.json in the main folder.

```json
	"thread": "<put your thread here (it must end with a /)>"
```

2.5 For now music is provided. It changes, when I code custom music in. :)

3. Run the script

```python
 py script.py
```

4. Videos will be output to the /output/ folder on root

5. Success