


import time

import Make_Video_Sections as Make_Video_Sections
from Make_Video_Globals import Globals
import Interactive_Editor

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

start_time = time.time()
        
saved_parts = {
    'Thanks': [[None, None], True],
    'Topic': [[None, None], True],
    'Subscribe': [[None, None], True],
    'Subscribe Box': [None, True],
    'Comment': [[None, None], True],
    'Background': [None, True]
}
Interactive_Editor.run_pygame_editor(settings, 'outro')
print(f"Outro Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")