#!/usr/bin/env python3
"""Script para verificar dados no banco"""

import requests
import json

def check_database():
    print("🔍 Verificando dados no banco de dados...")
    
    try:
        print("\n1. 📊 Todos os scores salvos:")
        response = requests.get("http://localhost:8000/compquest/score")
        if response.status_code == 200:
            data = response.json()
            scores = data.get('scores', [])
            if scores:
                for score in scores:
                    print(f"   Jogador: {score['player_name']}")
                    print(f"   Score: {score['score']} pontos")
                    print(f"   Venceu: {'Sim' if score['won'] else 'Não'}")
                    print(f"   Data: {score['date']}")
                    print(f"   Match ID: {score['match_id']}")
                    print("   " + "-" * 40)
            else:
                print("   Nenhum score encontrado ainda.")
        else:
            print(f"   Erro: {response.status_code}")
    
        for player in players:
            try:
                response = requests.get(f"http://localhost:8000/compquest/score/{player}")
                if response.status_code == 200:
                    stats = response.json()
                    print(f"   {player}:")
                    print(f"     Total de partidas: {stats['total_matches']}")
                    print(f"     Score total: {stats['total_score']}")
                    print(f"     Score médio: {stats['avg_score']}")
                    print(f"     Vitórias: {stats['wins']}")
                    print(f"     Melhor score: {stats['best_score']}")
                else:
                    print(f"   {player}: Não encontrado")
            except:
                print(f"   {player}: Erro ao buscar")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("Certifique-se de que o servidor está rodando!")

if __name__ == "__main__":
    check_database()
