

# runs my ffmpeg command to render the final video from all of its sections
#from pygame import image, display, event, quit

import subprocess
from Make_Video_Globals import Globals

if __name__ == "__main__":
    filenames = ['intro.mp4', 'q1.mp4', 'q2.mp4', 'q3.mp4', 'outro.mp4']
    output_filename = f'{Globals.topic} Quiz {Globals.quiz_num}.mp4'
    
    # add the correct path to the front
    full_path = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/Finished/"
    
    full_filenames = [full_path + filename for filename in filenames]
    
    # create the temp file list.txt and write the filenames in
    with open('video_file_list.txt', 'w') as file:
        for filename in full_filenames:
            file.write(f"file \'{filename}\'\n")

    # Assemble the full command
    #command = f"ffmpeg -f concat -safe 0 -i video_file_list.txt -c copy '{full_path + output_filename}' -y"
    
    # rencode with libx264 so it will compress way more
    command = f"ffmpeg -f concat -safe 0 -i video_file_list.txt -c:v libx264 -c:a copy '{full_path + output_filename}' -y"
    
    # rencode with toolbox so it will compress (does compress but not as much as libx264)
    #command = f"ffmpeg -f concat -safe 0 -i video_file_list.txt -c:v h264_videotoolbox -c:a copy '{full_path + output_filename}' -y"

    # Execute the command
    subprocess.run(command, shell=True)
    