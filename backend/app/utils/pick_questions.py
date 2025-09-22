import random, json

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    questions_json = json.load(f)

def pick_questions():
    easy = random.sample(questions_json["easy_questions"], 4)
    medium = random.sample(questions_json["medium_questions"], 4)
    hard = random.sample(questions_json["hard_questions"], 2)
    return easy + medium + hard
