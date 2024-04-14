from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip

import time
import subprocess
from PIL import Image

from Make_Video_Globals import Globals


# helper functions

# save a frame so i can check it without needing to render the whole video
def show_frame(clip, seconds, num):
    """
    Show a frame at time t of a clip
    """
    # Get a frame at the 10-second mark
    frame = clip.get_frame(seconds)

    print(frame.dtype)
    image = Image.fromarray(frame)
    # Save the image
    image.save(f'Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/Finished/video_debug_frame_{num}.jpg', quality=50) # very small just for editing

    return


# Function to generate a silent audio clip of a given duration
def generate_silence(duration=1.0):
    # Create a silent audio clip (the lambda function returns 0 for all "t")
    return AudioClip(lambda t: (0, 0), duration=duration)



# takes in a word, and returns an array where each element adds a word more than the last
# while keeping the same number of newlines
def make_one_word_per_line(raw_text):
    temp_text = ""
    lines = []
    num_nl = 0
    temp_nl = num_nl
    
    words = raw_text.split()
    num_nl = len(words)-1
    temp_nl = num_nl
    
    for i in range(1, len(words)+1):
        temp_nl = num_nl
        temp_text = ""
        for x in range(i):
            if temp_nl > 0:
                temp_text += words[x] + '\n'
                temp_nl -= 1
            else:
                temp_text += words[x]
        
        # add the rest of the nl's
        for y in range(temp_nl):
            temp_text += '\n'
        lines.append(temp_text)
    
    return lines


# take each clip already rendered out and stitch them together into one video file
def render_video():
    filenames = ['intro.mp4', 'q1.mp4', 'q2.mp4', 'q3.mp4', 'outro.mp4']
    output_filename = f'{Globals.topic} Quiz {Globals.quiz_num}_h264.mp4'
    
    # add the correct path to the front
    full_path = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/Finished/"
    
    full_filenames = [full_path + filename for filename in filenames]
    
    # create the temp file list.txt and write the filenames in
    with open('video_file_list.txt', 'w') as file:
        for filename in full_filenames:
            file.write(f"file \'{filename}\'\n")

    # Assemble the full command
    #command = f"ffmpeg -f concat -safe 0 -i video_file_list.txt -c copy '{full_path + output_filename}' -y"
    command = f"ffmpeg -f concat -safe 0 -i video_file_list.txt -c:v libx264 -c:a aac '{full_path + output_filename}' -y"



    # Execute the command
    subprocess.run(command, shell=True)