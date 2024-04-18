import os
import json
from Make_Video_Globals import Globals

# this will make the new folder structure for a new quiz
# takes the topic and num from Globals
# and will make the settings file which will be used from here on out



# write out the json settings data myself in a nicer way
def write_json_settings(settings, file):
    
    
    
    # add some spacing \n  to make it easier to read
    add_1_line = ['fps', 'quiz_num', 'use_timer_frame', 'font_general_text', 'text_border_colour', 
                  'title_to_question_silence', 'timer_size', 'quick_pop_in_overshoot', 'how_well_position', 
                  'topic_intro_position', 'prove_audio_text', 'three_questions_position', 
                  'three_questions_anim_out_time', 'seconds_position', 'question_title_pop_in_overshoot', 
                  'question_text_kerning', 
                    'question_1_timer_position', 'answer_1_position', 'question_1_image_answer_width',
                    'question_2_timer_position', 'answer_2_position', 'question_2_image_answer_width', 
                    'question_3_timer_position', 'answer_3_position', 'question_3_image_answer_width',
                    'thanks_pop_in_overshoot', 'topic_outro_colour', 'enjoy_audio_text', 'subscribe_kerning', 
                    'subscribe_box_colour', 'comment_anim_right_move',]
    
    add_2_line = ['answer_anim_out_time', 'question_1_image_helper_width', 'question_2_image_helper_width']
    
    add_3_line = ['background_size', 'seconds_anim_out_time', 'question_3_image_helper_width']
    
    
    
    # first get the default settings
    default_settings = None
    with open(f"Automation/Default_Settings.json", "r") as default_file:
        default_settings = json.load(default_file)
        
        
    file.write("{\n") # start with open bracket
    
    
    # go through each key in default settings but use the values from the previous if they exist. 
    # this will remove any variables that arnt being used anymore
    for key in default_settings:
        
        # set the value to the previous settings if it exists
        try:
            value = settings[key]
        except KeyError: # if it doesnt exist use the default
            value = default_settings[key]
        
        # write out the key
        file.write(f"\t\"{key}\": ")
        
        
        
        # specific cases
        if key == "garbage":
            file.write(f"\"garbage\"\n")
            
            
            
            
        
        
        # depending on the type of the setting
        elif type(value) == str:
            # escape back slach n
            value = value.replace('\n', '\\n')
            file.write(f"\"{value}\",\n")
            
        elif type(value) == bool:
            if value: file.write("true,\n")
            else: file.write("false,\n")
            
        elif type(value) == list:
            file.write("[")
            for i in range(len(value)):
                if i != 0: file.write(", ")
                
                if type(value[i]) == str: file.write(f"\"{value[i]}\"")
                else: file.write(f"{value[i]}")
            file.write("],\n")
                
            
        else:
            file.write(f"{value},\n")
            
            
        if key in add_1_line:
            file.write("\n")
        elif key in add_2_line:
            file.write("\n\n")
        elif key in add_3_line:
            file.write("\n\n\n")
        
    
    file.write("}\n") # end with closed bracket
    



