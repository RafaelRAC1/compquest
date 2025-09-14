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
- **SQLite** - Banco de dados relacional leve e baseado em arquivo

### Frontend
- **HTML5** - Estruturação das páginas e componentes
- **CSS3** - Estilização e design responsivo
- **JavaScript** - Interatividade e comunicação com a API
- **Fetch API** - Requisições HTTP para o backend

### Ferramentas de Desenvolvimento
- **Git & GitHub** - Controle de versão e colaboração
- **VS Code** - Editor de código recomendado
- **Postman** - Testes de API durante desenvolvimento

### Deploy
- **Docker** - Containerização para deploy simplificado
- **Docker Compose** - Orquestração de containers

## 📁 Estrutura Inicial do Projeto

```
CompQuest/
├── README.md
├── .gitignore
│
├── backend/
│   ├── main.py              # Ponto de entrada da API FastAPI
│   ├── requirements.txt     # Dependências Python
│   │
│   └── app/
│       ├── routes/
│       │   ├── health.py    # Rota /health (obrigatória)
│       │   ├── launch.py    # Rota /launch (obrigatória)
│       │   └── score.py     # Rota /score (obrigatória)
│       │
│       ├── models/          # Modelos do banco de dados
│       ├── services/        # Lógica de negócio
│       └── data/            # Banco SQLite e perguntas
│
└── frontend/
    ├── index.html
    └── assets/
        ├── css/
        ├── js/
        └── images/

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
### Configurando o Backend
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
# Navegar para a pasta do backend
cd backend

# Executar servidor FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Testar Endpoint /health

**Método 1 - Navegador:**
```
http://localhost:8000/compquest/health
```

**Método 2 - Terminal (curl):**
```bash
curl -X GET http://localhost:8000/compquest/health
```

**Método 3 - Postman:**
- Método: GET
- URL: `http://localhost:8000/compquest/health`

### Resposta Esperada
```json
{
  "message": "ok",
}
```

**Status Code:** `200 OK`

## 👥 Integrantes do Grupo

- **Rafael Corrêa** - GitHub: [@RafaelRAC1](https://github.com/RafaelRAC1)
- **Rafael Calixto** - GitHub: [@Rafael Calixto](https://github.com/rafael-calixto1)
- **Nohan Brendon**

**Curso:** Ciência da Computação - 5º Semestre  
**Instituição:** Centro Universitário Braz Cubas  
**Disciplina:** Fundamentos de Computabilidade e Complexidade

---

**Desenvolvido com 💜 para descontrair o ensino de Ciência da Computação 🤪**
