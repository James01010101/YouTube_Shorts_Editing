
# this will be where i run the pygame to edit my video 
#from pygame import image, display, event, quit
import pygame
import pygame_gui

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip

import Make_Video_Sections
import New_Folder
from Make_Video_Globals import Globals

from PIL import Image
import sys
import numpy as np
import time




class Slider_Control:
    def __init__(self, y_pos, label, part_label, settings_label, settings, value_range, increment, value_type, scaled_screen_size):
        self.slider_position = (scaled_screen_size[0] + 400, y_pos)
        self.slider_size = (300, 50)
        self.slider_label = label
        self.settings = settings
        self.settings_label = settings_label
        self.value_range = value_range
        self.slider_increment = increment
        self.scaled_screen_size = scaled_screen_size
        self.part_label = part_label # this will be used to access the parts dict
        
        
        self.revert_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.slider_position[0] + self.slider_size[0] + 225, self.slider_position[1]), (100, 50)),
                                      text='Revert')
        
        
        # if -1 its just a raw number
        # if 0 its a tuple and i want the 0th index
        # if 1 its a tuple and i want the 1st index
        self.value_type = value_type 
        
        if self.value_type == -1:
            self.original_value = settings[settings_label]
            self.slider = pygame_gui.elements.UIHorizontalSlider(
                                        relative_rect=pygame.Rect(self.slider_position, self.slider_size),
                                        start_value=self.settings[self.settings_label],
                                        value_range=self.value_range,
                                        click_increment=self.slider_increment)
            
        else: # its a tuple so slightly different
            self.original_value = settings[settings_label][self.value_type]
            self.slider = pygame_gui.elements.UIHorizontalSlider(
                                        relative_rect=pygame.Rect(self.slider_position, self.slider_size),
                                        start_value=self.settings[self.settings_label][self.value_type],
                                        value_range=self.value_range,
                                        click_increment=self.slider_increment)
            
        
    
    def draw_text_to_window(self, window, font):
        # show the current value
        text_surf = font.render(f'{self.get_slider_value()}', True, (255, 255, 255))
        window.blit(text_surf, (self.slider_position[0] + self.slider_size[0] + 10, self.slider_position[1] + 10)) 
        
        # show the original value
        text_surf = font.render(f'({self.original_value})', True, (255, 255, 255))
        window.blit(text_surf, (self.slider_position[0] + self.slider_size[0] + 110, self.slider_position[1] + 10)) 
        
        # show the label
        text_surf = font.render(f'{self.slider_label}', True, (255, 255, 255))
        window.blit(text_surf, (self.scaled_screen_size[0] + 10, self.slider_position[1] + 10))  
        
    
    def revert_value(self):
        self.set_slider_value(self.original_value)
        self.slider.set_current_value(self.original_value)
        
    def get_id(self):
        return self.slider
    
    def set_slider_value(self, value):
        if self.value_type == -1:
            self.settings[self.settings_label] = value
        else:
            self.settings[self.settings_label][self.value_type] = value
            
        
    def get_slider_value(self):
        if self.value_type == -1:
            return self.settings[self.settings_label]
        else:
            return self.settings[self.settings_label][self.value_type]



def get_moviepy_frame_to_pygame(clip, seconds, screen_size, scale):
    """
    Display a scaled frame at a given time from a clip in a PyGame window.
    
    Args:
    clip: moviepy VideoClip object
    seconds: Time in seconds to grab the frame from the clip
    window: The PyGame window surface to display the frame on
    scale: Scale factor for the frame (0.5 for 50% size)
    """
    # Get the frame from the clip
    frame = clip.get_frame(seconds)

    # Convert the edited_frame to uint8 if it's not already
    if frame.dtype != np.uint8:
        frame = frame.astype(np.uint8)
    
    # Convert the numpy array frame to a PyGame surface
    pygame_frame = pygame.image.frombuffer(frame.tobytes(), screen_size, "RGB")
    
    # Proceed with the adjusted scaling...
    pygame_frame_scaled = pygame.transform.scale(pygame_frame, (screen_size[0] * scale, screen_size[1] * scale))
    
    
    return pygame_frame_scaled




