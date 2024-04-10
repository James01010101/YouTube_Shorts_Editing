

# use [[slnc 1000]] so pause for 1 seecond

# help https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/FineTuning/FineTuning.html

# '#' are now comments out lines so they won't be read, this is using grep to remove lines starting with #

newfolder:
	clear
	python "Automation/New_Folder.py"

scripts:
	clear
	python "Automation/Make_Scripts.py"

audio:
	clear
	python "Automation/Make_Audio.py"

video:
	clear
	python "Automation/Make_Video_Main.py"



# run my test file to test some random code
test:
	clear
	python "Automation/Test.py"


# this will remove all audio files
cleanaudio:
	clear
	find Topics -type f -iname '*.wav' -exec rm -f {} +
	find Topics -type f -iname '*.mp3' -exec rm -f {} +
	find Topics -type f -iname '*.aiff' -exec rm -f {} +



