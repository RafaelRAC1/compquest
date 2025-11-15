# CompQuest 🎮

**QUIZ BATTLE SOBRE COMPUTABILIDADE E COMPLEXIDADE 🤺**

CompQuest é um quiz battle multiplayer que transforma o aprendizado de conceitos de Ciência da Computação em uma experiência descontraída. Combinando elementos de RPG com storytelling, o jogo permite que os jogadores explorem os fundamentos da computabilidade e complexidade de algoritmos de forma gamificada.


## 🎯 OBJETIVOS

### Objetivo Principal
Ensinar conceitos de Ciência da Computação através de uma abordagem lúdica e interativa, tornando temas complexos acessíveis e interessantes para estudantes.

### Objetivos Específicos

**📚 Educacionais:**
- Ensinar conceitos de **Máquina de Turing** de forma visual e intuitiva
- Explicar a diferença entre classes de complexidade **P e NP** através de analogias práticas
- Apresentar **análise de complexidade de algoritmos** com exemplos do mundo real
- Ampliar o vocabulário técnico dos jogadores de forma natural e contextualizada

**🎮 Gamificação:**
- Criar uma experiência de aprendizado envolvente através de storytelling
- Implementar sistema de progressão que motiva o estudo contínuo
- Estabelecer competição saudável através do ranking multiplayer

**🧠 Pedagógicos:**
- Transformar conceitos abstratos em experiências memoráveis
- Promover aprendizado ativo através da prática e repetição gamificada
- Criar ambiente seguro para errar e aprender com feedback imediato

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** - Linguagem principal para desenvolvimento da API
- **FastAPI** - Framework web moderno e rápido para criação de APIs REST
- **WebSocket** - Comunicação em tempo real entre jogadores
- **SQLite** - Banco de dados relacional leve e baseado em arquivo
- **Uvicorn** - Servidor ASGI de alta performance

### Frontend
- **HTML5** - Estruturação das páginas e componentes
- **CSS3** - Estilização e design responsivo com animações
- **JavaScript (ES6+)** - Interatividade e comunicação com a API
- **WebSocket API** - Comunicação em tempo real com o backend
- **Fetch API** - Requisições HTTP para o backend

### Ferramentas de Desenvolvimento
- **Git & GitHub** - Controle de versão e colaboração
- **VS Code** - Editor de código recomendado
- **Postman / Swagger UI** - Testes de API durante desenvolvimento

### Deploy
- **Docker** - Containerização para deploy simplificado
- **Docker Compose** - Orquestração de containers

## 🎮 Funcionalidades Principais

### Sistema de Jogo
- **Batalha em Tempo Real**: Dois jogadores competem respondendo questões simultaneamente
- **Sistema de Pontuação Dinâmica**: Pontos variam conforme a dificuldade (Fácil: 100, Médio: 200, Difícil: 400)
- **Sistema de Sequência (Streak)**: Multiplicador de pontuação que aumenta com acertos consecutivos
  - 1 acerto: x1.0
  - 2 acertos: x1.1
  - 3 acertos: x1.2
  - ... até 10+ acertos: x2.0
- **Sistema de Penalidade**: Quando um jogador erra, o oponente recebe 20% dos pontos base da questão

### Poderes Especiais
- **🧠 Alan Turing**: Acerta automaticamente a questão atual, mas reseta a sequência e usa multiplicador x1.0 (uso único por partida)
- **💾 Pente de Memória**: Substitui a questão atual por outra de mesma dificuldade (uso único por partida)

### Interface e Experiência
- **Modais Informativos**: Substituição de `confirm()` e `alert()` por modais estilizados
- **Exibição de Sequências**: Mostra a sequência atual de cada jogador
- **Feedback Visual**: Animações e transições suaves
- **Ranking em Tempo Real**: Top 3 jogadores exibidos no menu principal

### Segurança e Confiabilidade
- **Autenticação por Token**: Todas as requisições requerem token Bearer
- **Tratamento de Desconexão**: Quando um jogador sai, o outro é notificado e redirecionado (sem salvar pontuação)
- **Validação de Respostas**: Apenas a primeira resposta válida é considerada

## 📁 Estrutura do Projeto

