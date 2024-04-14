


import time

import Make_Video_Sections as Make_Video_Sections
from Make_Video_Globals import Globals

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

if settings['testing'] == 1:
    print("### You are trying to render with testing on ###")
    
start_time = time.time()
            
saved_parts = {
    'Title': [[None, None], True],
    'Question': [[None, None], True],
    'Answer Image': [None, True],
    'Answer': [[None, None], True],
    'Background': [None, True],
    'Timer': [None, True]
}

(q1_final_video, screenshot_time, saved_parts) = Make_Video_Sections.make_questions(settings, saved_parts, 3, True)
print(f"Q3 Editing and Render Took: {round(time.time() - start_time, 2)} seconds\n\n")