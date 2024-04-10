import os
from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips
# this will go through all folders and make and play the audio files

from Make_Video_Globals import Globals

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)


main_path = "/Users/jamescoldwell/Desktop/YouTube Shorts/Topics/"
quiz_path = f"{main_path}{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/"


do_in = 1
do_q1 = 1
do_q2 = 1
do_q3 = 1
do_ou = 1

sections_durations = [0, 0, 0, 0, 0]
total_duration = 0



if do_in:
    print("Making Intro Audio")
    # go through all files in the script folder and for each do something
    intro_audio_files = ["Quick" ,"How_Well", "Topic", "Prove", "3_Questions", "X_Seconds"]
    section = "Intro"
    for file in intro_audio_files:
        print(file)
        file = file.split('.')[0]
        
        os.system(f"grep -v '^#' '{quiz_path}Audio/{section}/Script/{file}.txt' | say -o '{quiz_path}Audio/temp.aiff'")
        os.system(f"ffmpeg -i '{quiz_path}/Audio/temp.aiff' '{quiz_path}/Audio/{section}/Wav/{file}.wav' -loglevel error -y")
        
    # join all audios together 
    clips = []
    for i in range(len(intro_audio_files)):
        clips.append(AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{intro_audio_files[i]}.wav"))
    
    combined_audio = concatenate_audioclips(clips)
    
    combined_audio.write_audiofile(f"{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3")
        
    print("Playing Intro Audio")
    os.system(f"afplay '{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3'")
    
    # get the duration of the mp3 audio clip
    for i in range(len(intro_audio_files)):
        sections_durations[0] += clips[i].duration
    sections_durations[0] = round(sections_durations[0], 2)
        
        
    print("Intro Duration: ", sections_durations[0])
    
    print() # for spacing
        

if do_q1:
    print("Making Q1 Audio")
    # go through all files in the script folder and for each do something
    q1_audio_files = ["Title" ,"Question", "Answer"]
    section = "Q1"
    for file in q1_audio_files:
        print(file)
        file = file.split('.')[0]
        
        os.system(f"grep -v '^#' '{quiz_path}Audio/{section}/Script/{file}.txt' | say -o '{quiz_path}Audio/temp.aiff'")
        os.system(f"ffmpeg -i '{quiz_path}/Audio/temp.aiff' '{quiz_path}/Audio/{section}/Wav/{file}.wav' -loglevel error -y")
        
    # join all audios together 
    a1 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[0]}.wav")
    a2 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[1]}.wav")
    a3 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[2]}.wav")
    
    combined_audio = concatenate_audioclips([a1, a2, a3])
    
    combined_audio.write_audiofile(f"{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3")
        
    print("Playing Q1 Audio")
    os.system(f"afplay '{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3'")
    
    sections_durations[1] = round(a1.duration + a2.duration + a3.duration, 2)
    print("Q1 Duration: ", sections_durations[1])
    
    print() # for spacing
    
    
if do_q2:
    print("Making Q2 Audio")
    # go through all files in the script folder and for each do something
    q1_audio_files = ["Title" ,"Question", "Answer"]
    section = "Q2"
    for file in q1_audio_files:
        print(file)
        file = file.split('.')[0]
        
        os.system(f"grep -v '^#' '{quiz_path}Audio/{section}/Script/{file}.txt' | say -o '{quiz_path}Audio/temp.aiff'")
        os.system(f"ffmpeg -i '{quiz_path}/Audio/temp.aiff' '{quiz_path}/Audio/{section}/Wav/{file}.wav' -loglevel error -y")
        
    # join all audios together 
    a1 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[0]}.wav")
    a2 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[1]}.wav")
    a3 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[2]}.wav")
    
    combined_audio = concatenate_audioclips([a1, a2, a3])
    
    combined_audio.write_audiofile(f"{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3")
        
    print("Playing Q2 Audio")
    os.system(f"afplay '{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3'")
    
    sections_durations[2] = round(a1.duration + a2.duration + a3.duration, 2)
    print("Q2 Duration: ", sections_durations[2])
    
    print() # for spacing
    

if do_q3:
    print("Making Q3 Audio")
    # go through all files in the script folder and for each do something
    q1_audio_files = ["Title" ,"Question", "Answer"]
    section = "Q3"
    for file in q1_audio_files:
        print(file)
        file = file.split('.')[0]
        
        os.system(f"grep -v '^#' '{quiz_path}Audio/{section}/Script/{file}.txt' | say -o '{quiz_path}Audio/temp.aiff'")
        os.system(f"ffmpeg -i '{quiz_path}/Audio/temp.aiff' '{quiz_path}/Audio/{section}/Wav/{file}.wav' -loglevel error -y")
        
    # join all audios together 
    a1 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[0]}.wav")
    a2 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[1]}.wav")
    a3 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{q1_audio_files[2]}.wav")
    
    combined_audio = concatenate_audioclips([a1, a2, a3])
    
    combined_audio.write_audiofile(f"{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3")
        
    print("Playing Q3 Audio")
    os.system(f"afplay '{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3'")
    
    sections_durations[3] = round(a1.duration + a2.duration + a3.duration, 2)
    print("Q3 Duration: ", sections_durations[3])
    
    print() # for spacing
    
    
if do_ou:
    print("Making Outro Audio")
    # go through all files in the script folder and for each do something
    outro_audio_files = ["Thanks" ,"Topic", "Enjoy", "Comments", "Subscribe"]
    section = "Outro"
    for file in outro_audio_files:
        print(file)
        file = file.split('.')[0]
        
        os.system(f"grep -v '^#' '{quiz_path}Audio/{section}/Script/{file}.txt' | say -o '{quiz_path}Audio/temp.aiff'")
        os.system(f"ffmpeg -i '{quiz_path}/Audio/temp.aiff' '{quiz_path}/Audio/{section}/Wav/{file}.wav' -loglevel error -y")
        
    # join all audios together 
    a1 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{outro_audio_files[0]}.wav")
    a2 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{outro_audio_files[1]}.wav")
    a3 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{outro_audio_files[2]}.wav")
    a4 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{outro_audio_files[3]}.wav")
    a5 = AudioFileClip(f"{quiz_path}Audio/{section}/Wav/{outro_audio_files[4]}.wav")
    
    combined_audio = concatenate_audioclips([a1, a2, a3, a4, a5])
    
    combined_audio.write_audiofile(f"{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3")
        
    print("Playing Outro Audio")
    os.system(f"afplay '{quiz_path}Audio/{section}/Wav/{section}_Combined.mp3'")
    
    sections_durations[4] = round(a1.duration + a2.duration + a3.duration + a4.duration + a5.duration, 2)
    print("Outro Duration: ", sections_durations[4])
    
    print() # for spacing
        

total_duration = sum(sections_durations)
print("Total duration of audio: ", round(total_duration, 2))

total_duration += (3 * settings['question_silence_duration'])
print(f"With {settings['question_silence_duration']} second delay for answering questions: ", round(total_duration, 2))

total_duration += settings['question_end_silence_duration'] * 3 + 1 # +1 for the intro to q1
print(f"With fade out period of {settings['question_end_silence_duration']} second: ", round(total_duration, 2))

total_duration += settings['title_to_question_silence'] * 3
print(f"With all other spaces throughout: ", round(total_duration, 2))
        
        
        
        
        
        