```
compquest/
├── README.md
├── .gitignore
│
├── backend/
│   ├── main.py                      # Ponto de entrada da API FastAPI
│   ├── requirements.txt             # Dependências Python
│   ├── compquest.db                 # Banco de dados SQLite
│   ├── check_database.py            # Script de verificação do banco
│   ├── check_sqlite.py              # Script de verificação SQLite
│   │
│   └── app/
│       ├── __init__.py
│       ├── database.py              # Gerenciador de banco de dados
│       ├── migrate_questions.py    # Migração de questões JSON → SQLite
│       │
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── health.py            # Rota /health
│       │   ├── launch.py            # Rotas de criação/entrada em sessões
│       │   ├── score.py             # Rotas de pontuação e ranking
│       │   └── websocket_routes.py  # WebSocket para jogo em tempo real
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── auth.py              # Autenticação por token
│       │   ├── game_logic.py        # Lógica principal do jogo
│       │   ├── session_manager.py   # Gerenciamento de sessões
│       │   ├── websocket_manager.py # Gerenciamento de WebSockets
│       │   ├── pick_questions.py    # Seleção de questões
│       │   └── Player.py             # Modelo de jogador
│       │
│       └── data/
│           ├── questions.json       # Banco de questões
│           └── old_questions.json   # Backup de questões antigas
│
└── frontend/
    ├── index.html                   # Página principal
    ├── css/
    │   └── index_style.css          # Estilos e animações
    └── js/
        └── index_scripts.js         # Lógica do frontend e WebSocket

```

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11 ou superior
- Git
- Navegador web moderno

### 1. Clonando o Repositório
```bash
git clone https://github.com/RafaelRAC1/compquest.git
cd compquest
```

### 2. Criar e Ativar Ambiente Virtual
```bash
# Navegar para a pasta do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
# Instalar dependências do projeto
pip install -r requirements.txt
```

### 4. Rodar o Serviço FastAPI
```bash
# Executar servidor FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Abrir o Jogo no Navegador

Com o servidor rodando, abra o arquivo `index.html` do frontend em **dois navegadores diferentes**:

**Caminho do arquivo:** `compquest/frontend/index.html`

**Abrir diretamente**
- Navegue até a pasta `frontend` e abra o arquivo `index.html` no navegador A
- Repita em outro navegador B, colando o link do navegador A

Depois acesse: `http://localhost:8080/index.html` em ambos os navegadores

### 6. Jogar uma Partida

1. **No primeiro navegador:**
   - Digite o nome do jogador (ex: "Jogador1")
   - Clique em **"Criar Sessão"**
   - Aguarde a mensagem de que a sessão foi criada

2. **No segundo navegador:**
   - Digite o nome do jogador (ex: "Jogador2")
   - Clique em **"Entrar em uma Sessão"**
   - O sistema encontrará automaticamente a sessão criada

3. **A partida começará automaticamente:**
   - Ambos os jogadores verão a primeira pergunta
   - Selecione uma das opções de resposta
   - O jogo continuará com as próximas perguntas (total de 10)

4. **Ao final da partida:**
   - Os jogadores serão informados sobre o vencedor e a pontuação final
   - Clique em **"Voltar ao Menu"** para iniciar uma nova partida

**Nota:** Para testar as rotas da API, acesse a documentação interativa do Swagger em `http://localhost:8000/docs`

---

## 📡 Principais Rotas da API

Todas as rotas estão prefixadas com `/compquest` e requerem autenticação via token Bearer.

### Tabela de Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/compquest/health` | Verifica status do servidor e estatísticas de sessões |
| POST | `/compquest/launch` | Cria uma nova sessão de jogo |
| POST | `/compquest/join-session/{session_id}` | Entra em uma sessão específica |
| POST | `/compquest/join-random-session` | Entra automaticamente em uma sessão disponível |
| GET | `/compquest/session/{session_id}` | Obtém informações de uma sessão |
| GET | `/compquest/sessions` | Lista todas as sessões ativas |
| POST | `/compquest/score` | Salva pontuação de um jogador |
| GET | `/compquest/score/{player_name}` | Obtém estatísticas de um jogador |
| GET | `/compquest/score` | Lista últimos 50 resultados |
| GET | `/compquest/top-players` | Obtém ranking dos melhores jogadores |
| WS | `/compquest/ws/{session_id}/{player_name}` | Conexão WebSocket para jogo em tempo real |

### 🔍 Rotas de Health e Status

#### `GET /compquest/health`
Verifica o status do servidor e estatísticas de sessões.

**Headers:**
```
Authorization: Bearer my_secret_token
```

