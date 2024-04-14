


import time

import Make_Video_Sections as Make_Video_Sections
from Make_Video_Globals import Globals

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

if settings['testing'] == 1:
    print("### You are trying to render with testing on ###")
    
start_time = time.time()

saved_parts = {
    'Thanks': [[None, None], True],
    'Topic': [[None, None], True],
    'Subscribe': [[None, None], True],
    'Subscribe Box': [None, True],
    'Comment': [[None, None], True],
    'Background': [None, True]
}

(outro_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_outro(settings, saved_parts, True)
print(f"Outro Editing and Render Took: {round(time.time() - start_time, 2)} seconds\n\n")