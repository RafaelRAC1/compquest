import random
from ..database import db_manager

def pick_questions():
    """Pick questions from database: 4 easy, 4 medium, 2 hard"""
    try:
        easy = db_manager.get_questions_by_difficulty("facil", 4)
        medium = db_manager.get_questions_by_difficulty("medio", 4)
        hard = db_manager.get_questions_by_difficulty("dificil", 2)
        
        print(f"Picked questions - Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")
        
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
        
        print(f"Total questions prepared: {len(questions)}")
        
        if len(questions) == 0:
            print("WARNING: No questions found in database! Check if questions are loaded.")
        
        return questions
    except Exception as e:
        print(f"ERROR in pick_questions: {e}")
        import traceback
        traceback.print_exc()
        return []