if __name__ == "__main__":
    quiz_folder = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}"


    # check if the parent folder exists
    if not os.path.exists(f"Topics/{Globals.topic}"):
        print("Parent folder doesnt exist so it is created")
        os.makedirs(f"Topics/{Globals.topic}")
        
        print("Making Assets Folder")
        os.makedirs(f"Topics/{Globals.topic}/Assets")
        
        

    # now check if the quiz folder exists
    if os.path.exists(f"{quiz_folder}"):
        print("This Quiz already exists, exiting")
    else:
        print("Quiz folder doesnt exist so it is created")
        os.makedirs(f"{quiz_folder}")
        
        # create the finished folder
        print("Making Finished Folder")
        os.makedirs(f"{quiz_folder}/Finished")
        
        # create the audio folder
        print("Making Audio Folder")
        os.makedirs(f"{quiz_folder}/Audio")
        
        audio_parent_folders = ["Intro", "Q1", "Q2", "Q3", "Outro"]
        
        for parent_folder in audio_parent_folders:
            print(f"Making {parent_folder} Folder")
            os.makedirs(f"{quiz_folder}/Audio/{parent_folder}")
                
                
                
        old_project_path = f"Topics/{Globals.topic}/{Globals.topic} Quiz {int(Globals.quiz_num) - 1}"
        new_project_path = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}"
        new_settings_path = new_project_path + "/settings.json"
        
        # if it is the first in this topic, or a settings file didnt exist before
        if int(Globals.quiz_num) <= 1 or not os.path.exists(old_project_path + "/settings.json"):
            # set it up with a default settings file
            with open(f"Automation/Default_Settings.json", "r") as default_file:
                settings = json.load(default_file)
                
            # update the settings with the topic and quiz number
            settings['topic'] = Globals.topic
            settings['full_topic'] = Globals.full_topic
            settings['quiz_num'] = Globals.quiz_num
            
            # update some settings which require topic and full topic
            settings['timer_path'] = new_project_path + "/Assets/Timers/"
            settings['background_image_path'] = new_project_path + "/Assets/Backgrounds/"
            
            settings['topic_intro_audio_text'] = Globals.full_topic
            settings['three_questions_audio_text'] = f"and answer these 3 {Globals.full_topic} questions, of in-creasing difficulty"
            
            settings['question_1_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_1_IMAGE"
            settings['question_1_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_1_HELPER"
            settings['question_2_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_2_IMAGE"
            settings['question_2_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_2_HELPER"
            settings['question_3_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_3_IMAGE"
            settings['question_3_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_3_HELPER"
            
            settings['topic_outro_audio_text'] = f"{Globals.full_topic} quiz."
            settings['subscribe_audio_text'] = f"and make sure to subscribe for more {Globals.full_topic} quizzes and fun facts."
            
                
                
                
        else: # there is already a settings file so i dont need to start from default
            with open(old_project_path + "/settings.json", "r") as file:
                settings = json.load(file)  
                
                # update the topic and quiz number
                settings['quiz_num'] = Globals.quiz_num
                settings.pop('garbage')
                
                # reset some variables back to default
                settings['question_1_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_1_IMAGE"
                settings['question_1_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_1_HELPER"
                settings['question_2_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_2_IMAGE"
                settings['question_2_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_2_HELPER"
                settings['question_3_image_answer_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_3_IMAGE"
                settings['question_3_image_helper_path'] = f"Topics/{Globals.topic}/Assets/ANSWER_3_HELPER"
                    
                settings['question_1_audio_text'] = "DEFAULT_QUESTION_1_AUDIO"
                settings['question_2_audio_text'] = "DEFAULT_QUESTION_2_AUDIO"
                settings['question_3_audio_text'] = "DEFAULT_QUESTION_3_AUDIO"
                
                settings['question_1_raw_text'] = "DEFAULT_QUESTION_1"
                settings['question_2_raw_text'] = "DEFAULT_QUESTION_2"
                settings['question_3_raw_text'] = "DEFAULT_QUESTION_3"
                
                settings['answer_1_audio_text'] = "DEFAULT_ANSWER_1_AUDIO"
                settings['answer_2_audio_text'] = "DEFAULT_ANSWER_2_AUDIO"
                settings['answer_3_audio_text'] = "DEFAULT_ANSWER_3_AUDIO"
                
                settings['answer_1_raw_text'] = "DEFAULT_ANSWER_1"
                settings['answer_2_raw_text'] = "DEFAULT_ANSWER_2"
                settings['answer_3_raw_text'] = "DEFAULT_ANSWER_3"
                
                # reset images size
                settings['question_1_image_answer_width'] = "1080"
                settings['question_2_image_answer_width'] = "1080"
                settings['question_3_image_answer_width'] = "1080"
                
                settings['question_1_image_helper_width'] = "1080"
                settings['question_2_image_helper_width'] = "1080"
                settings['question_3_image_helper_width'] = "1080"
                
                settings['question_1_image_answer_position'] = [0, 650]
                settings['question_2_image_answer_position'] = [0, 650]
                settings['question_3_image_answer_position'] = [0, 650]
                
                settings['question_1_image_helper_position'] = [0, 650]
                settings['question_2_image_helper_position'] = [0, 650]
                settings['question_3_image_helper_position'] = [0, 650]
                
                
                

                
                
            
                
                
        # once im done loading the settings ill save it either way
        with open(f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/settings.json", "w") as file:
            write_json_settings(settings, file)
                