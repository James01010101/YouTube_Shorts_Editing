from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip
from moviepy.video.tools.drawing import circle


import Make_Video_Animations as Animations
import Make_Video_Helpers as Helpers

import time
import numpy as np
import math
import textwrap


from proglog import ProgressBarLogger
class MyBarLogger(ProgressBarLogger):
    
    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print ('Parameter %s is now %s' % (parameter, value))
    
    def bars_callback(self, bar, attr, value,old_value=None):
        # Every time the logger progress is updated, this function is called        
        percentage = (value / self.bars[bar]['total']) * 100
        print(bar, attr, value)
        
        
        
        
        
# main make intro function
def make_intro(settings, saved_parts):
    
    intro_start_time = time.time()
    
    quiz_path = f"Topics/{settings['topic']}/{settings['topic']} Quiz {settings['quiz_num']}/"
    
    # load in all audio
    audio_quick = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/Quick.wav")
    audio_how_well = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/How_Well.wav")
    audio_topic = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/Topic.wav")
    audio_prove = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/Prove.wav")
    audio_3_questions = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/3_Questions.wav")
    audio_x_seconds = AudioFileClip(f"{quiz_path}Audio/Intro/Wav/X_Seconds.wav")
    
    # put together the audio
    intro_audio = concatenate_audioclips(
        [audio_quick,
         audio_how_well, 
         audio_topic,
         audio_prove,
         audio_3_questions, 
         audio_x_seconds,
         Helpers.generate_silence(1.0) ])
    
    intro_audio_duration_total = intro_audio.duration
    
    print_audio_times = False
    if print_audio_times:
        running_time = 0
        print("Intro Audio Durations:")
        # quickly print the length of each clip and how long it is
        print("Quick:    ", audio_quick.duration, "(", round(running_time, 2), ")")
        running_time += audio_quick.duration
        print("How Well: ", audio_how_well.duration, "(", round(running_time, 2), ")")
        running_time += audio_how_well.duration
        print("Topic:    ", audio_topic.duration, "(", round(running_time, 2), ")")
        running_time += audio_topic.duration
        print("Prove:    ", audio_prove.duration, "(", round(running_time, 2), ")")
        running_time += audio_prove.duration
        print("3 Quests: ", audio_3_questions.duration, "(", round(running_time, 2), ")")
        running_time += audio_3_questions.duration
        print("X Secs:   ", audio_x_seconds.duration, "(", round(running_time, 2), ")")
        running_time += audio_x_seconds.duration
        print("Silence:  ", "1.00", "(", round(running_time, 2), ")")
        print("Total:    ", round(intro_audio_duration_total, 2))
    
    print("Editing Video Intro")
    
    
    
    
    # Quick Text
    # intro animation
    if saved_parts['Quick'][0] is None or saved_parts['Quick'][1] == True:
        quick_start_time = time.time()
        intro_quick_text = ( TextClip(settings['quick_raw_text'], fontsize=settings['quick_font_size'], 
                                    font=settings['font_title'], 
                                    color=settings['quick_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['quick_kerning'])
                            .set_start(0)
                            .set_duration(intro_audio_duration_total))
        
        width, height = intro_quick_text.size
        intro_quick_text = intro_quick_text.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_quick.duration, 1, intro_audio_duration_total, width, height, settings['quick_pop_in_overshoot']))
        intro_quick_text = intro_quick_text.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_quick.duration, 1, intro_audio_duration_total, width, height, settings['screen_size'], settings['quick_position'][0], settings['quick_position'][1], settings['quick_pop_in_overshoot']))
            
        
        
        
        intro_quick_text_black_border = ( TextClip(settings['quick_raw_text'], fontsize=settings['quick_font_size'], 
                                                font=settings['font_title'], 
                                                color=settings['text_border_colour'], 
                                                size=settings['screen_size'], 
                                                kerning=settings['quick_kerning'], 
                                                stroke_width=settings['text_border_width'], 
                                                stroke_color=settings['text_border_colour'])
                                        .set_start(0)
                                        .set_duration(intro_audio_duration_total))
        
        width, height = intro_quick_text_black_border.size
        intro_quick_text_black_border = intro_quick_text_black_border.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_quick.duration, 1, intro_audio_duration_total, width, height, settings['quick_pop_in_overshoot']))
        intro_quick_text_black_border = intro_quick_text_black_border.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_quick.duration, 1, intro_audio_duration_total, width, height, settings['screen_size'], settings['quick_position'][0], settings['quick_position'][1], settings['quick_pop_in_overshoot']))
        
        intro_quick_text_combined = CompositeVideoClip([intro_quick_text_black_border, intro_quick_text], size=settings['screen_size'])
        intro_quick_text_combined = intro_quick_text_combined.crossfadeout(1)
        
        # update parts
        saved_parts['Quick'][0] = intro_quick_text_combined
        saved_parts['Quick'][1] = False
        quick_end_time = time.time()
        print(f"Text Time - Quick: {round(quick_end_time - quick_start_time, 2)}")
    
    
    
    
    
    # How well do you know text
    if saved_parts['How Well'][0] is None or saved_parts['How Well'][1] == True:
        how_well_start_time = time.time()
        
        full_text = settings['how_well_raw_text']
        char_duration = audio_how_well.duration / len(full_text)
        clips = []
        border_clips = []
        if not settings['testing']:
            for i in range(1, len(full_text) + 1):
                if i <= 11:
                    new_text = full_text[:i] + '\n'
                else:
                    new_text = full_text[:i]
                    
                new_clip = TextClip(new_text, 
                                    fontsize=settings['how_well_font_size'], 
                                    font=settings['font_general_text'], 
                                    color=settings['how_well_colour'],
                                    size=settings['screen_size'], 
                                    kerning=settings['how_well_kerning'], 
                                    interline=settings['how_well_interline'])
                new_clip = new_clip.set_duration(char_duration)
                clips.append(new_clip)
                
                # black boarder
                new_clip = TextClip(new_text, 
                                    fontsize=settings['how_well_font_size'], 
                                    font=settings['font_general_text'], 
                                    color=settings['text_border_colour'],
                                    size=settings['screen_size'], 
                                    kerning=settings['how_well_kerning'], 
                                    interline=settings['how_well_interline'], 
                                    stroke_width=settings['text_border_width'], 
                                    stroke_color=settings['text_border_colour'])
                new_clip = new_clip.set_duration(char_duration)
                border_clips.append(new_clip)
            
            
        # finally add a new clip which just lasts the entire rest of the intro
        new_clip = TextClip(full_text, 
                            fontsize=settings['how_well_font_size'], 
                            font=settings['font_general_text'], 
                            color=settings['how_well_colour'],
                            size=settings['screen_size'], 
                            kerning=settings['how_well_kerning'], 
                            interline=settings['how_well_interline'])
        new_clip = new_clip.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration))
        clips.append(new_clip)
        
        # black boarder
        new_clip_border = TextClip(full_text, 
                            fontsize=settings['how_well_font_size'], 
                            font=settings['font_general_text'], 
                            color=settings['text_border_colour'],
                            size=settings['screen_size'], 
                            kerning=settings['how_well_kerning'], 
                            interline=settings['how_well_interline'], 
                            stroke_width=settings['text_border_width'], 
                            stroke_color=settings['text_border_colour'])
        new_clip_border = new_clip_border.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration))
        border_clips.append(new_clip_border)
            
        # set the duration of the last clips to last (and one clip length)
        intro_how_well_text = concatenate_videoclips(clips, method="chain")    
        intro_how_well_text_black_border = concatenate_videoclips(border_clips, method="chain")
        
        intro_how_well_text_combined = ( CompositeVideoClip([intro_how_well_text_black_border, intro_how_well_text], size=settings['screen_size'])
                                        .set_position(settings['how_well_position'])
                                        .crossfadeout(1) )
        
        # to keep things alligned for debug image if testing
        if settings['testing']:
            intro_how_well_text_combined = intro_how_well_text_combined.set_start(audio_quick.duration + audio_how_well.duration)
        else:
            intro_how_well_text_combined = intro_how_well_text_combined.set_start(audio_quick.duration)
            
        saved_parts['How Well'][0] = intro_how_well_text_combined
        saved_parts['How Well'][1] = False
        
        how_well_end_time = time.time()
        print(f"Text Time - How Well: {round(how_well_end_time - how_well_start_time, 2)}")
    
    
    
    
    # Topic TITLE text
    if saved_parts['Topic'][0] is None or saved_parts['Topic'][1] == True:
        topic_start_time = time.time()    
        normal_clips = []
        border_clips = []
        
        
        
        if settings['topic_intro_one_word_per_line']:
            text_lines = Helpers.make_one_word_per_line(settings['full_topic'])
            
            
            for i in range(0, len(text_lines)):
                normal_clip = ( TextClip(text_lines[i], 
                                    fontsize=settings['topic_intro_font_size'], 
                                    font=settings['font_topic'], 
                                    color=settings['topic_intro_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['topic_intro_kerning'], 
                                    interline=settings['topic_intro_interline'],))
                
                border_clip = ( TextClip(text_lines[i], 
                                        fontsize=settings['topic_intro_font_size'], 
                                        font=settings['font_topic'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['topic_intro_kerning'], 
                                        interline=settings['topic_intro_interline'], 
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']))
                
                # check for last and make it last the rest of the time needed
                if i == len(text_lines)-1:
                    border_clip = border_clip.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration + ((len(text_lines)-1) * (audio_topic.duration/len(text_lines)))))
                    normal_clip = normal_clip.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration + ((len(text_lines)-1) * (audio_topic.duration/len(text_lines)))))
                else:
                    border_clip = border_clip.set_duration(audio_topic.duration/len(text_lines))
                    normal_clip = normal_clip.set_duration(audio_topic.duration/len(text_lines))
                
                normal_clips.append(normal_clip)
                border_clips.append(border_clip)
                
        else: # not doing one word per line
            # split topic into words
            words = settings['full_topic'].split(' ')
            temp_text = ''
            for i in range(0, len(words)):
                if i == len(words)-1:
                    temp_text += words[i]
                else: # if not last add a space
                    temp_text += words[i] + ' '
                    
                normal_clip = ( TextClip(temp_text, 
                                fontsize=settings['topic_intro_font_size'], 
                                font=settings['font_topic'], 
                                color=settings['topic_intro_colour'], 
                                size=settings['screen_size'], 
                                kerning=settings['topic_intro_kerning'], 
                                interline=settings['topic_intro_interline'],))
            
                border_clip = ( TextClip(temp_text, 
                                    fontsize=settings['topic_intro_font_size'], 
                                    font=settings['font_topic'], 
                                    color=settings['text_border_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['topic_intro_kerning'], 
                                    interline=settings['topic_intro_interline'], 
                                    stroke_width=settings['text_border_width'], 
                                    stroke_color=settings['text_border_colour']))
                
                if i == len(words)-1: # then its the last letter so it needs to last the rest
                    border_clip = border_clip.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration + ((len(words)-1) * (audio_topic.duration/len(words)))))
                    normal_clip = normal_clip.set_duration(intro_audio_duration_total - (audio_quick.duration + audio_how_well.duration + ((len(words)-1) * (audio_topic.duration/len(words)))))
                else: #else normal
                    border_clip = border_clip.set_duration(audio_topic.duration/len(words))
                    normal_clip = normal_clip.set_duration(audio_topic.duration/len(words))
            
                normal_clips.append(normal_clip)
                border_clips.append(border_clip)
                
            
            
        # add the last one which lasts
        
        # join then all
        intro_topic_text = concatenate_videoclips(normal_clips, method="chain")
        intro_topic_text_border = concatenate_videoclips(border_clips, method="chain")
        
        intro_topic_text_combined = ( CompositeVideoClip([intro_topic_text_border, intro_topic_text], size=settings['screen_size'])
                                        .set_start(audio_quick.duration + audio_how_well.duration)
                                        .set_position(settings['topic_intro_position'])
                                        .crossfadeout(1) )
        
        saved_parts['Topic'][0] = intro_topic_text_combined
        saved_parts['Topic'][1] = False
        
        topic_end_time = time.time()
        print(f"Text Time - Topic: {round(topic_end_time - topic_start_time, 2)}")
    
    
    
    # 3 Questions Text
    if saved_parts['3 Questions'][0] is None or saved_parts['3 Questions'][1] == True:
        three_questions_start_time = time.time()
        three_questions_audio_start = audio_quick.duration + audio_how_well.duration + audio_topic.duration + audio_prove.duration
        intro_three_questions_text = ( TextClip(settings['three_questions_raw_text'], 
                                                fontsize=settings['three_questions_font_size'], 
                                                font=settings['font_general_text'], 
                                                color=settings['three_questions_colour'], 
                                                size=settings['screen_size'], 
                                                kerning=settings['three_questions_kerning']) )
            
        intro_three_questions_text_border = ( TextClip(settings['three_questions_raw_text'], 
                                                        fontsize=settings['three_questions_font_size'], 
                                                        font=settings['font_general_text'], 
                                                        color=settings['text_border_colour'], 
                                                        size=settings['screen_size'], 
                                                        kerning=settings['three_questions_kerning'], 
                                                        stroke_width=settings['text_border_width'], 
                                                        stroke_color=settings['text_border_colour']) )
        
        three_questions_duration = intro_audio_duration_total - three_questions_audio_start
        intro_three_questions_text_combined = ( CompositeVideoClip([intro_three_questions_text_border, intro_three_questions_text], size=settings['screen_size'])
                                            .set_duration(three_questions_duration)
                                            .set_start(three_questions_audio_start)
                                            .crossfadein(settings['three_questions_anim_in_time'])
                                            .crossfadeout(settings['three_questions_anim_out_time'])
                                            )
            
        # returns the new x position of the text and keeps the y the same
        intro_three_questions_text_combined = intro_three_questions_text_combined.set_position(lambda t: (
                                                Animations.slide_in_slide_out(t, 
                                                                            audio_3_questions.duration, 
                                                                            settings['three_questions_anim_out_time'],
                                                                            three_questions_duration, 
                                                                            settings['three_questions_position'][0], 
                                                                            settings['three_questions_anim_overshoot'], 
                                                                            settings['three_questions_anim_right_move']),
                                                settings['three_questions_position'][1])) 
        
        saved_parts['3 Questions'][0] = intro_three_questions_text_combined
        saved_parts['3 Questions'][1] = False
        
        three_questions_end_time = time.time()
        print(f"Text Time - 3 Questions: {round(three_questions_end_time - three_questions_start_time, 2)}")
    
    
    
    # 5 seconds text
    if saved_parts['Seconds'][0] is None or saved_parts['Seconds'][1] == True:
        seconds_start_time = time.time()
        seconds_audio_start = audio_quick.duration + audio_how_well.duration + audio_topic.duration + audio_prove.duration + audio_3_questions.duration
        intro_seconds_text = ( TextClip(settings['seconds_raw_text'], 
                                        fontsize=settings['seconds_font_size'], 
                                        font=settings['font_general_text'], 
                                        color=settings['seconds_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['seconds_kerning']) )
            
        intro_seconds_text_border = ( TextClip(settings['seconds_raw_text'], 
                                                        fontsize=settings['seconds_font_size'], 
                                                        font=settings['font_general_text'], 
                                                        color=settings['text_border_colour'], 
                                                        size=settings['screen_size'], 
                                                        kerning=settings['seconds_kerning'], 
                                                        stroke_width=settings['text_border_width'], 
                                                        stroke_color=settings['text_border_colour']) )
                        
        intro_seconds_duration = intro_audio_duration_total - seconds_audio_start
        intro_seconds_text_combined = ( CompositeVideoClip([intro_seconds_text_border, intro_seconds_text], size=settings['screen_size'])
                                        .set_start(seconds_audio_start)
                                        .set_duration(intro_seconds_duration)
                                        .crossfadein(settings['seconds_anim_in_time'])
                                        .crossfadeout(settings['seconds_anim_out_time'])
                                        )
        
        
        # returns the new x position of the text and keeps the y the same
        intro_seconds_text_combined = intro_seconds_text_combined.set_position(lambda t: (
                                                Animations.slide_in_slide_out(t, 
                                                                            audio_x_seconds.duration, 
                                                                            settings['seconds_anim_out_time'],
                                                                            intro_seconds_duration, 
                                                                            settings['seconds_position'][0], 
                                                                            settings['seconds_anim_overshoot'], 
                                                                            settings['seconds_anim_right_move']),
                                                settings['seconds_position'][1])) 
        
        saved_parts['Seconds'][0] = intro_seconds_text_combined
        saved_parts['Seconds'][1] = False
        
        seconds_end_time = time.time()
        print(f"Text Time - 5 Seconds: {round(seconds_end_time - seconds_start_time, 2)}")
        
    


    # background image
    if saved_parts['Background'][0] is None or saved_parts['Background'][1] == True:
        background_start_time = time.time()
        background_image = ( ImageClip(settings['background_image_path'])
                            .set_duration(intro_audio_duration_total) # how many seconds the clip lasts for 
                            .set_position(settings['background_position'])) 
        
        if settings['use_background_width']:
            background_image = background_image.resize(width=settings['background_size'])
        else: # use height instead
            background_image = background_image.resize(height=settings['background_size'])
            
        saved_parts['Background'][0] = background_image
        saved_parts['Background'][1] = False
        
        background_end_time = time.time()
        print(f"Background Time: {round(background_end_time - background_start_time, 2)}")
    
    
    # this will overlay the text on the background
    intro_video_combined = CompositeVideoClip([saved_parts['Background'][0], 
                                               saved_parts['Quick'][0], 
                                               saved_parts['How Well'][0],
                                               saved_parts['Topic'][0],
                                               saved_parts['3 Questions'][0],
                                               saved_parts['Seconds'][0]], 
                                                size=settings['screen_size'])
    
    intro_video_audio_combined = intro_video_combined.set_audio(intro_audio)
    
    
    Helpers.show_frame(intro_video_combined, intro_audio_duration_total - 1, 0)
    
    intro_end_time = time.time()
    

    # short video for testing
    if settings['render_in']:
        #intro_video_audio_combined = intro_video_audio_combined.subclip( 
                                        #intro_audio.duration - 1.25,
                                        #intro_audio.duration)
        
        print("Intro Starting Render, Edit Took: ", round(intro_end_time - intro_start_time, 2), " seconds")
        
        start_time = time.time()
        intro_video_audio_combined.write_videofile(
                                filename=f"{quiz_path}Finished/intro.mp4", 
                                fps=settings['fps'],  # Frame rate
                                codec="libx264",  # Video codec (h264) or 'mpeg4' could also work
                                audio=True, # Do not include audio
                                audio_codec="aac",  # Audio codec
                                audio_bitrate="192k",  # Audio bitrate
                                preset="medium",  # Compression (ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow, placebo)
                                threads=8,  # Number of threads for processing (None for auto)
                                ffmpeg_params=[],  # Additional FFmpeg parameters: CRF for quality lossless => ['-qp', '0']
                                logger="bar"
                            )
        end_time = time.time()
        total_time = round(end_time - start_time)
        total_minutes = math.floor(total_time / 60)
        total_seconds = total_time - (total_minutes * 60)
        print(f"Intro Render took: {total_minutes}:{total_seconds} seconds")
    
    
    #return intro_video_audio_combined
    return (intro_video_audio_combined, intro_audio_duration_total - 1, saved_parts)



# main make intro function
def make_questions(settings, saved_parts, question_num):
    
    q_start_time = time.time()
    
    quiz_path = f"Topics/{settings['topic']}/{settings['topic']} Quiz {settings['quiz_num']}/"
    
    # load in all audio
    audio_title = AudioFileClip(f"{quiz_path}Audio/Q{question_num}/Wav/Title.wav")
    audio_question = AudioFileClip(f"{quiz_path}Audio/Q{question_num}/Wav/Question.wav")
    audio_answer = AudioFileClip(f"{quiz_path}Audio/Q{question_num}/Wav/Answer.wav")
    
    # put together the audio
    audio_combined = concatenate_audioclips(
        [audio_title,
         Helpers.generate_silence(settings['title_to_question_silence']),
         audio_question, 
         Helpers.generate_silence(settings['question_silence_duration']),
         audio_answer,
         Helpers.generate_silence(settings['question_end_silence_duration'])])
    
    audio_duration_total = round(audio_combined.duration, 2)
    
    print_audio_times = False
    if print_audio_times:
        running_time = 0
        print(f"Q{question_num} Audio Durations:")
        # quickly print the length of each clip and how long it is
        print("Title:     ", audio_title.duration, "(", round(running_time, 2), ")")
        running_time += audio_title.duration
        print("Pause:     ", format(settings['title_to_question_silence'], ".2f"), "(", round(running_time, 2), ")")
        running_time += settings['title_to_question_silence']
        print("Question:  ", audio_question.duration, "(", round(running_time, 2), ")")
        running_time += audio_question.duration
        print("Pause:     ", format(settings['question_silence_duration'], ".2f"), "(", round(running_time, 2), ")")
        running_time += settings['question_silence_duration']
        print("Answer:    ", audio_answer.duration, "(", round(running_time, 2), ")")
        running_time += audio_answer.duration
        print("End Pause: ", format(settings['question_end_silence_duration'], '.2f'), "(", round(running_time, 2), ")")
        running_time += settings['question_end_silence_duration']
        print("Total:     ", round(audio_duration_total, 2))
    
    print(f"Editing Video Q{question_num}")
    
    
    
    # Title Text
    # intro animation
    if saved_parts['Title'][0] is None or saved_parts['Title'][1] == True:
        title_start_time = time.time()
        title_text = ( TextClip(f"{settings['question_raw_text']} {question_num}", 
                                fontsize=settings['question_title_font_size'], 
                                font=settings['font_title'], 
                                color=settings['question_title_colour'], 
                                size=settings['screen_size'], 
                                kerning=settings['question_title_kerning']) )
        
        width, height = title_text.size
        title_text = title_text.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_title.duration, 1, audio_duration_total, width, height, settings['question_title_pop_in_overshoot']))
        title_text = title_text.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_title.duration, 1, audio_duration_total, width, height, settings['screen_size'], settings['question_title_position'][0], settings['question_title_position'][1], settings['question_title_pop_in_overshoot']))
            
            
        
        title_text_border = ( TextClip(f"{settings['question_raw_text']} {question_num}", 
                                        fontsize=settings['question_title_font_size'], 
                                        font=settings['font_title'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['question_title_kerning'], 
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']) )
                        
        
        width, height = title_text_border.size
        title_text_border = title_text_border.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_title.duration, 1, audio_duration_total, width, height, settings['question_title_pop_in_overshoot']))
        title_text_border = title_text_border.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_title.duration, 1, audio_duration_total, width, height, settings['screen_size'], settings['question_title_position'][0], settings['question_title_position'][1], settings['question_title_pop_in_overshoot']))
            
        title_text_combined = ( CompositeVideoClip([title_text_border, title_text], size=settings['screen_size'])
                                .set_start(0)
                                .set_duration(audio_duration_total)
                                .crossfadeout(1) )
        
        saved_parts['Title'][0] = title_text_combined
        saved_parts['Title'][1] = False
        
        title_end_time = time.time()
        print(f"Text Time - Title: {round(title_end_time - title_start_time, 2)}")
    
    
    
    
    # question text
    if saved_parts['Question'][0] is None or saved_parts['Question'][1] == True:
        question_text_start_time = time.time()
        
        if question_num == 1:
            question_raw_text = settings['question_1_raw_text']
            question_font_size = settings['question_1_font_size']
            question_position = settings['question_1_position']
            timer_position = settings['question_1_timer_position']
            interline = settings['question_1_text_interline']
            question_wrap_width = settings['question_1_text_wrap_width']
        elif question_num == 2:
            question_raw_text = settings['question_2_raw_text']
            question_font_size = settings['question_2_font_size']
            question_position = settings['question_2_position']
            timer_position = settings['question_2_timer_position']
            interline = settings['question_2_text_interline']
            question_wrap_width = settings['question_2_text_wrap_width']
        elif question_num == 3:
            question_raw_text = settings['question_3_raw_text']
            question_font_size = settings['question_3_font_size']
            question_position = settings['question_3_position']
            timer_position = settings['question_3_timer_position']
            interline = settings['question_3_text_interline']
            question_wrap_width = settings['question_3_text_wrap_width']
        
        # wrap the text around
        question_raw_text = textwrap.fill(question_raw_text, question_wrap_width)
        
            
        char_duration = audio_question.duration / len(question_raw_text)
        # find all the \n's
        new_lines_indexes = []
        for i in range(0, len(question_raw_text)):
            if question_raw_text[i] == '\n':
                new_lines_indexes.append(i)
        
                
        clips = []
        border_clips = []
        if not settings['testing']:
            for i in range(1, len(question_raw_text) + 1):
                # add new lines if needed so text stays in the same place
                new_text = question_raw_text[:i]
                for nl_index in new_lines_indexes:
                    if i <= nl_index:
                        new_text = new_text + '\n'
                        
                    
                new_clip = TextClip(new_text, 
                                    fontsize=question_font_size, 
                                    font=settings['font_general_text'], 
                                    color=settings['question_text_colour'],
                                    size=settings['screen_size'], 
                                    kerning=settings['question_text_kerning'], 
                                    interline=interline)
                new_clip = new_clip.set_duration(char_duration)
                clips.append(new_clip)
                
                # black boarder
                new_clip = TextClip(new_text, 
                                    fontsize=question_font_size, 
                                    font=settings['font_general_text'], 
                                    color=settings['text_border_colour'],
                                    size=settings['screen_size'], 
                                    kerning=settings['question_text_kerning'], 
                                    interline=interline, 
                                    stroke_width=settings['text_border_width'], 
                                    stroke_color=settings['text_border_colour'])
                new_clip = new_clip.set_duration(char_duration)
                border_clips.append(new_clip)
            
        # finally add a new clip which just lasts the entire rest of the intro
        new_clip = TextClip(question_raw_text, 
                            fontsize=question_font_size, 
                            font=settings['font_general_text'], 
                            color=settings['question_text_colour'],
                            size=settings['screen_size'], 
                            kerning=settings['question_text_kerning'], 
                            interline=interline)
        new_clip = new_clip.set_duration(audio_duration_total - (audio_title.duration + settings['title_to_question_silence'] + audio_question.duration))
        clips.append(new_clip)
        
        # black boarder
        new_clip = TextClip(question_raw_text, 
                            fontsize=question_font_size, 
                            font=settings['font_general_text'], 
                            color=settings['question_text_colour'],
                            size=settings['screen_size'], 
                            kerning=settings['question_text_kerning'], 
                            interline=interline, 
                            stroke_width=settings['text_border_width'], 
                            stroke_color=settings['text_border_colour'])
        new_clip = new_clip.set_duration(audio_duration_total - (audio_title.duration + settings['title_to_question_silence'] + audio_question.duration))
        border_clips.append(new_clip)
            
        # set the duration of the last clips to last (and one clip length)
        question_text = concatenate_videoclips(clips, method="chain")
        
        question_text_border = concatenate_videoclips(border_clips, method="chain")
                                
        
        question_text_combined = ( CompositeVideoClip([question_text_border, question_text], size=settings['screen_size'])
                                    .set_position(question_position)
                                    .crossfadeout(1) )
        
        # so if im testing everything still lines up (otherwise question comes in right, but goes out too early)
        if settings['testing']:
            question_text_combined = question_text_combined.set_start(audio_title.duration + settings['title_to_question_silence'] + audio_question.duration)
        else:
            question_text_combined = question_text_combined.set_start(audio_title.duration + settings['title_to_question_silence'])
        
        saved_parts['Question'][0] = question_text_combined
        saved_parts['Question'][1] = False
        
        question_text_end_time = time.time()
        print(f"Text Time - Question: {round(question_text_end_time - question_text_start_time, 2)}")
        
        
    # load in the timer
    if saved_parts['Timer'][0] is None or saved_parts['Timer'][1] == True:
        timer_start_time = time.time()
        timer = ( VideoFileClip(settings['timer_path'], has_mask=True)
                .set_position(timer_position)
                .set_start(audio_title.duration + settings['title_to_question_silence'] + audio_question.duration))
        
        saved_parts['Timer'][0] = timer
        saved_parts['Timer'][1] = False
            
        timer_end_time = time.time()
        print(f"Text Time - Timer: {round(timer_end_time - timer_start_time, 2)}")
    
    
    
    
    # answer text
    if saved_parts['Answer'][0] is None or saved_parts['Answer'][1] == True:
        answer_start_time = time.time()
        
        answer_audio_start = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
        
        if question_num == 1:
            answer_raw_text = settings['answer_1_raw_text']
            answer_font_size = settings['answer_1_font_size']
            answer_position = settings['answer_1_position']
            answer_wrap_width = settings['answer_1_text_wrap_width']
        elif question_num == 2:
            answer_raw_text = settings['answer_2_raw_text']
            answer_font_size = settings['answer_2_font_size']
            answer_position = settings['answer_2_position']
            answer_wrap_width = settings['answer_2_text_wrap_width']
        elif question_num == 3:
            answer_raw_text = settings['answer_3_raw_text']
            answer_font_size = settings['answer_3_font_size']
            answer_position = settings['answer_3_position']
            answer_wrap_width = settings['answer_3_text_wrap_width']
            
        answer_raw_text = textwrap.fill(answer_raw_text, answer_wrap_width)
            
        answer_text = ( TextClip(answer_raw_text, 
                                    fontsize=answer_font_size, 
                                    font=settings['font_general_text'], 
                                    color=settings['answer_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['answer_kerning'],
                                    interline=settings['answer_interline']) )
            
        answer_text_border = ( TextClip(answer_raw_text, 
                                        fontsize=answer_font_size, 
                                        font=settings['font_general_text'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['answer_kerning'], 
                                        interline=settings['answer_interline'],
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']) )
                        
        
        answer_text_combined = ( CompositeVideoClip([answer_text_border, answer_text], size=settings['screen_size'])
                                .set_start(answer_audio_start) 
                                .set_duration(audio_duration_total - answer_audio_start)
                                .crossfadein(0.5)
                                .crossfadeout(settings['answer_anim_out_time']) )
        
        answer_text_combined = answer_text_combined.set_position(lambda t: (
                                Animations.slide_in_slide_out(  t, 
                                                                -1, 
                                                                settings['answer_anim_out_time'],
                                                                audio_duration_total - answer_audio_start, 
                                                                answer_position[0], 
                                                                settings['answer_anim_overshoot'], 
                                                                settings['answer_anim_right_move']),
                                                                answer_position[1]) )
                                                                                                
        
        saved_parts['Answer'][0] = answer_text_combined
        saved_parts['Answer'][1] = False
        
        answer_end_time = time.time()
        print(f"Text Time - Answer: {round(answer_end_time - answer_start_time, 2)}")
    
    
    # load in the answer image
    if saved_parts['Answer Image'][0] is None or saved_parts['Answer Image'][1] == True:
        answer_image_start_time = time.time()
        if question_num == 1:
            
            # if using answer image for both answer and helper i dont need fade in middle
            if settings['question_1_image_use_answer_for_both']:
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_1_image_answer_path']) 
                            .resize(width=settings['question_1_image_answer_width'])
                            .set_position(settings['question_1_image_answer_position'])
                            .set_start(audio_title.duration + settings['title_to_question_silence'])
                            .set_duration(audio_duration_total - (audio_title.duration + settings['title_to_question_silence']))
                            .crossfadein(audio_question.duration)
                            .crossfadeout(1)
                            )
                
            
            # else if im using a helper which is different from answer
            elif settings['question_1_image_use_helper']:
                
                # start at start of question text 
                helper_start_time = audio_title.duration + settings['title_to_question_silence']
                
                # load in helper image
                helper_image = ( ImageClip(settings['question_1_image_helper_path']) 
                            .resize(width=settings['question_1_image_helper_width'])
                            .set_position(settings['question_1_image_helper_position'])
                            .set_start(helper_start_time)
                            .set_duration(audio_question.duration + settings['question_silence_duration'] + min(1, audio_answer.duration))
                            .crossfadein(min(1, audio_question.duration))
                            .crossfadeout(min(1, audio_answer.duration))
                            )
                
                
                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_1_image_answer_path']) 
                            .resize(width=settings['question_1_image_answer_width'])
                            .set_position(settings['question_1_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
                
                # combine and answer and helper images into the clip
                answer_image = CompositeVideoClip([answer_image, helper_image], size=settings['screen_size'])
                
            
            # just use the answer image not helper
            else:

                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_1_image_answer_path']) 
                            .resize(width=settings['question_1_image_answer_width'])
                            .set_position(settings['question_1_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
            
        elif question_num == 2:
            # if using answer image for both answer and helper i dont need fade in middle
            if settings['question_2_image_use_answer_for_both']:
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_2_image_answer_path']) 
                            .resize(width=settings['question_2_image_answer_width'])
                            .set_position(settings['question_2_image_answer_position'])
                            .set_start(audio_title.duration + settings['title_to_question_silence'])
                            .set_duration(audio_duration_total - (audio_title.duration + settings['title_to_question_silence']))
                            .crossfadein(audio_question.duration)
                            .crossfadeout(1)
                            )
                
            
            # else if im using a helper which is different from answer
            elif settings['question_2_image_use_helper']:
                
                # start at start of question text 
                helper_start_time = audio_title.duration + settings['title_to_question_silence']
                
                # load in helper image
                helper_image = ( ImageClip(settings['question_2_image_helper_path']) 
                            .resize(width=settings['question_2_image_helper_width'])
                            .set_position(settings['question_2_image_helper_position'])
                            .set_start(helper_start_time)
                            .set_duration(audio_question.duration + settings['question_silence_duration'] + min(1, audio_answer.duration))
                            .crossfadein(min(1, audio_question.duration))
                            .crossfadeout(min(1, audio_answer.duration))
                            )
                
                
                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_2_image_answer_path']) 
                            .resize(width=settings['question_2_image_answer_width'])
                            .set_position(settings['question_2_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
                
                # combine and answer and helper images into the clip
                answer_image = CompositeVideoClip([answer_image, helper_image], size=settings['screen_size'])
                
            
            # just use the answer image not helper
            else:

                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_2_image_answer_path']) 
                            .resize(width=settings['question_2_image_answer_width'])
                            .set_position(settings['question_2_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
            
        elif question_num == 3:
            # if using answer image for both answer and helper i dont need fade in middle
            if settings['question_3_image_use_answer_for_both']:
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_3_image_answer_path']) 
                            .resize(width=settings['question_3_image_answer_width'])
                            .set_position(settings['question_3_image_answer_position'])
                            .set_start(audio_title.duration + settings['title_to_question_silence'])
                            .set_duration(audio_duration_total - (audio_title.duration + settings['title_to_question_silence']))
                            .crossfadein(audio_question.duration)
                            .crossfadeout(1)
                            )
                
            
            # else if im using a helper which is different from answer
            elif settings['question_3_image_use_helper']:
                
                # start at start of question text 
                helper_start_time = audio_title.duration + settings['title_to_question_silence']
                
                # load in helper image
                helper_image = ( ImageClip(settings['question_3_image_helper_path']) 
                            .resize(width=settings['question_3_image_helper_width'])
                            .set_position(settings['question_3_image_helper_position'])
                            .set_start(helper_start_time)
                            .set_duration(audio_question.duration + settings['question_silence_duration'] + min(1, audio_answer.duration))
                            .crossfadein(min(1, audio_question.duration))
                            .crossfadeout(min(1, audio_answer.duration))
                            )
                
                
                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_3_image_answer_path']) 
                            .resize(width=settings['question_3_image_answer_width'])
                            .set_position(settings['question_3_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
                
                # combine and answer and helper images into the clip
                answer_image = CompositeVideoClip([answer_image, helper_image], size=settings['screen_size'])
                
            
            # just use the answer image not helper
            else:

                # start at start of question text 
                image_start_time = audio_title.duration + settings['title_to_question_silence'] + audio_question.duration + settings['question_silence_duration']
                
                # load in answer image
                answer_image = ( ImageClip(settings['question_3_image_answer_path']) 
                            .resize(width=settings['question_3_image_answer_width'])
                            .set_position(settings['question_3_image_answer_position'])
                            .set_start(image_start_time)
                            .set_duration(audio_duration_total - image_start_time)
                            .crossfadein(min(1, audio_answer.duration))
                            .crossfadeout(1)
                            )
                
        saved_parts['Answer Image'][0] = answer_image
        saved_parts['Answer Image'][1] = False
        
        answer_image_end_time = time.time()
        print(f"Text Time - Answer Image: {round(answer_image_end_time - answer_image_start_time, 2)}")
    
    
    
    

    # background image
    if saved_parts['Background'][0] is None or saved_parts['Background'][1] == True:
        background_start_time = time.time()
        background_image = ( ImageClip(settings['background_image_path'])
                            .set_duration(audio_duration_total) # how many seconds the clip lasts for 
                            .set_position(settings['background_position']))
        
        if settings['use_background_width']:
            background_image = background_image.resize(width=settings['background_size'])
        else: # use height instead
            background_image = background_image.resize(height=settings['background_size'])
                            
        saved_parts['Background'][0] = background_image
        saved_parts['Background'][1] = False
        
        background_end_time = time.time()
        print(f"Background Time: {round(background_end_time - background_start_time, 2)}")
    
    
    # this will overlay the text on the background
    video_combined = CompositeVideoClip([saved_parts['Background'][0], 
                                            saved_parts['Answer Image'][0],
                                            saved_parts['Title'][0],
                                            saved_parts['Question'][0],
                                            saved_parts['Timer'][0],
                                            saved_parts['Answer'][0]], 
                                                size=settings['screen_size'])
    video_audio_combined = video_combined.set_audio(audio_combined)
    
    
    # debug frame with everything in it
    if settings['use_timer_frame']:
        # timer frame
        debug_frame_time = audio_duration_total - settings['question_end_silence_duration'] - audio_answer.duration - 2
    else:
        # regular answer frame
        debug_frame_time = audio_duration_total - 1
        
    Helpers.show_frame(video_combined, debug_frame_time, question_num)
    
    q_end_time = time.time()
    
    
    if question_num == 1 and settings['render_q1']:
        render_question = True
    elif question_num == 2 and settings['render_q2']:
        render_question = True
    elif question_num == 3 and settings['render_q3']:
        render_question = True
    else:
        render_question = False
        
    # short video for testing
    if render_question:
        #video_audio_combined = video_audio_combined.subclip(3.2)
        
        print(f"Q{question_num}    Starting Render, Edit Took: ", round(q_end_time - q_start_time, 2), " seconds")
        
        
        start_time = time.time()
        logger = MyBarLogger()
        video_audio_combined.write_videofile(
                                filename=f"{quiz_path}Finished/q{question_num}.mp4", 
                                fps=settings['fps'],  # Frame rate
                                codec="libx264",  # Video codec (h264) or 'mpeg4' could also work
                                audio=True, # Do not include audio
                                audio_codec="aac",  # Audio codec
                                audio_bitrate="192k",  # Audio bitrate
                                preset="medium",  # Compression (ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow, placebo)
                                threads=8,  # Number of threads for processing (None for auto)
                                ffmpeg_params=[],  # Additional FFmpeg parameters: CRF for quality
                                logger="bar"
                            )
        end_time = time.time()
        total_time = round(end_time - start_time)
        total_minutes = math.floor(total_time / 60)
        total_seconds = total_time - (total_minutes * 60)
        print(f"Q{question_num} Render took: {total_minutes}:{total_seconds} seconds")
    
    return (video_audio_combined, debug_frame_time, saved_parts)




     
# main make outro function
def make_outro(settings, saved_parts):
    
    outro_start_time = time.time()
    
    quiz_path = f"Topics/{settings['topic']}/{settings['topic']} Quiz {settings['quiz_num']}/"
    
    # load in all audio
    audio_thanks = AudioFileClip(f"{quiz_path}Audio/Outro/Wav/Thanks.wav")
    audio_topic = AudioFileClip(f"{quiz_path}Audio/Outro/Wav/Topic.wav")
    audio_enjoy = AudioFileClip(f"{quiz_path}Audio/Outro/Wav/Enjoy.wav")
    audio_comment = AudioFileClip(f"{quiz_path}Audio/Outro/Wav/Comments.wav")
    audio_subscribe = AudioFileClip(f"{quiz_path}Audio/Outro/Wav/Subscribe.wav")
    
    # put together the audio
    outro_audio = concatenate_audioclips(
        [audio_thanks,
         audio_topic,
         audio_enjoy,
         audio_comment,
         audio_subscribe])
    
    outro_audio_duration_total = outro_audio.duration
    
    print_audio_times = False
    if print_audio_times: 
        running_time = 0
        print("Outro Audio Durations:")
        # quickly print the length of each clip and how long it is
        print("Thanks:    ", audio_thanks.duration, "(", round(running_time, 2), ")")
        running_time += audio_thanks.duration
        print("Topic:     ", audio_topic.duration, "(", round(running_time, 2), ")")
        running_time += audio_topic.duration
        print("Enjoy:     ", audio_enjoy.duration, "(", round(running_time, 2), ")")
        running_time += audio_enjoy.duration
        print("Comments:  ", audio_comment.duration, "(", round(running_time, 2), ")")
        running_time += audio_comment.duration
        print("Subscribe: ", audio_subscribe.duration, "(", round(running_time, 2), ")")
        running_time += audio_subscribe.duration
        print("Total:     ", round(outro_audio_duration_total, 2))
        
    print("Editing Video Outro")
    
    
    
    # Thanks for playing Text
    # outro animation
    if saved_parts['Thanks'][0] is None or saved_parts['Thanks'][1] == True:
        thanks_start_time = time.time()
        thanks_text = ( TextClip(settings['thanks_raw_text'], 
                                    fontsize=settings['thanks_font_size'], 
                                    font=settings['font_general_text'], 
                                    color=settings['thanks_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['thanks_kerning'], 
                                    interline=settings['thanks_interline']) )
        
        width, height = thanks_text.size
        thanks_text = thanks_text.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_thanks.duration, -1, outro_audio_duration_total, width, height, settings['thanks_pop_in_overshoot']))
        thanks_text = thanks_text.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_thanks.duration, -1, outro_audio_duration_total, width, height, settings['screen_size'], settings['thanks_text_position'][0], settings['thanks_text_position'][1], settings['thanks_pop_in_overshoot']))

        thanks_text_border = ( TextClip(settings['thanks_raw_text'], 
                                        fontsize=settings['thanks_font_size'], 
                                        font=settings['font_general_text'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['thanks_kerning'], 
                                        interline=settings['thanks_interline'], 
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']) )
        
        width, height = thanks_text_border.size
        thanks_text_border = thanks_text_border.resize(
            lambda t: Animations.pop_in_pop_out_size(t, audio_thanks.duration, -1, outro_audio_duration_total, width, height, settings['thanks_pop_in_overshoot']))
        thanks_text_border = thanks_text_border.set_position(
            lambda t: Animations.pop_in_pop_out_position(t, audio_thanks.duration, -1, outro_audio_duration_total, width, height, settings['screen_size'], settings['thanks_text_position'][0], settings['thanks_text_position'][1], settings['thanks_pop_in_overshoot']))
        
        thanks_text_combined = ( CompositeVideoClip([thanks_text_border, thanks_text], size=settings['screen_size'])
                                    .set_duration(outro_audio_duration_total) )
        
        saved_parts['Thanks'][0] = thanks_text_combined
        saved_parts['Thanks'][1] = False
        
        thanks_end_time = time.time()
        print(f"Text Time - Thanks: {round(thanks_end_time - thanks_start_time, 2)}")
    
    
    
    # Topic TITLE text
    if saved_parts['Topic'][0] is None or saved_parts['Topic'][1] == True:
        topic_start_time = time.time()    
        normal_clips = []
        border_clips = []
        
        if settings['topic_outro_one_word_per_line']:
            text_lines = Helpers.make_one_word_per_line(settings['full_topic'])
            for i in range(0, len(text_lines)):
                normal_clip = ( TextClip(text_lines[i], 
                                    fontsize=settings['topic_outro_font_size'], 
                                    font=settings['font_topic'], 
                                    color=settings['topic_outro_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['topic_outro_kerning'], 
                                    interline=settings['topic_outro_interline']) )
                
                border_clip = ( TextClip(text_lines[i], 
                                        fontsize=settings['topic_outro_font_size'],
                                        font=settings['font_topic'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['topic_outro_kerning'], 
                                        interline=settings['topic_outro_interline'], 
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']) )
                
                # check for last and make it last the rest of the time needed
                if i == len(text_lines)-1:
                    border_clip = border_clip.set_duration(outro_audio_duration_total - (audio_thanks.duration + ((len(text_lines)-1) * (audio_topic.duration/len(text_lines)))))
                    normal_clip = normal_clip.set_duration(outro_audio_duration_total - (audio_thanks.duration + ((len(text_lines)-1) * (audio_topic.duration/len(text_lines)))))
                else:
                    border_clip = border_clip.set_duration(audio_topic.duration/len(text_lines))
                    normal_clip = normal_clip.set_duration(audio_topic.duration/len(text_lines))
                
                normal_clips.append(normal_clip)
                border_clips.append(border_clip)
            
        else:
            # split topic into words
            words = settings['full_topic'].split(' ')
            temp_text = ''
            for i in range(0, len(words)):
                if i == len(words)-1:
                    temp_text += words[i]
                else: # if not last add a space
                    temp_text += words[i] + ' '
                    
                normal_clip = ( TextClip(temp_text, 
                                    fontsize=settings['topic_outro_font_size'], 
                                    font=settings['font_topic'], 
                                    color=settings['topic_outro_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['topic_outro_kerning'], 
                                    interline=settings['topic_outro_interline']) )
                
                border_clip = ( TextClip(temp_text, 
                                        fontsize=settings['topic_outro_font_size'],
                                        font=settings['font_topic'], 
                                        color=settings['text_border_colour'], 
                                        size=settings['screen_size'], 
                                        kerning=settings['topic_outro_kerning'], 
                                        interline=settings['topic_outro_interline'], 
                                        stroke_width=settings['text_border_width'], 
                                        stroke_color=settings['text_border_colour']) )
                
                if i == len(words)-1:
                    border_clip = border_clip.set_duration(outro_audio_duration_total - (audio_thanks.duration + ((len(words)-1) * (audio_topic.duration/len(words)))))
                    normal_clip = normal_clip.set_duration(outro_audio_duration_total - (audio_thanks.duration + ((len(words)-1) * (audio_topic.duration/len(words)))))
                else:
                    border_clip = border_clip.set_duration(audio_topic.duration/len(words))
                    normal_clip = normal_clip.set_duration(audio_topic.duration/len(words))
            
                normal_clips.append(normal_clip)
                border_clips.append(border_clip)
            
        # add the last one which lasts
        
        # join then all
        outro_topic_text = concatenate_videoclips(normal_clips, method="chain")
        outro_topic_text_border = concatenate_videoclips(border_clips, method="chain")
        
        outro_topic_text_combined = ( CompositeVideoClip([outro_topic_text_border, outro_topic_text], size=settings['screen_size'])
                                        .set_start(audio_thanks.duration)
                                        .set_position(settings['topic_outro_position']))
        
        saved_parts['Topic'][0] = outro_topic_text_combined
        saved_parts['Topic'][1] = False
        
        topic_end_time = time.time()
        print(f"Text Time - Topic: {round(topic_end_time - topic_start_time, 2)}")
    
    
    
    
    # Subscribe text
    if saved_parts['Subscribe'][0] is None or saved_parts['Subscribe'][1] == True:
        subscribe_start_time = time.time()
        subscribe_audio_start = audio_thanks.duration + audio_topic.duration + audio_comment.duration  + audio_enjoy.duration
        subscribe_text = ( TextClip(settings['subscribe_raw_text'], 
                                    fontsize=settings['subscribe_font_size'], 
                                    font=settings['font_general_text'], 
                                    color=settings['subscribe_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['subscribe_kerning']) )
            
        subscribe_text_border = ( TextClip(settings['subscribe_raw_text'], 
                                            fontsize=settings['subscribe_font_size'], 
                                            font=settings['font_general_text'], 
                                            color=settings['text_border_colour'], 
                                            size=settings['screen_size'], 
                                            kerning=settings['subscribe_kerning'], 
                                            stroke_width=settings['text_border_width'], 
                                            stroke_color=settings['text_border_colour']) )

        subscribe_text_combined = ( CompositeVideoClip([subscribe_text_border, subscribe_text], size=settings['screen_size'])
                                    .set_start(subscribe_audio_start)
                                    .set_duration(outro_audio_duration_total - subscribe_audio_start)
                                    .crossfadein(1)
                                    .set_position(settings['subscribe_text_position']) )
        
        saved_parts['Subscribe'][0] = subscribe_text_combined
        saved_parts['Subscribe'][1] = False
        
        subscribe_end_time = time.time()
        print(f"Text Time - Subscribe: {round(subscribe_end_time - subscribe_start_time, 2)}")
    
    
    # subscribe red background
    if saved_parts['Subscribe Box'][0] is None or saved_parts['Subscribe Box'][1] == True:
        subscribe_box_start_time = time.time()
        subscribe_audio_start = audio_thanks.duration + audio_topic.duration + audio_comment.duration  + audio_enjoy.duration
        subscribe_rectangle = ( ColorClip(size=settings['subscribe_box_size'], color=settings['subscribe_box_colour'])
                                .set_start(subscribe_audio_start) 
                                .set_duration(outro_audio_duration_total - subscribe_audio_start)
                                .crossfadein(1)
                                .set_position(settings['subscribe_box_position']) )
        
        saved_parts['Subscribe Box'][0] = subscribe_rectangle
        saved_parts['Subscribe Box'][1] = False
        
        subscribe_box_end_time = time.time()
        print(f"Text Time - Subscribe Box: {round(subscribe_box_end_time - subscribe_box_start_time, 2)}")
    
    
    # Comment Text
    if saved_parts['Comment'][0] is None or saved_parts['Comment'][1] == True:
        comment_start_time = time.time()
        comment_audio_start = audio_thanks.duration + audio_topic.duration + audio_enjoy.duration
        comment_text = ( TextClip(settings['comment_raw_text'], 
                                    fontsize=settings['comment_font_size'], 
                                    font=settings['font_general_text'], 
                                    color=settings['comment_colour'], 
                                    size=settings['screen_size'], 
                                    kerning=settings['comment_kerning'], 
                                    interline=settings['comment_interline']) )
            
        comment_text_border = ( TextClip(settings['comment_raw_text'], 
                                            fontsize=settings['comment_font_size'], 
                                            font=settings['font_general_text'], 
                                            color=settings['text_border_colour'], 
                                            size=settings['screen_size'], 
                                            kerning=settings['comment_kerning'], 
                                            interline=settings['comment_interline'], 
                                            stroke_width=settings['text_border_width'], 
                                            stroke_color=settings['text_border_colour']) )
        
        comment_text_combined = ( CompositeVideoClip([comment_text_border, comment_text], size=settings['screen_size'])
                                    .set_start(comment_audio_start)
                                    .set_duration(outro_audio_duration_total - comment_audio_start)
                                    .crossfadein(1)
                                    )
        
        comment_text_combined = comment_text_combined.set_position(lambda t: (
                                Animations.slide_in_slide_out(  t, 
                                                                1, 
                                                                -1,
                                                                outro_audio_duration_total - comment_audio_start, 
                                                                settings['comment_text_position'][0], 
                                                                settings['comment_anim_overshoot'], 
                                                                settings['comment_anim_right_move']),
                                                                settings['comment_text_position'][1]) ) 
        
        saved_parts['Comment'][0] = comment_text_combined
        saved_parts['Comment'][1] = False
                                                
        comment_end_time = time.time()
        print(f"Text Time - Comment: {round(comment_end_time - comment_start_time, 2)}")
    
    


    # background image
    if saved_parts['Background'][0] is None or saved_parts['Background'][1] == True:
        background_start_time = time.time()
        background_image = ( ImageClip(settings['background_image_path'])
                            .set_duration(outro_audio_duration_total) 
                            .set_position(settings['background_position']) )

        if settings['use_background_width']:
            background_image = background_image.resize(width=settings['background_size'])
        else: # use height instead
            background_image = background_image.resize(height=settings['background_size'])

        saved_parts['Background'][0] = background_image
        saved_parts['Background'][1] = False
        
        background_end_time = time.time()
        print(f"Background Time: {round(background_end_time - background_start_time, 2)}")
        
    
    # this will overlay the text on the background
    outro_video_combined = CompositeVideoClip([saved_parts['Background'][0], 
                                            saved_parts['Thanks'][0], 
                                            saved_parts['Topic'][0], 
                                            saved_parts['Comment'][0],
                                            saved_parts['Subscribe Box'][0],
                                            saved_parts['Subscribe'][0],], size=settings['screen_size'])
    outro_video_audio_combined = outro_video_combined.set_audio(outro_audio)
    
    
    Helpers.show_frame(outro_video_audio_combined, outro_audio_duration_total - 1, 4)

    outro_end_time = time.time()
    
    
    # short video for testing
    if settings['render_ou']:
        #outro_video_audio_combined = outro_video_audio_combined.subclip(0, audio_thanks.duration)
        
        print(f"Outro Starting Render, Edit Took: ", round(outro_end_time - outro_start_time, 2), " seconds")
        
        start_time = time.time()
        outro_video_audio_combined.write_videofile(
                                filename=f"{quiz_path}Finished/outro.mp4", 
                                fps=settings['fps'],  # Frame rate
                                codec="libx264",  # Video codec (h264) or 'mpeg4' could also work
                                audio=True, # Do not include audio
                                audio_codec="aac",  # Audio codec
                                audio_bitrate="192k",  # Audio bitrate
                                preset="medium",  # Compression (ultrafast, superfast, veryfast, faster, fast, medium (default), slow, slower, veryslow, placebo)
                                threads=8,  # Number of threads for processing (None for auto)
                                ffmpeg_params=[],  # Additional FFmpeg parameters: CRF for quality
                                logger="bar"
                            )
        end_time = time.time()
        total_time = round(end_time - start_time)
        total_minutes = math.floor(total_time / 60)
        total_seconds = total_time - (total_minutes * 60)
        print(f"Outro Render took: {total_minutes}:{total_seconds} seconds")
    
    return (outro_video_audio_combined, outro_audio_duration_total - 1, saved_parts)