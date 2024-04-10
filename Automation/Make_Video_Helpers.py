from moviepy.editor import *
#import moviepy.video.fx.all as vfx
from moviepy.audio.AudioClip import AudioClip
import time

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