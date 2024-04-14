

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


# run each part Editing in the pygame editor individually from command line
edit_intro:
	clear
	python "Automation/Edit_Intro.py"

edit_q1:
	clear
	python "Automation/Edit_Q1.py"

edit_q2:
	clear
	python "Automation/Edit_Q2.py"

edit_q3:
	clear
	python "Automation/Edit_Q3.py"

edit_outro:
	clear
	python "Automation/Edit_Outro.py"

# go through and edit each section one at a time
edit_all: edit_intro edit_q1 edit_q2 edit_q3 edit_outro




# render each part out individually from command line
render_intro:
	clear
	python "Automation/Render_Intro.py"

render_q1:
	clear
	python "Automation/Render_Q1.py"

render_q2:
	clear
	python "Automation/Render_Q2.py"

render_q3:
	clear
	python "Automation/Render_Q3.py"

render_outro:
	clear
	python "Automation/Render_Outro.py"




# render the final video dont remake any parts
render_final:
	clear
	python "Automation/Render_Final.py"

# render out all individual parts and the final full video
render_all: render_intro render_q1 render_q2 render_q3 render_outro
	python "Automation/Render_Final.py"

# run my test file to test some random code
test:
	clear
	python "Automation/Test.py"


# this will remove all audio files
clean_audio:
	clear
	find Topics -type f -iname '*.wav' -exec rm -f {} +
	find Topics -type f -iname '*.mp3' -exec rm -f {} +
	find Topics -type f -iname '*.aiff' -exec rm -f {} +



