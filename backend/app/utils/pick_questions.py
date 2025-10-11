import random
from ..database import db_manager

def pick_questions():
    """Pick questions from database: 4 easy, 4 medium, 2 hard"""
    easy = db_manager.get_questions_by_difficulty("facil", 4)
    medium = db_manager.get_questions_by_difficulty("medio", 4)
    hard = db_manager.get_questions_by_difficulty("dificil", 2)
    
    questions = []
    
    for q in easy + medium + hard:
        correct_answer = None
        options = []
        
        for option in q['options']:
            options.append(option['text'])
            if option['correct']:
                correct_answer = option['text']
        
        question_data = {
            "question": q['question'],
            "options": options,
            "answer": correct_answer,
            "oracle_hint": q['hint'],
            "explanation": q['explanation'],
            "id": q['id'] 
        }
        questions.append(question_data)
    
    return questions
