import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str = "compquest.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com todas as tabelas e restrições"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Habilita chaves estrangeiras
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            # Cria tabela categoria
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dificuldade VARCHAR(10) NOT NULL UNIQUE,
                    CHECK (dificuldade IN ('facil', 'medio', 'dificil'))
                )
            """)
            
            # Cria tabela pergunta
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pergunta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    dica TEXT,
                    explicacao TEXT,
                    id_categoria INTEGER NOT NULL,
                    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
                )
            """)
            
            # Cria tabela alternativa
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alternativa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    letra VARCHAR(1) NOT NULL,
                    correta INTEGER NOT NULL DEFAULT 0,
                    id_pergunta INTEGER NOT NULL,
                    FOREIGN KEY (id_pergunta) REFERENCES pergunta(id),
                    CHECK (letra IN ('A', 'B', 'C', 'D')),
                    CHECK (correta IN (0, 1))
                )
            """)
            
            # Cria tabela jogador
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(50) NOT NULL UNIQUE
                )
            """)
            
            # Cria tabela partida
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS partida (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Cria tabela joga (entidade associativa)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS joga (
                    id_jogador INTEGER NOT NULL,
                    id_partida INTEGER NOT NULL,
                    score INTEGER NOT NULL DEFAULT 0,
                    venceu INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (id_jogador, id_partida),
                    FOREIGN KEY (id_jogador) REFERENCES jogador(id),
                    FOREIGN KEY (id_partida) REFERENCES partida(id),
                    CHECK (venceu IN (0, 1)),
                    CHECK (score >= 0)
                )
            """)
            
            # Cria tabela contem (entidade associativa)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contem (
                    id_partida INTEGER NOT NULL,
                    id_pergunta INTEGER NOT NULL,
                    PRIMARY KEY (id_partida, id_pergunta),
                    FOREIGN KEY (id_partida) REFERENCES partida(id),
                    FOREIGN KEY (id_pergunta) REFERENCES pergunta(id)
                )
            """)
            
            # Cria índices
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pergunta_categoria ON pergunta(id_categoria)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alternativa_pergunta ON alternativa(id_pergunta)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_joga_jogador ON joga(id_jogador)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_joga_partida ON joga(id_partida)")
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Gerenciador de contexto para conexões com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def get_or_create_player(self, player_name: str) -> int:
        """Obtém ID do jogador ou cria se não existir"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tenta obter jogador existente
            cursor.execute("SELECT id FROM jogador WHERE nome = ?", (player_name,))
            result = cursor.fetchone()
            
            if result:
                return result['id']
            
            # Cria novo jogador
            cursor.execute("INSERT INTO jogador (nome) VALUES (?)", (player_name,))
            conn.commit()
            return cursor.lastrowid
    
    def create_match(self) -> int:
        """Cria uma nova partida e retorna seu ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO partida (data) VALUES (CURRENT_TIMESTAMP)")
            conn.commit()
            return cursor.lastrowid
    
    def save_match_result(self, match_id: int, player_id: int, score: int, won: bool = False):
        """Salva resultado do jogador para uma partida"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO joga (id_jogador, id_partida, score, venceu)
                VALUES (?, ?, ?, ?)
            """, (player_id, match_id, score, 1 if won else 0))
            conn.commit()
    
    def add_questions_to_match(self, match_id: int, question_ids: List[int]):
        """Adiciona questões usadas em uma partida"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for question_id in question_ids:
                cursor.execute("""
                    INSERT OR IGNORE INTO contem (id_partida, id_pergunta)
                    VALUES (?, ?)
                """, (match_id, question_id))
            conn.commit()
    
    def get_questions_by_difficulty(self, difficulty: str, limit: int = None) -> List[Dict[str, Any]]:
        """Obtém questões por nível de dificuldade"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT p.id, p.nome, p.dica, p.explicacao, c.dificuldade
                FROM pergunta p
                JOIN categoria c ON p.id_categoria = c.id
                WHERE c.dificuldade = ?
                ORDER BY RANDOM()
            """
            
            if limit:
                query += " LIMIT ?"
                cursor.execute(query, (difficulty, limit))
            else:
                cursor.execute(query, (difficulty,))
            
            questions = []
            for row in cursor.fetchall():
                # Obtém alternativas para esta questão
                cursor.execute("""
                    SELECT nome, letra, correta
                    FROM alternativa
                    WHERE id_pergunta = ?
                    ORDER BY letra
                """, (row['id'],))
                
                alternatives = []
                for alt_row in cursor.fetchall():
                    alternatives.append({
                        'text': alt_row['nome'],
                        'letter': alt_row['letra'],
                        'correct': bool(alt_row['correta'])
                    })
                
                questions.append({
                    'id': row['id'],
                    'question': row['nome'],
                    'hint': row['dica'] or '',
                    'explanation': row['explicacao'] or '',
                    'difficulty': row['dificuldade'],
                    'options': alternatives
                })
            
            return questions
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """Obtém todas as questões com suas alternativas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.id, p.nome, p.dica, p.explicacao, c.dificuldade
                FROM pergunta p
                JOIN categoria c ON p.id_categoria = c.id
                ORDER BY c.dificuldade, p.id
            """)
            
            questions = []
            for row in cursor.fetchall():
                # Obtém alternativas para esta questão
                cursor.execute("""
                    SELECT nome, letra, correta
                    FROM alternativa
                    WHERE id_pergunta = ?
                    ORDER BY letra
                """, (row['id'],))
                
                alternatives = []
                for alt_row in cursor.fetchall():
                    alternatives.append({
                        'text': alt_row['nome'],
                        'letter': alt_row['letra'],
                        'correct': bool(alt_row['correta'])
                    })
                
                questions.append({
                    'id': row['id'],
                    'question': row['nome'],
                    'hint': row['dica'] or '',
                    'explanation': row['explicacao'] or '',
                    'difficulty': row['dificuldade'],
                    'options': alternatives
                })
            
            return questions
    
    def get_player_stats(self, player_name: str) -> Dict[str, Any]:
        """Obtém estatísticas do jogador"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Obtém ID do jogador
            player_id = self.get_or_create_player(player_name)
            
            # Obtém estatísticas de partidas
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_matches,
                    SUM(score) as total_score,
                    AVG(score) as avg_score,
                    SUM(venceu) as wins,
                    MAX(score) as best_score
                FROM joga
                WHERE id_jogador = ?
            """, (player_id,))
            
            stats = cursor.fetchone()
            
            return {
                'player_name': player_name,
                'total_matches': stats['total_matches'] or 0,
                'total_score': stats['total_score'] or 0,
                'avg_score': round(stats['avg_score'] or 0, 2),
                'wins': stats['wins'] or 0,
                'best_score': stats['best_score'] or 0
            }
    
    def has_questions(self) -> bool:
        """Verifica se o banco de dados possui questões"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM pergunta")
            result = cursor.fetchone()
            return result['count'] > 0 if result else False
    
    def get_top_players(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Obtém os melhores jogadores por pontuação máxima"""
        with self.get_connection() as conn:
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
            
            players = []
            for row in cursor.fetchall():
                players.append({
                    'player_name': row['nome'],
                    'max_score': row['max_score'] or 0
                })
            
            return players

# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()
