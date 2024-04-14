


import time

import Make_Video_Sections as Make_Video_Sections
from Make_Video_Globals import Globals
import Interactive_Editor

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

start_time = time.time()
        
saved_parts = {
    'Title': [[None, None], True],
    'Question': [[None, None], True],
    'Answer Image': [None, True],
    'Answer': [[None, None], True],
    'Background': [None, True],
    'Timer': [None, True]
}
Interactive_Editor.run_pygame_editor(settings, 'q2')
print(f"Q2 Editing Took: {round(time.time() - start_time, 2)} seconds\n\n")