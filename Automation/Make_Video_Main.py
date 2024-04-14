import time
import math
import sys
import os

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip

import Make_Video_Sections as Make_Video_Sections
import Make_Video_Animations
from Make_Video_Globals import Globals
from Make_Video_Helpers import *
import Interactive_Editor

    



if __name__ == '__main__':
    
    # print info about available (color, font)
    print(TextClip.list('font'))
    
    # this file isnt used anymore
    sys.exit(0)
    
    # load in the correct globals file
    settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)
    
    
    use_pygame_editor = True
        
        
    
    
    full_edit_start_time = time.time()
    
    if settings['render_video']:
        # render the video from its parts
        render_video()
        print("Finished Rendering Video Exiting")
        sys.exit(0)
        
        
    
    
    total_editing_time = 0
    final_clips = []
    
    processes = []
    
    if settings['edit_in']:
        
        if use_pygame_editor:
            Interactive_Editor.run_pygame_editor(settings, 'intro')
            
        else:
            start_time = time.time()
            
            saved_parts = {
                'Quick': [[None, None], True],
                'How Well': [[None, None], True],
                'Topic': [[None, None], True],
                '3 Questions': [[None, None], True],
                'Seconds': [[None, None], True],
                'Background': [None, True]
            }
            (intro_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_intro(settings, saved_parts)
            final_clips.append(intro_final_video)
            print(f"Intro Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")
            
    
    if settings['edit_q1']:
        if use_pygame_editor:
            Interactive_Editor.run_pygame_editor(settings, 'q1')
            
        else:
            start_time = time.time()
            
            saved_parts = {
                'Title': [[None, None], True],
                'Question': [[None, None], True],
                'Answer Image': [None, True],
                'Answer': [[None, None], True],
                'Background': [None, True],
                'Timer': [None, True]
            }
            
            (q1_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 1)
            final_clips.append(q1_final_video)
            print(f"Q1 Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")
            
    
    if settings['edit_q2']:
        if use_pygame_editor:
            Interactive_Editor.run_pygame_editor(settings, 'q2')
            
        else:
            start_time = time.time()
            
            saved_parts = {
                'Title': [[None, None], True],
                'Question': [[None, None], True],
                'Answer Image': [None, True],
                'Answer': [[None, None], True],
                'Background': [None, True],
                'Timer': [None, True]
            }
            
            (q2_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 2)
            final_clips.append(q2_final_video)
            print(f"Q2 Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")

    if settings['edit_q3']:
        if use_pygame_editor:
            Interactive_Editor.run_pygame_editor(settings, 'q3')
            
        else:
            start_time = time.time()
            
            saved_parts = {
                'Title': [[None, None], True],
                'Question': [[None, None], True],
                'Answer Image': [None, True],
                'Answer': [[None, None], True],
                'Background': [None, True],
                'Timer': [None, True]
            }
            
            (q3_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 3)
            final_clips.append(q3_final_video)
            print(f"Q3 Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")

    
    if settings['edit_ou']:
        if use_pygame_editor:
            Interactive_Editor.run_pygame_editor(settings, 'outro')
            
        else:
            start_time = time.time()
            
            saved_parts = {
                'Thanks': [[None, None], True],
                'Topic': [[None, None], True],
                'Subscribe': [[None, None], True],
                'Subscribe Box': [None, True],
                'Comment': [[None, None], True],
                'Background': [None, True]
            }
            
            (outro_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_outro(settings, saved_parts)
            final_clips.append(outro_final_video)
            print(f"Outro Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")
    
    
    full_edit_end_time = time.time()
    print("Total Time:", round(full_edit_end_time - full_edit_start_time, 2), " seconds")
        
    if not settings['render_video']:
        sys.exit(0)

        
        
        
    # print out total frames
    running_frames = 0
    if settings['edit_in']:
        print("Intro Frames: ", running_frames, "->", round(running_frames + intro_final_video.duration * 60))
        running_frames = round(running_frames + intro_final_video.duration * 60)
    
    if settings['edit_q1']:
        print("Q1 Frames:    ", running_frames, "->", round(running_frames + q1_final_video.duration * 60))
        running_frames = round(running_frames + q1_final_video.duration * 60)
    
    if settings['edit_q2']:
        print("Q2 Frames:    ", running_frames, "->", round(running_frames + q2_final_video.duration * 60))
        running_frames = round(running_frames + q2_final_video.duration * 60)
    
    if settings['edit_q3']:
        print("Q3 Frames:    ", running_frames, "->", round(running_frames + q3_final_video.duration * 60))
        running_frames = round(running_frames + q3_final_video.duration * 60)
    
    if settings['edit_ou'] :
        print("Outro Frames: ", running_frames, "->", round(running_frames + outro_final_video.duration * 60))
        running_frames = round(running_frames + outro_final_video.duration * 60)
        
    print(f"Output Video will be {round(running_frames/60, 2)} seconds long\n\n")
        
    
    # join all intro questions and outro together
    if settings['render_video']:
        final_video = concatenate_videoclips(final_clips, method="chain")
        
        start_time = time.time()
        final_video.write_videofile(
                                filename=f"Topics/{settings['topic']}/{settings['topic']} Quiz {settings['quiz_num']}/Finished/{settings['topic']} Quiz {settings['quiz_num']}.mp4", 
                                fps=settings['fps'],  # Frame rate
                                codec="libx264",  # Video codec (h264) or 'mpeg4' could also work
                                audio=True, # Do not include audio
                                audio_codec="aac",  # Audio codec
                                audio_bitrate="192k",  # Audio bitrate
                                preset="placebo",  # Compression (ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow, placebo)
                                threads=8,  # Number of threads for processing (None for auto)
                                ffmpeg_params=[],  # Additional FFmpeg parameters: CRF for quality
                                logger="bar"
                            )
        end_time = time.time()
        
        print("Total Rendered Frames: ", round(final_video.duration * 60))
        
        total_time = round(end_time - start_time)
        total_minutes = math.floor(total_time / 60)
        total_seconds = total_time - (total_minutes * 60)
        print(f"Final Render took: {total_minutes}:{total_seconds} seconds")



