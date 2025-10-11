import json
import os
from .database import db_manager

def migrate_questions():
    """Migrate questions from JSON to SQLite database"""
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'questions.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM alternativa")
        cursor.execute("DELETE FROM pergunta")
        cursor.execute("DELETE FROM categoria")
        
        categories = {
            'facil': 1,
            'medio': 2,
            'dificil': 3
        }
        
        for difficulty, cat_id in categories.items():
            cursor.execute("INSERT INTO categoria (id, dificuldade) VALUES (?, ?)", (cat_id, difficulty))
        
        difficulty_mapping = {
            'easy_questions': 'facil',
            'medium_questions': 'medio',
            'hard_questions': 'dificil'
        }
        
        for json_key, difficulty in difficulty_mapping.items():
            questions = questions_data.get(json_key, [])
            
            for question_data in questions:
                cursor.execute("""
                    INSERT INTO pergunta (nome, dica, explicacao, id_categoria)
                    VALUES (?, ?, ?, ?)
                """, (
                    question_data['question'],
                    question_data.get('oracle_hint', ''),
                    question_data.get('explanation', ''),
                    categories[difficulty]
                ))
                
                question_id = cursor.lastrowid
                
                # Insert alternatives
                correct_answer = question_data['answer']
                options = question_data['options']
                
                for i, option in enumerate(options):
                    letter = chr(ord('A') + i)
                    is_correct = 1 if option == correct_answer else 0
                    
                    cursor.execute("""
                        INSERT INTO alternativa (nome, letra, correta, id_pergunta)
                        VALUES (?, ?, ?, ?)
                    """, (option, letter, is_correct, question_id))
        
        conn.commit()
        print("Questions migrated successfully!")

if __name__ == "__main__":
    migrate_questions()
