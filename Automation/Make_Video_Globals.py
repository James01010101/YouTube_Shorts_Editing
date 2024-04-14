
import json

class Globals:
    topic = "JJK"
    quiz_num = "1"
    

    def read_settings_file(topic, quiz_num):
        with open(f"Topics/{topic}/{topic} Quiz {quiz_num}/settings.json", "r") as file:
            return json.load(file)  




    