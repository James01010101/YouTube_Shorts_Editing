
from Make_Video_Globals import Globals

# this will make the txt files for the questions and answers so i can do audio on them
# now make the script files

settings = Globals.read_settings_file(Globals.topic, Globals.quiz_num)

quiz_folder = f"Topics/{Globals.topic}/{Globals.topic} Quiz {Globals.quiz_num}"


print("Making Intro Script Files")
with open(f"{quiz_folder}/Audio/Intro/Script/Quick.txt", "w") as file:
    file.write(f"[[rate 150]]\nQuick,\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Intro/Script/How_Well.txt", "w") as file:
    file.write(f"[[rate 200]]\nHow well do you know[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Intro/Script/Topic.txt", "w") as file:
    file.write(f"[[rate 200]]\n{settings['full_topic']}[[rate 0]]")

with open(f"{quiz_folder}/Audio/Intro/Script/Prove.txt", "w") as file:
    file.write(f"[[rate 200]]\nProve your knowledge[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Intro/Script/3_Questions.txt", "w") as file:
    file.write(f"[[rate 200]]\nand answer these 3 {settings['full_topic']} questions, of in-creasing difficulty\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Intro/Script/X_Seconds.txt", "w") as file:
    file.write(f"[[rate 200]]\nin less than {settings['question_silence_duration']} seconds?\n[[rate 0]]")
    
    
print("Making Question Script Files")
for question_number in range(1,4):
    with open(f"{quiz_folder}/Audio/Q{question_number}/Script/Title.txt", "w") as file:
        file.write(f"[[rate 200]]\nQuestion number {question_number} [[slnc 300]] \n")
        
        if question_number == 1:
            file.write("We’ll start off with an easy question.")
        elif question_number == 2:
            file.write("This next question will be medium difficulty.")
        elif question_number == 3:
            file.write("Finally, here is a hard difficulty question.")
            
        file.write("\n[[rate 0]]")
        
        
    with open(f"{quiz_folder}/Audio/Q{question_number}/Script/Question.txt", "w") as file:
        file.write(f"[[rate 200]]\n")
        
        if question_number == 1:
            file.write(settings['question_1_raw_text'])
        elif question_number == 2:
            file.write(settings['question_2_raw_text'])
        elif question_number == 3:
            file.write(settings['question_3_raw_text'])
            
        file.write("\n[[rate 0]]")
            
        
            
            
    with open(f"{quiz_folder}/Audio/Q{question_number}/Script/Answer.txt", "w") as file:
        file.write(f"[[rate 200]]\nThe correct answer, is ")
        
        if question_number == 1:
            file.write(settings['answer_1_raw_text'])
        elif question_number == 2:
            file.write(settings['answer_2_raw_text'])
        elif question_number == 3:
            file.write(settings['answer_3_raw_text'])
        
        file.write("\n[[rate 0]]")
            
    
    

print("Making Outro Script Files")
with open(f"{quiz_folder}/Audio/Outro/Script/Thanks.txt", "w") as file:
    file.write(f"[[rate 200]]\nThanks for playing my\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Outro/Script/Topic.txt", "w") as file:
    file.write(f"[[rate 200]]\n{settings['full_topic']} quiz.\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Outro/Script/Enjoy.txt", "w") as file:
    file.write(f"[[rate 200]]\nI hope you enjoyed it.\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Outro/Script/Comments.txt", "w") as file:
    file.write(f"[[rate 200]]\nLeave your score in the comments, and let me know if you got all 3 questions correct.\n[[rate 0]]")
    
with open(f"{quiz_folder}/Audio/Outro/Script/Subscribe.txt", "w") as file:
    file.write(f"[[rate 200]]\nmake sure to subscribe and check out my playlists for more {settings['full_topic']} quizzes and fun facts.\n[[rate 0]]")