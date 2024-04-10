
import json

class Globals:
    topic = "Horizon"
    quiz_num = "3"
    

    def read_settings_file(topic, quiz_num):
        with open(f"Topics/{topic}/{topic} Quiz {quiz_num}/settings.json", "r") as file:
            return json.load(file)  
    
    
    
    
    # variables to make globals work until i remove it all
    screen_size = (1080, 1920)
    
    # go through each topic so i can save its variables so i dont have to change everything every time
    if topic == "Horizon":
            
        ''' Text '''
        ''' Fonts '''
        # Generic = "Arial-Rounded-MT-Bold"
        # AOT = "Cloister-Black-Light"
        
        # seperating these out because some fonts arnt easy to read but i still want them for the topic question and titles
        font_topic = "horizon" # the font for the topic eg (AOT)
        font_title = "horizon" # used for Question titles
        font_general_text = "Arial-Rounded-MT-Bold" # use for all other text
        
        
        ''' Text Borders '''
        text_border_width = 40
        text_border_colour = 'black'
        
        
        # have the debug frame be with the timer so i can make sure its not overlapping
        use_timer_frame = True
        
        
        
        #background
        background_image_path = f"{topic}/Assets/Backgrounds/FW 1.jpg"
        background_position = (0, 0)
        use_background_width = False # either start with width or height
        
        # is use width use screen_size[0] else use screen_size[1]
        background_size = screen_size[1]
        

        # Question 1 easy
        question_1_raw_text = "What is the name\nof this Machine?"
        question_1_font_size = 100
        question_1_position = ("center", -550)
        question_1_timer_position = (75, 625)
        
        answer_1_raw_text = "Scrapper"
        answer_1_font_size = 175
        answer_1_position = ("center", 500)
        answer_1_image_path = f"{topic}/Assets/Machines/Scrapper/Scrapper 3.jpg"
        answer_1_image_helper = True # if it is shown for the whole question or just the answer
        answer_1_image_position = (0, 625)
        answer_1_image_width = screen_size[0] + 100
        
        
        # Question 2 medium
        question_2_raw_text = "What is the name\nof this Character?"
        question_2_font_size = 100
        question_2_position = ("center", -550)
        question_2_timer_position = (75, 625)
        
        answer_2_raw_text = "Rost"
        answer_2_font_size = 175
        answer_2_position = ("center", 500)
        answer_2_image_path = f"{topic}/Assets/Characters/Rost/Rost 1.jpg"
        answer_2_image_helper = True
        answer_2_image_position = (-350, 625)
        answer_2_image_width = screen_size[0] + 400
        
        
        # Question 3 hard
        question_3_raw_text = "Name the Sub-Func\ntasked with restoring\nplant life to Earth?"
        question_3_font_size = 80
        question_3_position = ("center", -525)
        question_3_timer_position = ('center')
        
        answer_3_raw_text = "Demeter"
        answer_3_font_size = 175
        answer_3_position = ("center", 500)
        answer_3_image_path = f"{topic}/Assets/AI/Demeter.png"
        answer_3_image_helper = False
        answer_3_image_position = ('center', 550)
        answer_3_image_width = screen_size[0] + 500
        
        
        
        ''' Sections '''
        ''' Intro '''
        quick_raw_text = "Quick"
        quick_font_size = 275
        quick_colour = 'yellow'
        quick_kerning = 0
        quick_position = (0, -750)
        
        how_well_raw_text = "How Well Do\nYou Know"
        how_well_font_size = 140
        how_well_colour = 'cyan'
        how_well_kerning = 0
        how_well_interline = -25
        how_well_position = ('center', -400)
        
        topic_intro_font_size = 180
        topic_intro_colour = 'white'
        topic_intro_kerning = -10
        topic_intro_interline = 0
        topic_intro_position = ("center", 50)
        
        three_questions_raw_text = "3 Questions"
        three_questions_font_size = 150
        three_questions_colour = 'orange'
        three_questions_kerning = 0
        three_questions_position = ("center", 425)
        
        seconds_raw_text = "3 Seconds"
        seconds_font_size = 150
        seconds_colour = 'orange'
        seconds_kerning = 0
        seconds_position = ("center", 600)
        
        
        
        ''' Questions'''
        question_title_font_size = 170
        question_title_colour = 'yellow'
        question_title_position = (0, -750)
        question_title_kerning = -10
        
        question_raw_text = 'Question'
        
        question_text_colour = 'cyan'
        question_text_kerning = 0
        question_text_interline = -20
        
        answer_colour = 'orange'
        answer_kerning = 0
        answer_interline = -20
        
        
        
        ''' Outro '''
        thanks_raw_text = "Thanks For\nPlaying"
        thanks_font_size = 160
        thanks_text_position = (0, -675)
        thanks_colour = 'yellow'
        thanks_kerning = 0
        thanks_interline = -20
        
        topic_outro_position = ("center", -190)
        topic_outro_font_size = 180
        topic_outro_kerning = -10
        topic_outro_interline = 0
        topic_outro_colour = 'white'
        
        subscribe_raw_text = "Subscribe!"
        subscribe_font_size = 150
        subscribe_text_position = ("center", 250)
        subscribe_colour = 'white'
        subscribe_kerning = 0
        
        subscribe_box_position = ("center", 1105)
        subscribe_box_size = (850, 200)
        subscribe_box_colour = (255, 0, 0) # this has to be rgb instead of name
        
        comment_raw_text = "Comment Your\nScore Below"
        comment_font_size = 115
        comment_text_position = ("center", 550)
        comment_interline = 0
        comment_colour = 'orange'
        comment_kerning = 0
        
    elif topic == "TLOU":
            
        ''' Text '''
        ''' Fonts '''
        # Generic = "Arial-Rounded-MT-Bold"
        # AOT = "Cloister-Black-Light"
        
        # seperating these out because some fonts arnt easy to read but i still want them for the topic question and titles
        font_topic = "Headliner-No.-45" # the font for the topic eg (AOT)
        font_title = "Headliner-No.-45" # used for Question titles
        font_general_text = "Headliner-No.-45" # use for all other text
        
        
        ''' Text Borders '''
        text_border_width = 40
        text_border_colour = 'black'
        
        
        # have the debug frame be with the timer so i can make sure its not overlapping
        use_timer_frame = False
        
        
        
        #background
        background_image_path = f"{topic}/Assets/Backgrounds/Tralier 1.jpg"
        background_position = (0, 0)
        use_background_width = False # either start with width or height
        
        # is use width use screen_size[0] else use screen_size[1]
        background_size = screen_size[1]
        

        # Question 1 easy
        question_1_raw_text = "What is the full name\nof this Character?"
        question_1_font_size = 130
        question_1_position = ("center", -500)
        question_1_timer_position = (75, 625)
        
        answer_1_raw_text = "Tommy Miller"
        answer_1_font_size = 200
        answer_1_position = ("center", 500)
        answer_1_image_path = f"{topic}/Assets/Characters/Tommy/Tommy 1.jpeg"
        answer_1_image_helper = True # if it is shown for the whole question or just the answer
        answer_1_image_position = (-100, 600)
        answer_1_image_width = screen_size[0] + 200
        
        
        # Question 2 medium
        question_2_raw_text = "What is the name of\nthe Actor who plays\nJoel in the games?"
        question_2_font_size = 130
        question_2_position = ("center", -440)
        question_2_timer_position = ('center')
        
        answer_2_raw_text = "Troy Baker"
        answer_2_font_size = 225
        answer_2_position = ("center", 500)
        answer_2_image_path = f"{topic}/Assets/Actors/Joel/Troy 2.jpeg"
        answer_2_image_helper = False
        answer_2_image_position = (0, 525)
        answer_2_image_width = screen_size[0]
        
        
        # Question 3 hard
        question_3_raw_text = "What is the name\nof Ellie's Mother?"
        question_3_font_size = 140
        question_3_position = ("center", -500)
        question_3_timer_position = ('center')
        
        answer_3_raw_text = "Anna"
        answer_3_font_size = 175
        answer_3_position = ("center", 500)
        answer_3_image_path = f"{topic}/Assets/Notes/Ellie\'s mum note cropped.jpeg"
        answer_3_image_helper = False
        answer_3_image_position = (0, 500)
        answer_3_image_width = screen_size[0]
        
        
        
        ''' Sections '''
        ''' Intro '''
        quick_raw_text = "Quick"
        quick_font_size = 300
        quick_colour = 'yellow'
        quick_kerning = 0
        quick_position = (0, -750)
        
        how_well_raw_text = "How Well Do\nYou Know"
        how_well_font_size = 175
        how_well_colour = 'cyan'
        how_well_kerning = 0
        how_well_interline = -10
        how_well_position = ('center', -450)
        
        # have each topic word on a new line or not
        topic_intro_one_word_per_line = False
        topic_intro_font_size = 200
        topic_intro_colour = 'white'
        topic_intro_kerning = 0
        topic_intro_interline = 0
        topic_intro_position = ("center", 10)
        
        three_questions_raw_text = "3 Questions"
        three_questions_font_size = 200
        three_questions_colour = 'orange'
        three_questions_kerning = 0
        three_questions_position = ("center", 425)
        
        seconds_raw_text = "3 Seconds"
        seconds_font_size = 200
        seconds_colour = 'orange'
        seconds_kerning = 0
        seconds_position = ("center", 625)
        
        
        
        ''' Questions'''
        question_title_font_size = 250
        question_title_colour = 'yellow'
        question_title_position = (0, -750)
        question_title_kerning = 0
        
        question_raw_text = 'Question'
        
        question_text_colour = 'cyan'
        question_text_kerning = 0
        question_text_interline = -10
        
        answer_colour = 'orange'
        answer_kerning = 0
        answer_interline = -10
        
        
        
        ''' Outro '''
        thanks_raw_text = "Thanks For\nPlaying"
        thanks_font_size = 250
        thanks_text_position = (0, -675)
        thanks_colour = 'yellow'
        thanks_kerning = 0
        thanks_interline = -10
        
        topic_outro_one_word_per_line = False
        topic_outro_position = ("center", -180)
        topic_outro_font_size = 200
        topic_outro_kerning = 0
        topic_outro_interline = 0
        topic_outro_colour = 'white'
        
        subscribe_raw_text = "Subscribe!"
        subscribe_font_size = 200
        subscribe_text_position = ("center", 220)
        subscribe_colour = 'white'
        subscribe_kerning = 0
        
        subscribe_box_position = ("center", 1050)
        subscribe_box_size = (700, 210)
        subscribe_box_colour = (255, 0, 0) # this has to be rgb instead of name
        
        comment_raw_text = "Comment Your\nScore Below"
        comment_font_size = 185
        comment_text_position = ("center", 550)
        comment_interline = 0
        comment_colour = 'orange'
        comment_kerning = 0
        
    elif topic == "Invincible":
            
        ''' Text '''
        ''' Fonts '''
        # Generic = "Arial-Rounded-MT-Bold"
        # AOT = "Cloister-Black-Light"
        
        # seperating these out because some fonts arnt easy to read but i still want them for the topic question and titles
        font_topic = "Wood-Block-CG" # the font for the topic eg (AOT)
        font_title = "Wood-Block-CG" # used for Question titles
        font_general_text = "Wood-Block-CG" # use for all other text
        
        
        ''' Text Borders '''
        text_border_width = 40
        text_border_colour = 'black'
        
        
        # have the debug frame be with the timer so i can make sure its not overlapping
        use_timer_frame = False
        
        
        
        #background
        background_image_path = f"{topic}/Assets/Characters/Invincible/Invincible 2.jpg"
        background_position = (-115, 0)
        use_background_width = False # either start with width or height
        
        # is use width use screen_size[0] else use screen_size[1]
        background_size = screen_size[1]
        

        # Question 1 easy
        question_1_raw_text = "What is Omni-Mans\nreal name?"
        question_1_font_size = 130
        question_1_position = ("center", -515)
        question_1_timer_position = ('center', 1250)
        
        answer_1_raw_text = "Nolan Grayson"
        answer_1_font_size = 175
        answer_1_position = ("center", 500)
        answer_1_image_path = f"{topic}/Assets/Characters/Nolan Grayson/Nolan 1.jpeg"
        answer_1_image_helper = False # if it is shown for the whole question or just the answer
        answer_1_image_position = (0, 500)
        answer_1_image_width = screen_size[0]
        
        
        # Question 2 medium
        question_2_raw_text = "What is the name of\nInvincibles Mother?"
        question_2_font_size = 130
        question_2_position = ("center", -515)
        question_2_timer_position = ('center', 1250)
        
        answer_2_raw_text = "Debbie Grayson"
        answer_2_font_size = 175
        answer_2_position = ("center", 500)
        answer_2_image_path = f"{topic}/Assets/Characters/Debbie Grayson/Debbie 2.jpeg"
        answer_2_image_helper = False
        answer_2_image_position = (-275, 500)
        answer_2_image_width = screen_size[0] + 550
        
        
        # Question 3 hard
        question_3_raw_text = "Name the alien race\nthat uses humans as\nthier hive mind host"
        question_3_font_size = 125
        question_3_position = ("center", -465)
        question_3_timer_position = ('center', 1250)
        
        answer_3_raw_text = "Sequids"
        answer_3_font_size = 200
        answer_3_position = ("center", 500)
        answer_3_image_path = f"{topic}/Assets/Characters/Sequids/Sequid 1.jpeg"
        answer_3_image_helper = False
        answer_3_image_position = (-100, 650)
        answer_3_image_width = screen_size[0] + 150
        
        
        
        ''' Sections '''
        ''' Intro '''
        quick_raw_text = "Quick"
        quick_font_size = 325
        quick_colour = 'yellow'
        quick_kerning = 0
        quick_position = (0, -750)
        
        how_well_raw_text = "How Well Do\nYou Know"
        how_well_font_size = 200
        how_well_colour = 'cyan'
        how_well_kerning = 0
        how_well_interline = 0
        how_well_position = ('center', -400)
        
        # have each topic word on a new line or not
        topic_intro_one_word_per_line = False
        topic_intro_font_size = 250
        topic_intro_colour = 'white'
        topic_intro_kerning = 0
        topic_intro_interline = 0
        topic_intro_position = ("center", 175)
        
        three_questions_raw_text = "3 Questions"
        three_questions_font_size = 225
        three_questions_colour = 'orange'
        three_questions_kerning = 0
        three_questions_position = ("center", 425)
        
        seconds_raw_text = "3 Seconds"
        seconds_font_size = 225
        seconds_colour = 'orange'
        seconds_kerning = 0
        seconds_position = ("center", 625)
        
        
        
        ''' Questions'''
        question_title_font_size = 250
        question_title_colour = 'yellow'
        question_title_position = (0, -750)
        question_title_kerning = 0
        
        question_raw_text = 'Question'
        
        question_text_colour = 'cyan'
        question_text_kerning = 0
        question_text_interline = -10
        
        answer_colour = 'orange'
        answer_kerning = 0
        answer_interline = -10
        
        
        
        ''' Outro '''
        thanks_raw_text = "Thanks For\nPlaying"
        thanks_font_size = 225
        thanks_text_position = (0, -675)
        thanks_colour = 'yellow'
        thanks_kerning = 0
        thanks_interline = -10
        
        topic_outro_one_word_per_line = False
        topic_outro_position = ("center", -325)
        topic_outro_font_size = 250
        topic_outro_kerning = 0
        topic_outro_interline = 0
        topic_outro_colour = 'white'
        
        subscribe_raw_text = "Subscribe!"
        subscribe_font_size = 200
        subscribe_text_position = ("center", 225)
        subscribe_colour = 'white'
        subscribe_kerning = 0
        
        subscribe_box_position = ("center", 1050)
        subscribe_box_size = (750, 225)
        subscribe_box_colour = (255, 0, 0) # this has to be rgb instead of name
        
        comment_raw_text = "Comment Your\nScore Below"
        comment_font_size = 185
        comment_text_position = ("center", 550)
        comment_interline = 0
        comment_colour = 'orange'
        comment_kerning = 0 




    