def run_pygame_editor(settings, section):
    
    pygame.font.init()  # Initialize the font module
    pygame.init()
    
    if settings["testing"] == 1:
        print("### Testing On ###")
    
    screen_size = (1080, 1920)
    scale = 0.6
    scaled_screen_size = (int(screen_size[0]*scale), int(screen_size[1]*scale))
    extra_control_space = 800
    
    
    
    # Set up the display
    window_size = (screen_size[0] + extra_control_space, scaled_screen_size[1]) # add as much to x as i want for more space for controls
    video_area_width = scaled_screen_size[0] # keps aspect ratio
    controls_area_width = window_size[0] - video_area_width
    
    # Define rects for each area for easier management
    video_area = pygame.Rect(0, 0, video_area_width, window_size[1])
    controls_area = pygame.Rect(video_area_width, 0, controls_area_width, window_size[1])
    
    # make the pygame window
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Frame Preview")
    
    # pygame gui stuff
    manager = pygame_gui.UIManager(window_size)
    
    
    # font sizes for text
    font_size = 50
    font = pygame.font.Font(None, font_size)  # None uses the default font
    
    
    # create all my controls and values    
    update_image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scaled_screen_size[0] + 10, scaled_screen_size[1] - 50), (200, 50)),
                                      text='Update Image',
                                      manager=manager)
    
    save_image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scaled_screen_size[0] + 260, scaled_screen_size[1] - 50), (200, 50)),
                                      text='Save Settings',
                                      manager=manager)
    
    discard_image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scaled_screen_size[0] + 510, scaled_screen_size[1] - 50), (200, 50)),
                                      text='Discard Settings',
                                      manager=manager)
    
    # flip from timer frame to answer frame
    helper_image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((scaled_screen_size[0] + 760, scaled_screen_size[1] - 50), (200, 50)),
                                      text='Swap Debug Image',
                                      manager=manager)
    
    

    
    all_slider_controls = []
    # text for this section
    if section == 'intro':
        
        # this will store the text with a dirty bool so i can know if i need to recalculate it
        saved_parts = {
            'Quick': [[None, None], True],
            'How Well': [[None, None], True],
            'Topic': [[None, None], True],
            '3 Questions': [[None, None], True],
            'Seconds': [[None, None], True],
            'Background': [None, True]
        }
        
        
        all_slider_controls.append(Slider_Control(0, "Quick Size", "Quick", "quick_font_size", settings, (0, 350), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(50, "Quick Position Y", "Quick", "quick_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(150, "How Well Size", "How Well", "how_well_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(200, "How Well Interline", "How Well", "how_well_interline", settings, (-150, 150), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(250, "How Well Position Y", "How Well", "how_well_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(350, "Topic Size", "Topic", "topic_intro_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(400, "Topic Interline", "Topic", "topic_intro_interline", settings, (-150, 150), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(450, "Topic Position Y", "Topic", "topic_intro_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(550, "3 Questions Size", "3 Questions", "three_questions_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(600, "3 Questions Position Y", "3 Questions", "three_questions_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(700, "Seconds Size", "Seconds", "seconds_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(750, "Seconds Position Y", "Seconds", "seconds_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))

    elif section == 'q1':
        
        # this will store the text with a dirty bool so i can know if i need to recalculate it
        saved_parts = {
            'Title': [[None, None], True],
            'Question': [[None, None], True],
            'Answer Image': [None, True],
            'Answer': [[None, None], True],
            'Background': [None, True],
            'Timer': [None, True]
        }
        
        all_slider_controls.append(Slider_Control(0, "Title Size", "Title", "question_title_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(50, "Title Position Y", "Title", "question_title_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(150, "Question Size", "Question", "question_1_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(200, "Question Position Y", "Question", "question_1_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(250, "Question Interline", "Question", "question_1_text_interline", settings, (-1000, 1000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(300, "Question Wrap Width", "Question", "question_1_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(400, "Answer Image Width", "Answer Image", "question_1_image_answer_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(450, "Answer Image PosX", "Answer Image", "question_1_image_answer_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(500, "Answer Image PosY", "Answer Image", "question_1_image_answer_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        # add helper image here (use answer image for helper they are both done in the same code, so dont need to seperate them)
        all_slider_controls.append(Slider_Control(600, "Helper Image Width", "Answer Image", "question_1_image_helper_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(650, "Helper Image PosX", "Answer Image", "question_1_image_helper_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(700, "Helper Image PosY", "Answer Image", "question_1_image_helper_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(800, "Answer Size", "Answer", "answer_1_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(850, "Answer Position Y", "Answer", "answer_1_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(900, "Answer Wrap Width", "Answer", "answer_1_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
        
        
    elif section == 'q2':
        
        # this will store the text with a dirty bool so i can know if i need to recalculate it
        saved_parts = {
            'Title': [[None, None], True],
            'Question': [[None, None], True],
            'Answer Image': [None, True],
            'Answer': [[None, None], True],
            'Background': [None, True],
            'Timer': [None, True]
        }
        
        all_slider_controls.append(Slider_Control(0, "Title Size", "Title", "question_title_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(50, "Title Position Y", "Title", "question_title_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(150, "Question Size", "Question", "question_2_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(200, "Question Position Y", "Question", "question_2_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(250, "Question Interline", "Question", "question_2_text_interline", settings, (-1000, 1000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(300, "Question Wrap Width", "Question", "question_2_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(400, "Answer Image Width", "Answer Image", "question_2_image_answer_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(450, "Answer Image PosX", "Answer Image", "question_2_image_answer_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(500, "Answer Image PosY", "Answer Image", "question_2_image_answer_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        # add helper image here (use answer image for helper they are both done in the same code, so dont need to seperate them)
        all_slider_controls.append(Slider_Control(600, "Helper Image Width", "Answer Image", "question_2_image_helper_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(650, "Helper Image PosX", "Answer Image", "question_2_image_helper_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(700, "Helper Image PosY", "Answer Image", "question_2_image_helper_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(800, "Answer Size", "Answer", "answer_2_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(850, "Answer Position Y", "Answer", "answer_2_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(900, "Answer Wrap Width", "Answer", "answer_2_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
        
    
    elif section == 'q3':
        
        # this will store the text with a dirty bool so i can know if i need to recalculate it
        saved_parts = {
            'Title': [[None, None], True],
            'Question': [[None, None], True],
            'Answer Image': [None, True],
            'Answer': [[None, None], True],
            'Background': [None, True],
            'Timer': [None, True]
        }
        
        all_slider_controls.append(Slider_Control(0, "Title Size", "Title", "question_title_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(50, "Title Position Y", "Title", "question_title_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(150, "Question Size", "Question", "question_3_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(200, "Question Position Y", "Question", "question_3_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(250, "Question Interline", "Question", "question_3_text_interline", settings, (-1000, 1000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(300, "Question Wrap Width", "Question", "question_3_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(400, "Answer Image Width", "Answer Image", "question_3_image_answer_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(450, "Answer Image PosX", "Answer Image", "question_3_image_answer_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(500, "Answer Image PosY", "Answer Image", "question_3_image_answer_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        # add helper image here (use answer image for helper they are both done in the same code, so dont need to seperate them)
        all_slider_controls.append(Slider_Control(600, "Helper Image Width", "Answer Image", "question_3_image_helper_width", settings, (0, 2000), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(650, "Helper Image PosX", "Answer Image", "question_3_image_helper_position", settings, (-500, 500), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(700, "Helper Image PosY", "Answer Image", "question_3_image_helper_position", settings, (0, 2000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(800, "Answer Size", "Answer", "answer_3_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(850, "Answer Position Y", "Answer", "answer_3_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(900, "Answer Wrap Width", "Answer", "answer_3_text_wrap_width", settings, (0, 50), 1, -1, scaled_screen_size))
    
    if section == 'outro':
        
        # this will store the text with a dirty bool so i can know if i need to recalculate it
        saved_parts = {
            'Thanks': [[None, None], True],
            'Topic': [[None, None], True],
            'Subscribe': [[None, None], True],
            'Subscribe Box': [None, True],
            'Comment': [[None, None], True],
            'Background': [None, True]
        }
        
        
        all_slider_controls.append(Slider_Control(0, "Thanks Size", "Thanks", "thanks_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(50, "Thanks Position Y", "Thanks", "thanks_text_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(100, "Thanks Interline", "Thanks", "thanks_interline", settings, (-150, 150), 5, -1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(200, "Topic Size", "Topic", "topic_outro_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(250, "Topic Interline", "Topic", "topic_outro_interline", settings, (-150, 150), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(300, "Topic Position Y", "Topic", "topic_outro_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(400, "Subscribe Size", "Subscribe", "subscribe_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(450, "Subscribe Position Y", "Subscribe", "subscribe_text_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        
        all_slider_controls.append(Slider_Control(550, "Subscribe Size X", "Subscribe Box", "subscribe_box_size", settings, (0, 1100), 5, 0, scaled_screen_size))
        all_slider_controls.append(Slider_Control(600, "Subscribe Size Y", "Subscribe Box", "subscribe_box_size", settings, (0, 500), 5, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(650, "Subscribe Box PosY", "Subscribe Box", "subscribe_box_position", settings, (0, 2000), 5, 1, scaled_screen_size))

        all_slider_controls.append(Slider_Control(750, "Comment Size", "Comment", "comment_font_size", settings, (0, 300), 5, -1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(800, "Comment Position Y", "Comment", "comment_text_position", settings, (-1000, 1000), 25, 1, scaled_screen_size))
        all_slider_controls.append(Slider_Control(850, "Comment Interline", "Comment", "comment_interline", settings, (-150, 150), 5, -1, scaled_screen_size))

    


    # variables i need
    image_dirty = True
    editing_image = None
        
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame.QUIT:
                running = False
                
                
            # check for gui slider events
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                for sc in all_slider_controls:
                    if event.ui_element == sc.get_id():
                        sc.set_slider_value(event.value)
                        saved_parts[sc.part_label][1] = True
            
            
        # check if any revert buttons have been pressed  
        for sc in all_slider_controls:  
            if sc.revert_button.check_pressed():
                sc.revert_value()  
                saved_parts[sc.part_label][1] = True     
            



        # check if i pressed the update image button
        if update_image_button.check_pressed():
            image_dirty = True
            
        elif save_image_button.check_pressed():
            running = False
            # write the new settings to the file
            with open(f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}/settings.json", "w") as file:
                New_Folder.write_json_settings(settings, file)
                
        elif discard_image_button.check_pressed():
            running = False
            
        elif helper_image_button.check_pressed():
            settings['use_timer_frame'] = not settings['use_timer_frame']
            image_dirty = True
            
            
    
        
        # Fill the background
        manager.update(time_delta)
        window.fill((0, 0, 0))
        
        
        # if the controls have change i need to recalculate the image
        if image_dirty:
            # recalculate the new image
            if section == 'intro':
                
                start_editing_time = time.time()
                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time, saved_parts) = Make_Video_Sections.make_intro(settings, saved_parts, False)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
                
                end_editing_time = time.time()
                print("Intro Editing Took: ", round(end_editing_time - start_editing_time, 2), " seconds\n")
                
            elif section == 'q1':
                
                start_editing_time = time.time()
                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 1, False)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
                
                end_editing_time = time.time()
                print("Q1 Editing Took: ", round(end_editing_time - start_editing_time, 2), " seconds\n")
                
            elif section == 'q2':
                
                start_editing_time = time.time()
                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 2, False)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
                
                end_editing_time = time.time()
                print("Q2 Editing Took: ", round(end_editing_time - start_editing_time, 2), " seconds\n")
                
            elif section == 'q3':
                
                start_editing_time = time.time()
                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 3, False)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
                
                end_editing_time = time.time()
                print("Q3 Editing Took: ", round(end_editing_time - start_editing_time, 2), " seconds\n")
                
            elif section == 'outro':
                
                start_editing_time = time.time()
                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time, saved_parts) = Make_Video_Sections.make_outro(settings, saved_parts, False)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
                
                end_editing_time = time.time()
                print("Outro Editing Took: ", round(end_editing_time - start_editing_time, 2), " seconds\n")
        
        
        # Display a frame from the clip
        window.blit(editing_image, (0, 0))
        
        
        # update the controls
        # test slider value
        for sc in all_slider_controls:
            sc.draw_text_to_window(window, font)

        
        manager.draw_ui(window)
        
        
        
        # Update the display
        pygame.display.flip()

    # Quit PyGame
    pygame.quit()





