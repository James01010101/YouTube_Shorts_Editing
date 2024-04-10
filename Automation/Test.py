#from pygame import image, display, event, quit
import pygame
import pygame_gui

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioClip

from PIL import Image
import sys
import numpy as np



def get_moviepy_frame_to_pygame(clip, seconds, window, video_area, scale=0.5):
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
    frame_shape = frame.shape[1::-1]  # Get the original frame size (width, height)

    # Scale the frame size by the scale factor
    scaled_size = (int(frame_shape[0] * scale), int(frame_shape[1] * scale))

    # Convert the numpy array frame to a PyGame surface
    pygame_frame = pygame.image.frombuffer(frame.tobytes(), frame_shape, "RGB")

    # Adjust scaling to fit in video_area
    max_width, max_height = video_area.width, video_area.height
    aspect_ratio = frame_shape[0] / frame_shape[1]
    scaled_width = min(max_width, int(max_height * aspect_ratio))
    scaled_height = int(scaled_width / aspect_ratio)

    # Proceed with the adjusted scaling...
    pygame_frame_scaled = pygame.transform.scale(pygame_frame, (scaled_width, scaled_height))

    # Calculate position to center the frame in the video area
    position = (video_area.left + (video_area.width - scaled_width) // 2,
                video_area.top + (video_area.height - scaled_height) // 2)

    # Draw the scaled frame to the window at the calculated position
    
    
    return pygame_frame_scaled



# this is where i will check all controls and update the values for the screen 
# also actually display the controls
def update_controls(font, window, current_slider_value, test_slider_position, test_slider_size):
    
    # Create a text surface
    text_surf = font.render(f'{current_slider_value}', True, (255, 255, 255))
    # Blit the text surface onto the window
    # Adjust the position as needed (+10 is just for padding)
    window.blit(text_surf, (test_slider_position[0] + test_slider_size[0] + 10, test_slider_position[1] + 10))  
        
    return






if __name__ == "__main__":
    
    pygame.font.init()  # Initialize the font module
    pygame.init()
    
    
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
    test_slider_position = (540 + 50, 50)
    test_slider_size = (300, 50)
    test_slider_value = 100
    test_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(test_slider_position, test_slider_size),
                                                        start_value=test_slider_value,
                                                        value_range=(0, 300),
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
                    image_dirty = True
                    
            
            
            manager.process_events(event)
        
        # Fill the background
        manager.update(time_delta)
        window.fill(BLACK)
        
        
        # if the controls have change i need to recalculate the image
        if image_dirty:
            editing_image = get_moviepy_frame_to_pygame(clip, 15, window, video_area)  # Show a frame at 10 seconds
        
        
        # Display a frame from the clip
        window.blit(editing_image, position)
        
        # display all of the controls
        update_controls(font, window, test_slider_value, test_slider_position, test_slider_size)
        
        manager.draw_ui(window)
        
        
        
        # Update the display
        pygame.display.flip()

    # Quit PyGame
    pygame.quit()
    sys.exit()






'''
    
pygame.init()

# Set up the display
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Slider Example")
background = pygame.Surface(window_size)
background.fill(pygame.Color('#000000'))

# Set up PyGame GUI
manager = pygame_gui.UIManager(window_size)
opacity_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((350, 550), (100, 50)),
                                                        start_value=100,
                                                        value_range=(0, 100),
                                                        manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)
    
    manager.update(time_delta)
    
    window.blit(background, (0, 0))
    manager.draw_ui(window)
    
    pygame.display.update()

pygame.quit()

'''
