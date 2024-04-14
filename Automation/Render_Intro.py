


import time

import Make_Video_Sections as Make_Video_Sections
from Make_Video_Globals import Globals

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

if settings['testing'] == 1:
    print("### You are trying to render with testing on ###")

start_time = time.time()
        
saved_parts = {
    'Quick': [[None, None], True],
    'How Well': [[None, None], True],
    'Topic': [[None, None], True],
    '3 Questions': [[None, None], True],
    'Seconds': [[None, None], True],
    'Background': [None, True]
}
(intro_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_intro(settings, saved_parts, True)
print(f"Intro Editing and Render Took: {round(time.time() - start_time, 2)} seconds\n\n")