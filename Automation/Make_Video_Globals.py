
import json

class Globals:
    topic = "Fortnite"
    full_topic = "Fortnite"
    quiz_num = "4"
    

    def read_settings_file(topic, quiz_num):
        with open(f"Topics/{topic}/{topic} Quiz {quiz_num}/settings.json", "r") as file:
            return json.load(file)  




    