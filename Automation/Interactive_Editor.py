
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




class Slider_Control:
    def __init__(self, y_pos, label, settings_label, settings, value_range, increment, value_type, scaled_screen_size, manager):
        self.slider_position = (scaled_screen_size[0] + 400, y_pos)
        self.slider_size = (300, 50)
        self.slider_label = label
        self.settings = settings
        self.settings_label = settings_label
        self.value_range = value_range
        self.slider_increment = increment
        self.scaled_screen_size = scaled_screen_size
        
        
        self.revert_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.slider_position[0] + self.slider_size[0] + 225, self.slider_position[1]), (100, 50)),
                                      text='Revert',
                                      manager=manager)
        
        
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
                                        click_increment=self.slider_increment,
                                        manager=manager)
            
        else: # its a tuple so slightly different
            self.original_value = settings[settings_label][self.value_type]
            self.slider = pygame_gui.elements.UIHorizontalSlider(
                                        relative_rect=pygame.Rect(self.slider_position, self.slider_size),
                                        start_value=self.settings[self.settings_label][self.value_type],
                                        value_range=self.value_range,
                                        click_increment=self.slider_increment,
                                        manager=manager)
            
        
    
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
    
    

    
    all_slider_controls = []
    # text for this section
    if section == 'intro':
        all_slider_controls.append(Slider_Control(0, "Quick Size", "quick_font_size", settings, (0, 300), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(50, "Quick Position Y", "quick_position", settings, (-1000, 1000), 25, 1, scaled_screen_size, manager))
        
        all_slider_controls.append(Slider_Control(150, "How Well Size", "how_well_font_size", settings, (0, 300), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(200, "How Well Interline", "how_well_interline", settings, (-150, 150), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(250, "How Well Position Y", "how_well_position", settings, (-1000, 1000), 25, 1, scaled_screen_size, manager))
        
        all_slider_controls.append(Slider_Control(350, "Topic Size", "topic_intro_font_size", settings, (0, 300), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(400, "Topic Interline", "topic_intro_interline", settings, (-150, 150), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(450, "Topic Position Y", "topic_intro_position", settings, (-1000, 1000), 25, 1, scaled_screen_size, manager))
        
        all_slider_controls.append(Slider_Control(550, "3 Questions Size", "three_questions_font_size", settings, (0, 300), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(600, "3 Questions Position Y", "three_questions_position", settings, (-1000, 1000), 25, 1, scaled_screen_size, manager))
        
        all_slider_controls.append(Slider_Control(700, "Seconds Size", "seconds_font_size", settings, (0, 300), 5, -1, scaled_screen_size, manager))
        all_slider_controls.append(Slider_Control(750, "Seconds Position Y", "seconds_position", settings, (-1000, 1000), 25, 1, scaled_screen_size, manager))
    
    
    
    
    
    
    

    # Define your colors
    BLACK = (0, 0, 0)
    
    # Load your video clip (replace 'your_video.mp4' with your actual video file path)
    clip = VideoFileClip('Topics/Fortnite/Fortnite Quiz 3/Finished/Fortnite Quiz 3.mp4')


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
            
            
        # check if any revert buttons have been pressed  
        for sc in all_slider_controls:  
            if sc.revert_button.check_pressed():
                sc.revert_value()       
            



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
            
        


           
        
        # Fill the background
        manager.update(time_delta)
        window.fill(BLACK)
        
        
        # if the controls have change i need to recalculate the image
        if image_dirty:
            # recalculate the new image
            if section == 'intro':

                # settings will already be kept up to date so just make the new image
                (edited_clip, screenshot_time) = Make_Video_Sections.make_intro(settings)
                editing_image = get_moviepy_frame_to_pygame(edited_clip, screenshot_time, screen_size, scale)
                image_dirty = False
        
        
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
    sys.exit()