**Resposta:**
```json
{
  "status": "Running!",
  "sessions": {
    "total_sessions": 0,
    "waiting_sessions": 0,
    "open_sessions": 0
  }
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

### 🎮 Rotas de Sessão e Jogo

#### `POST /compquest/launch`
Cria uma nova sessão de jogo para um jogador.

**Body (JSON):**
```json
{
  "name": "Jogador1"
}
```

**Resposta:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "message": "Session created, waiting for second player."
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `POST /compquest/join-session/{session_id}`
Permite que um segundo jogador entre em uma sessão existente.

**Parâmetros:**
- `session_id` (path) - ID da sessão retornado por `/launch`

**Body (JSON):**
```json
{
  "name": "Jogador2"
}
```

**Resposta (quando há 2 jogadores):**
```json
{
  "session_id": "abc123-def456-ghi789",
  "message": "Game ready!",
  "players": ["Jogador1", "Jogador2"]
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `POST /compquest/join-random-session`
Entra automaticamente em uma sessão aleatória disponível.

**Body (JSON):**
```json
{
  "name": "Jogador2"
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `GET /compquest/session/{session_id}`
Obtém informações sobre uma sessão específica.

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `GET /compquest/sessions`
Lista todas as sessões ativas.

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

### 📊 Rotas de Pontuação e Ranking

#### `POST /compquest/score`
Salva a pontuação de um jogador após uma partida.

**Body (JSON):**
```json
{
  "player_name": "Jogador1",
  "score": 1500,
  "won": true
}
```

**Resposta:**
```json
{
  "player_name": "Jogador1",
  "score": 1500,
  "won": true,
  "match_id": 1,
  "date": "2024-01-15 10:30:00"
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `GET /compquest/score/{player_name}`
Obtém estatísticas de um jogador específico.

**Resposta:**
```json
{
  "player_name": "Jogador1",
  "total_matches": 5,
  "total_score": 7500,
  "avg_score": 1500.0,
  "wins": 3,
  "best_score": 2000
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `GET /compquest/score`
Lista os últimos 50 resultados de partidas.

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

#### `GET /compquest/top-players?limit=3`
Obtém os melhores jogadores por pontuação máxima.

**Parâmetros de Query:**
- `limit` (opcional) - Número de jogadores a retornar (padrão: 3)

**Resposta:**
```json
{
  "top_players": [
    {
      "player_name": "Jogador1",
      "max_score": 2000
    },
    {
      "player_name": "Jogador2",
      "max_score": 1800
    }
  ]
}
```

**Teste no Swagger:** Acesse `http://localhost:8000/docs` e teste a rota diretamente na interface.

---

### 🔌 WebSocket - Comunicação em Tempo Real

#### `WS /compquest/ws/{session_id}/{player_name}`
Conexão WebSocket para comunicação em tempo real durante o jogo.

**Parâmetros:**
- `session_id` - ID da sessão
- `player_name` - Nome do jogador

**Autenticação:**
- Via cabeçalho: `Authorization: Bearer my_secret_token`
- Via query parameter: `?token=my_secret_token`

**Eventos Enviados pelo Cliente:**
```json
// Enviar resposta
{
  "event": "answer",
  "answer": "Opção A"
}

// Pronto para próxima questão
{
  "event": "ready_next"
}

// Usar poder do Alan Turing
{
  "event": "use_turing"
}

// Usar pente de troca
{
  "event": "use_memory_stick"
}
```

**Eventos Recebidos do Servidor:**
```json
// Nova questão
{
  "event": "new_question",
  "index": 1,
  "total": 10,
  "question": {
    "question": "Pergunta aqui...",
    "options": ["Opção A", "Opção B", "Opção C", "Opção D"],
    "oracle_hint": "Dica do oráculo"
  }
}

// Resultado da rodada
{
  "event": "round_result",
  "winner": "Jogador1",
  "correct_answer": "Opção A",
  "explanation": "Explicação da resposta"
}

// Sessão pronta
{
  "event": "session_ready",
  "session": { ... }
}
```

**Nota:** A conexão WebSocket é gerenciada automaticamente pelo frontend durante o jogo.

---

## 🔐 Variáveis de Ambiente, Tokens e Portas

### Porta do Servidor
- **Porta padrão:** `8000`
- **Host padrão:** `0.0.0.0` (quando executado com uvicorn) ou `127.0.0.1` (quando executado diretamente)
- **URL base:** `http://localhost:8000`

**Para alterar a porta:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Token de Autenticação
- **Token padrão:** `my_secret_token`
- **Localização:** `app/utils/auth.py` (variável `AUTH_TOKEN`)
- **Formato:** Bearer Token
- **Uso:** Todas as rotas REST e WebSocket requerem autenticação

**Como usar:**
```bash
# REST API
Authorization: Bearer my_secret_token

# WebSocket (query parameter)
ws://localhost:8000/compquest/ws/{session_id}/{player_name}?token=my_secret_token
```

### Banco de Dados
- **Tipo:** SQLite
- **Arquivo:** `compquest.db` (criado automaticamente na raiz do backend)
- **Localização:** Mesmo diretório onde o servidor é executado

**Estrutura do Banco:**
- `categoria` - Níveis de dificuldade (fácil, médio, difícil)
- `pergunta` - Questões do jogo
- `alternativa` - Opções de resposta
- `jogador` - Informações dos jogadores
- `partida` - Histórico de partidas
- `joga` - Relação jogador-partida com pontuação
- `contem` - Relação partida-pergunta

---

## 🧪 Testando as Rotas da API

Para testar todas as rotas da API, utilize a documentação interativa do Swagger:

1. **Acesse:** `http://localhost:8000/docs`
2. **Autenticação:** Clique no botão **"Authorize"** no topo da página
3. **Token:** Digite `my_secret_token` (sem o prefixo "Bearer")
4. **Teste as rotas:** Clique em qualquer rota, depois em **"Try it out"** e **"Execute"**

A documentação do Swagger permite testar todas as rotas diretamente no navegador, sem necessidade de ferramentas externas como Postman ou cURL.

---

## 🧪 Seção de Testes

A tabela abaixo documenta os testes realizados para validar as funcionalidades do sistema:

| Nº  | Funcionalidade           | Tipo de Teste  | Passos Realizados                          | Resultado Esperado                                                | Resultado Obtido                                                                 | Status |
|-----|--------------------------|----------------|---------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------|---------|
| 1   | Autenticação por token   | Funcional      | Enviar requisição sem token                 | Retornar 401 Unauthorized                                         | 401 retornado corretamente                                                       | ✅ Ok   |
| 2   | Autenticação por token   | Funcional      | Enviar requisição com token válido          | Permitir acesso e retornar dados                                  | Acesso concedido                                                                 | ✅ Ok   |
| 3   | Sistema de pontuação     | Funcional      | Jogador acerta 3 questões seguidas          | Multiplicador chega a x1.2                                        | Correto                                                                          | ✅ Ok   |
| 4   | Penalidade de erro       | Funcional      | Jogador erra após acerto                    | Perde streak de pontos; adversário ganha                          | Pontuação ajustada                                                               | ✅ Ok   |
| 5   | Uso do Alan Turing       | Exploratório   | Jogador usa Alan Turing                     | Questão é acertada automaticamente; streak reinicia               | Correto                                                                          | ✅ Ok   |
| 6   | Uso do Pente de Memória  | Funcional      | Jogador usa 1x durante partida              | Questão é trocada por outra de mesma dificuldade                  | Correto                                                                          | ✅ Ok   |
| 7   | Ranking                  | Funcional      | Inserir pontuação final dos jogadores       | Ranking atualizado corretamente no banco                          | Correto                                                                          | ✅ Ok   |
| 8   | Interface de batalha     | Exploratório   | Dois jogadores respondendo rápido           | Apenas o primeiro tem sua resposta validada                       | Correto                                                                          | ✅ Ok   |
| 9   | Fluxo completo de jogo   | Exploratório   | Jogar uma partida completa                  | Tudo funciona sem erro                                            | Se um jogador sair da partida, o outro não sabe → Corrigido. Jogador é informado que o outro saiu, e então é redirecionado para o menu. | ✅ Ok   |
| 10  | Saída durante Jogo       | Exploratório   | Sair de uma partida durante o jogo          | Dados do jogador não são registrados no banco de dados            | Correto                                                                          | ✅ Ok   |
| 12  | Pontuação                | Exploratório   | Jogador seleciona questão                   | Modal exibe informações da questão e alternativa correta          | Corrigido. Exibição de dados em `confirm` trocada por exibição em modal com UI padronizada. | ✅ Ok   |

## 👥 Integrantes do Grupo

- **Rafael Corrêa** - GitHub: [@RafaelRAC1](https://github.com/RafaelRAC1)
- **Rafael Calixto** - GitHub: [@Rafael Calixto](https://github.com/rafael-calixto1)
- **Nohan Brendon**

**Curso:** Ciência da Computação - 5º Semestre  
**Instituição:** Centro Universitário Braz Cubas  
**Disciplina:** Fundamentos de Computabilidade e Complexidade

---

**Desenvolvido com 💜 para descontrair o ensino de Ciência da Computação 🤪**