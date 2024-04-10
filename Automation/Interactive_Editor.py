
# this will be where i run the pygame to edit my video 
#from pygame import image, display, event, quit
import pygame
import pygame_gui

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip

import Make_Video_Sections

from PIL import Image
import sys
import numpy as np



def get_moviepy_frame_to_pygame(clip, seconds, screen_size, scale=0.5):
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
    
    
    # Set up the display
    window_size = (1080, 1920/2)
    video_area_width = 1080/2 # half for video half for sliders
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
    update_image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 900), (200, 50)),
                                      text='Update Image',
                                      manager=manager)

    
    
    test_slider_position = (540 + 50, 50)
    test_slider_size = (300, 50)
    test_slider_value = 100
    test_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(test_slider_position, test_slider_size),
                                                        start_value=test_slider_value,
                                                        value_range=(0, 300),
                                                        click_increment=25,
                                                        manager=manager)
    
    

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
            if event.type == pygame.QUIT:
                running = False
                
                
            # check for gui slider events
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == test_slider:
                    test_slider_value = event.value
                    
                    
            
            
            manager.process_events(event)
        
        # Fill the background
        manager.update(time_delta)
        window.fill(BLACK)
        
        
        # if the controls have change i need to recalculate the image
        if image_dirty:
            # recalculate the new image
            if section == 'intro':
                edited_clip = Make_Video_Sections.make_intro(settings)
            
                editing_image = get_moviepy_frame_to_pygame(edited_clip, 5, screen_size, 0.5)
                image_dirty = False
        
        
        # Display a frame from the clip
        window.blit(editing_image, (0, 0))
        
        
        
        # display all of the controls
        
        # 
        
        
        # test slider value
        text_surf = font.render(f'{test_slider_value}', True, (255, 255, 255))
        window.blit(text_surf, (test_slider_position[0] + test_slider_size[0] + 10, test_slider_position[1] + 10))  

        
        manager.draw_ui(window)
        
        
        
        # Update the display
        pygame.display.flip()

    # Quit PyGame
    pygame.quit()
    sys.exit()





