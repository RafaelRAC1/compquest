#!/usr/bin/env python3
"""Script para verificar dados diretamente no SQLite"""

import sqlite3
from datetime import datetime

def check_sqlite_database():
    print("🗄️ Verificando dados diretamente no SQLite...")
    
    try:
        conn = sqlite3.connect('compquest.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n👥 JOGADORES:")
        cursor.execute("SELECT * FROM jogador")
        players = cursor.fetchall()
        for player in players:
            print(f"   ID: {player['id']}, Nome: {player['nome']}")
        
        print("\n🎮 PARTIDAS:")
        cursor.execute("SELECT * FROM partida ORDER BY data DESC")
        matches = cursor.fetchall()
        for match in matches:
            print(f"   ID: {match['id']}, Data: {match['data']}")
        
        print("\n🏆 SCORES:")
        cursor.execute("""
            SELECT j.nome, j.score, j.venceu, p.data, p.id as match_id
            FROM joga j
            JOIN jogador j ON j.id_jogador = j.id
            JOIN partida p ON j.id_partida = p.id
            ORDER BY p.data DESC
        """)
        scores = cursor.fetchall()
        for score in scores:
            print(f"   Jogador: {score['nome']}")
            print(f"   Score: {score['score']} pontos")
            print(f"   Venceu: {'Sim' if score['venceu'] else 'Não'}")
            print(f"   Data: {score['data']}")
            print(f"   Match ID: {score['match_id']}")
            print("   " + "-" * 40)
        
        print("\n❓ PERGUNTAS USADAS:")
        cursor.execute("""
            SELECT p.id as match_id, p.data, COUNT(c.id_pergunta) as num_questions
            FROM partida p
            LEFT JOIN contem c ON p.id = c.id_partida
            GROUP BY p.id, p.data
            ORDER BY p.data DESC
        """)
        match_questions = cursor.fetchall()
        for mq in match_questions:
            print(f"   Match {mq['match_id']} ({mq['data']}): {mq['num_questions']} perguntas")
        
        print("\n📈 ESTATÍSTICAS GERAIS:")
        cursor.execute("SELECT COUNT(*) as total_jogadores FROM jogador")
        total_players = cursor.fetchone()['total_jogadores']
        
        cursor.execute("SELECT COUNT(*) as total_partidas FROM partida")
        total_matches = cursor.fetchone()['total_partidas']
        
        cursor.execute("SELECT SUM(score) as total_score FROM joga")
        total_score = cursor.fetchone()['total_score'] or 0
        
        print(f"   Total de jogadores: {total_players}")
        print(f"   Total de partidas: {total_matches}")
        print(f"   Score total acumulado: {total_score}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def top_players(limit=5):
    """Top X jogadores por maior score registrado"""
    print(f"\n🏆 TOP {limit} JOGADORES (MAIOR SCORE):")
    print("=" * 50)
    print(f"{'RANK':<5} {'JOGADOR':<20} {'MAIOR SCORE':<15}")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('compquest.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                jg.nome,
                MAX(j.score) as max_score
            FROM joga j
            JOIN jogador jg ON j.id_jogador = jg.id
            GROUP BY j.id_jogador, jg.nome
            ORDER BY max_score DESC
            LIMIT ?
        """, (limit,))
        
        players = cursor.fetchall()
        for i, player in enumerate(players, 1):
            print(f"{i:<5} {player['nome']:<20} {player['max_score']:<15}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def match_by_id(match_id):
    """Buscar resultado da partida por ID"""
    print(f"\n🎮 PARTIDA ID: {match_id}")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('compquest.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM partida WHERE id = ?", (match_id,))
        match = cursor.fetchone()
        
        if not match:
            print("❌ Partida não encontrada!")
            return
            
        print(f"Data: {match['data']}")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                jg.nome,
                j.score,
                j.venceu
            FROM joga j
            JOIN jogador jg ON j.id_jogador = jg.id
            WHERE j.id_partida = ?
            ORDER BY j.score DESC
        """, (match_id,))
        
        players = cursor.fetchall()
        print(f"{'JOGADOR':<20} {'SCORE':<10} {'VENCEU':<10}")
        print("-" * 40)
        
        for player in players:
            won = "SIM" if player['venceu'] else "NÃO"
            print(f"{player['nome']:<20} {player['score']:<10} {won:<10}")
        
        cursor.execute("""
            SELECT COUNT(*) as num_questions
            FROM contem
            WHERE id_partida = ?
        """, (match_id,))
        
        num_questions = cursor.fetchone()['num_questions']
        print(f"\nPerguntas usadas: {num_questions}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def last_match():
    """Informações da última partida"""
    print("\n🕐 ÚLTIMA PARTIDA:")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('compquest.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.id, p.data
            FROM partida p
            ORDER BY p.data DESC
            LIMIT 1
        """)
        
        last_match = cursor.fetchone()
        
        if not last_match:
            print("❌ Nenhuma partida encontrada!")
            return
            
        print(f"ID: {last_match['id']}")
        print(f"Data: {last_match['data']}")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                jg.nome,
                j.score,
                j.venceu
            FROM joga j
            JOIN jogador jg ON j.id_jogador = jg.id
            WHERE j.id_partida = ?
            ORDER BY j.score DESC
        """, (last_match['id'],))
        
        players = cursor.fetchall()
        print(f"{'JOGADOR':<20} {'SCORE':<10} {'VENCEU':<10}")
        print("-" * 40)
        
        for player in players:
            won = "SIM" if player['venceu'] else "NÃO"
            print(f"{player['nome']:<20} {player['score']:<10} {won:<10}")
        
        cursor.execute("""
            SELECT COUNT(*) as num_questions
            FROM contem
            WHERE id_partida = ?
        """, (last_match['id'],))
        
        num_questions = cursor.fetchone()['num_questions']
        print(f"\nPerguntas usadas: {num_questions}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def match_questions(match_id):
    """Mostrar perguntas utilizadas em uma partida específica"""
    print(f"\n❓ PERGUNTAS DA PARTIDA ID: {match_id}")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect('compquest.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, data FROM partida WHERE id = ?", (match_id,))
        match = cursor.fetchone()
        
        if not match:
            print("❌ Partida não encontrada!")
            return
            
        print(f"Data da partida: {match['data']}")
        print("-" * 80)
        
        cursor.execute("""
            SELECT 
                p.id as pergunta_id,
                p.nome as pergunta,
                p.dica,
                c.dificuldade,
                COUNT(a.id) as num_alternativas
            FROM contem c
            JOIN pergunta p ON c.id_pergunta = p.id
            JOIN categoria cat ON p.id_categoria = cat.id
            LEFT JOIN alternativa a ON p.id = a.id_pergunta
            WHERE c.id_partida = ?
            GROUP BY p.id, p.nome, p.dica, c.dificuldade
            ORDER BY c.dificuldade, p.id
        """, (match_id,))
        
        questions = cursor.fetchall()
        
        if not questions:
            print("❌ Nenhuma pergunta encontrada para esta partida!")
            return
            
        print(f"{'ID':<5} {'DIFICULDADE':<10} {'PERGUNTA':<50} {'ALTERNATIVAS':<12}")
        print("-" * 80)
        
        for q in questions:
            pergunta_short = q['pergunta'][:47] + "..." if len(q['pergunta']) > 50 else q['pergunta']
            print(f"{q['pergunta_id']:<5} {q['dificuldade']:<10} {pergunta_short:<50} {q['num_alternativas']:<12}")
        
        print("-" * 80)
        print(f"Total de perguntas: {len(questions)}")
        
        if questions:
            print(f"\n📝 DETALHES DA PRIMEIRA PERGUNTA (ID: {questions[0]['pergunta_id']}):")
            print(f"Pergunta: {questions[0]['pergunta']}")
            print(f"Dica: {questions[0]['dica']}")
            print(f"Dificuldade: {questions[0]['dificuldade']}")
            
            cursor.execute("""
                SELECT letra, nome, correta
                FROM alternativa
                WHERE id_pergunta = ?
                ORDER BY letra
            """, (questions[0]['pergunta_id'],))
            
            alternatives = cursor.fetchall()
            print("Alternativas:")
            for alt in alternatives:
                correct = "✓" if alt['correta'] else " "
                print(f"  {alt['letra']}) {alt['nome']} {correct}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def reset_database():
    """Zerar base de dados mantendo apenas as perguntas"""
    print("🗑️ ZERANDO BASE DE DADOS (mantendo perguntas)...")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('compquest.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM jogador")
        players_before = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM partida")
        matches_before = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM joga")
        scores_before = cursor.fetchone()[0]
        
        print(f"ANTES DA LIMPEZA:")
        print(f"  Jogadores: {players_before}")
        print(f"  Partidas: {matches_before}")
        print(f"  Scores: {scores_before}")
        print("-" * 40)
        
        cursor.execute("DELETE FROM contem")  
        cursor.execute("DELETE FROM joga")    
        cursor.execute("DELETE FROM partida")
        cursor.execute("DELETE FROM jogador") 
        
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('jogador', 'partida')")
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM jogador")
        players_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM partida")
        matches_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM joga")
        scores_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pergunta")
        questions_count = cursor.fetchone()[0]
        
        print(f"APÓS A LIMPEZA:")
        print(f"  Jogadores: {players_after}")
        print(f"  Partidas: {matches_after}")
        print(f"  Scores: {scores_after}")
        print(f"  Perguntas: {questions_count} (mantidas)")
        print("-" * 40)
        print("✅ Base de dados zerada com sucesso!")
        print("✅ Perguntas mantidas intactas!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "top":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            top_players(limit)
        elif command == "match":
            if len(sys.argv) > 2:
                match_id = int(sys.argv[2])
                match_by_id(match_id)
            else:
                print("❌ Uso: python check_sqlite.py match <id>")
        elif command == "last":
            last_match()
        elif command == "questions":
            if len(sys.argv) > 2:
                match_id = int(sys.argv[2])
                match_questions(match_id)
            else:
                print("❌ Uso: python check_sqlite.py questions <match_id>")
        elif command == "reset":
            reset_database()
        else:
            print("❌ Comandos disponíveis: top, match, last, questions, reset")
    else:
        check_sqlite_database()
