import os
import json
from Make_Video_Globals import Globals

# this will make the new folder structure for a new quiz
# takes the topic and num from Globals
# and will make the settings file which will be used from here on out



# write out the json settings data myself in a nicer way
def write_json_settings(settings, file):
    
    # add some spacing \n  to make it easier to read
    add_1_line = ['fps', 'use_timer_frame', 'edit_ou', 'font_general_text', 'text_border_colour', 
                    'timer_path', 'background_size', 'question_1_timer_position', 'answer_1_position', 
                    'question_2_timer_position', 'answer_2_position', 'question_3_timer_position', 
                    'answer_3_position', 'quick_pop_in_overshoot', 'how_well_position', 
                    'topic_intro_position', 'three_questions_position', 'three_questions_anim_out_time', 
                    'seconds_position', 'question_raw_text', 'question_text_interline', 
                    'thanks_pop_in_overshoot', 'topic_outro_colour', 'subscribe_kerning', 'subscribe_box_colour',
                    'question_1_image_use_helper', 'question_2_image_use_helper', 'question_3_image_use_helper']
    
    add_2_line = []
    
    add_3_line = ['quiz_num', 'render_ou', 'title_to_question_silence', "question_1_image_helper_width", 
                  "question_2_image_helper_width", "question_3_image_helper_width", 'seconds_anim_out_time', 
                  'answer_anim_out_time']
        
        
    file.write("{\n") # start with open bracket
    
    
    for key in settings:
        value = settings[key]
        
        # write out the key
        file.write(f"\t\"{key}\": ")
        
        
        
        # specific cases
        if key in ["question_1_timer_position", "question_2_timer_position", "question_3_timer_position"]:
            ["center", 1250],
            file.write(f"[\"center\", 1250],\n")
            
            
        
        
        # depending on the type of the setting
        elif type(value) == str:
            # escape back slach n
            value = value.replace('\n', '\\n')
            file.write(f"\"{value}\",\n")
            
        elif type(value) == bool:
            if value: file.write("true,\n")
            else: file.write("false,\n")
            
        else:
            file.write(f"{value},\n")
            
            
        if key in add_1_line:
            file.write("\n")
        elif key in add_2_line:
            file.write("\n\n")
        elif key in add_3_line:
            file.write("\n\n\n")
        
    
    # write some garbage comment so i dont have to deal with the last comma
    file.write("\n\n\t\"garbage\": \"garbage\"\n")
    file.write("}\n") # end with closed bracket
    



quiz_folder = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}"


# check if the parent folder exists
if not os.path.exists(f"Topics/{Globals.topic}"):
    print("Parent folder doesnt exist so it is created")
    os.makedirs(f"Topics/{Globals.topic}")
    
    print("Making Assets Folder")
    os.makedirs(f"Topics/{Globals.topic}/Assets")
    
    

# now check if the quiz folder exists
if not os.path.exists(f"{quiz_folder}"):
    print("Quiz folder doesnt exist so it is created")
    os.makedirs(f"{quiz_folder}")
    
    # create the finished folder
    print("Making Finished Folder")
    os.makedirs(f"{quiz_folder}/Finished")
    
    # create the audio folder
    print("Making Audio Folder")
    os.makedirs(f"{quiz_folder}/Audio")
    
    audio_parent_folders = ["Intro", "Q1", "Q2", "Q3", "Outro"]
    audio_sub_folders = ["Script", "Wav"]
    
    for parent_folder in audio_parent_folders:
        for sub_folder in audio_sub_folders:
            print(f"Making {parent_folder} {sub_folder} Folder")
            os.makedirs(f"{quiz_folder}/Audio/{parent_folder}/{sub_folder}")
            
            
            
        
    
    # finally make the settings file which should be a copy of the previous one if num > 1
    if int(Globals.quiz_num) > 1:
        try:
            with open(f"Topics/{Globals.topic}/{Globals.topic} Quiz {int(Globals.quiz_num) - 1}/settings.json", "r") as file:
                settings = json.load(file)  
                
                # update the topic and quiz number
                settings['topic'] = Globals.topic
                settings['full_topic'] = Globals.topic
                settings['quiz_num'] = Globals.quiz_num
                settings.pop('garbage')
                
                
        except FileNotFoundError: # if the file doesnt exist use default
            # set it up with a default settings file
            with open(f"Automation/Default_Settings.json", "r") as file:
                settings = json.load(file)
                
                #update the settings with the topic and quiz number
                settings['topic'] = Globals.topic
                settings['full_topic'] = Globals.topic
                settings['quiz_num'] = Globals.quiz_num
                
            
    else:
        # set it up with a default settings file
        with open(f"Automation/Default_Settings.json", "r") as file:
            settings = json.load(file)
            
            #update the settings with the topic and quiz number
            settings['topic'] = Globals.topic
            settings['full_topic'] = Globals.topic
            settings['quiz_num'] = Globals.quiz_num
            
            
    # once im done loading the settings ill save it either way
    with open(f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/settings.json", "w") as file:
        write_json_settings(settings, file)
            