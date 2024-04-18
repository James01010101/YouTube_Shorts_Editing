import os
import time
import multiprocessing as mp

from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips

from Make_Video_Globals import Globals



settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

main_path = "/Users/jamescoldwell/Desktop/YouTube Shorts/Topics/"
quiz_path = f"{main_path}{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/"
audio_path = f"{quiz_path}Audio"


do_in = 0
do_q1 = 0
do_q2 = 0
do_q3 = 0
do_ou = 1


sections_durations = [0, 0, 0, 0, 0]
total_duration = 0

audio_speed = 200


def Create_Audio_File(section, audio_file, text):
    
    # add the speed to the text
    text = f"[[rate {audio_speed}]] {text} [[rate 0]]"
        
    os.system(f"say '{text}' -o '{audio_path}/{section}/{audio_file}.aiff'")
    os.system(f"ffmpeg -i '{audio_path}/{section}/{audio_file}.aiff' '{audio_path}/{section}/{audio_file}.wav' -loglevel error -y")
    
    # delete the aiff file
    os.system(f"rm '{audio_path}/{section}/{audio_file}.aiff'")


# create the joined audio file with all of the parts for this section
def Create_Full_Audio_File(section, clips):
    
    # join all audios together 
    combined_audio = concatenate_audioclips(clips)
    combined_audio.write_audiofile(f"{audio_path}/{section}/{section}_Combined.mp3")
    


def Play_Full_Audio(section):
    #print(f"Playing {section} Audio")
    os.system(f"afplay '{audio_path}/{section}/{section}_Combined.mp3'")
    
    
def Create_Full_Section(section, settings, audio_txt_files):
    print(f"\nMaking {section} Audio")
    
    clips = []
    # create all audios
    for (audio_file, text) in audio_txt_files:
        print(audio_file)
        
        if audio_file == "Answer":
            # then i need to add some stuff to the text first
            text = f"The correct answer, is {settings[text]}"
        else:
            text = settings[text]
            
        Create_Audio_File(section, audio_file, text)
        clips.append(AudioFileClip(f"{audio_path}/{section}/{audio_file}.wav"))
        
    # join all audios together into the full mp3
    Create_Full_Audio_File(section, clips)
    
    
def Do_Question(q):
    section = f"Q{q}"
    q_audio_txt_files = [("Title", f"question_{q}_audio_title_text"),
                            ("Question", f"question_{q}_audio_text"),
                            ("Answer", f"answer_{q}_audio_text")]
    
    Create_Full_Section(section, settings, q_audio_txt_files)
        
    
# this will go through each section and make the audio files if they re true
def Run_Create_Audio_Files():
    started_playing_audio = False
    
    if do_in:
        section = "Intro"
        intro_audio_txt_files = [
            ("Quick", "quick_audio_text"),
            ("How_Well", "how_well_audio_text"),
            ("Topic", "topic_intro_audio_text"),
            ("Prove", "prove_audio_text"),
            ("3_Questions", "three_questions_audio_text"),
            ("X_Seconds", "seconds_audio_text"),
        ]
        
        Create_Full_Section(section, settings, intro_audio_txt_files)
        if not started_playing_audio: # so that only the first section to finish will start playing the audio
            mp.Process(target=Play_All_Audio_Files).start()
            started_playing_audio = True
             

    if do_q1:
        q = 1
        section = f"Q{q}"
        Do_Question(q)
        if not started_playing_audio:
            mp.Process(target=Play_All_Audio_Files).start()
            started_playing_audio = True
        
    if do_q2:
        q = 2
        section = f"Q{q}"
        Do_Question(q)
        if not started_playing_audio:
            mp.Process(target=Play_All_Audio_Files).start()
            started_playing_audio = True
        
    if do_q3:
        q = 3
        section = f"Q{q}"
        Do_Question(q)
        if not started_playing_audio:
            mp.Process(target=Play_All_Audio_Files).start()
            started_playing_audio = True
        

    if do_ou:
        section = "Outro"
        outro_audio_txt_files = [
            ("Thanks", "thanks_audio_text"),
            ("Topic", "topic_outro_audio_text"),
            ("Enjoy", "enjoy_audio_text"),
            ("Comments", "comment_audio_text"),
            ("Subscribe", "subscribe_audio_text"),
        ]
        
        Create_Full_Section(section, settings, outro_audio_txt_files)
        if not started_playing_audio:
            mp.Process(target=Play_All_Audio_Files).start()
            started_playing_audio = True
        
        
    # load in all the full mp3 files for duration
    # this way i always get the total duration of audio even if i dont run all
    print() # for spacing
    all_sections = ["Intro", "Q1", "Q2", "Q3", "Outro"]
    for i in range(len(all_sections)):
        if os.path.exists(f"{audio_path}/{all_sections[i]}/{all_sections[i]}_Combined.mp3"):
            audio = AudioFileClip(f"{audio_path}/{all_sections[i]}/{all_sections[i]}_Combined.mp3")
            sections_durations[i] = round(audio.duration, 2)
            
        else: # if that audio file doesnt exist then 0
            sections_durations[i] = 0
            
        print(f"{all_sections[i]} duration: {sections_durations[i]}")
        
            
        
    total_duration = sum(sections_durations)
    print("\nTotal duration of spoken audio: ", round(total_duration, 2))

    total_duration += (3 * settings['question_silence_duration'])
    print(f"With {settings['question_silence_duration']} second delay for answering questions: ", (3 * settings['question_silence_duration']))

    total_duration += settings['question_end_silence_duration'] * 3 + 1 # +1 for the intro to q1
    print(f"With fade out period of {settings['question_end_silence_duration']} second: ", settings['question_end_silence_duration'] * 3 + 1)

    total_duration += settings['title_to_question_silence'] * 3
    print(f"With all other spaces throughout: ", settings['title_to_question_silence'] * 3)
    
    print("\nTotal duration of video: ", round(total_duration, 2))
        
        

# this will go through and play all audio files 
def Play_All_Audio_Files():
    
    if do_in:
        section = "Intro"
        Play_Full_Audio(section)
        
    if do_q1:
        q = 1
        section = f"Q{q}"
        Play_Full_Audio(section)
        
    if do_q2:
        q = 2
        section = f"Q{q}"
        Play_Full_Audio(section)
        
    if do_q3:
        q = 3
        section = f"Q{q}"
        Play_Full_Audio(section)
        
    if do_ou:
        section = "Outro"
        Play_Full_Audio(section)
    

if __name__ == '__main__':
    Run_Create_Audio_Files()
    
    
            

    
            
            
            
            
            
            