# CompQuest 🎮

**QUIZ BATTLE SOBRE COMPUTABILIDADE E COMPLEXIDADE 🤺**

CompQuest é um quiz battle multiplayer que transforma o aprendizado de conceitos de Ciência da Computação em uma experiência descontraída. Combinando elementos de RPG com storytelling, o jogo permite que os jogadores explorem os fundamentos da computabilidade e complexidade de algoritmos de forma gamificada.

O projeto apresenta um sistema de ranking, mecânicas especiais como o Oráculo para explicações e a ajuda de Alan Turing, além de um sistema de pontuação baseado em streaks que incentiva o aprendizado contínuo.

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

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.11 ou superior
- Git
- Navegador web moderno

### Clonando o Repositório
```bash
git clone https://github.com/RafaelRAC1/compquest.git
cd compquest
```

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

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Testar se app está rodando (RETORNA 200 OK)
# [Colar URL no navegador ou Postman para HTTP GET]
http://localhost:8000/compquest/health
```

---

**Desenvolvido com para descontrair o ensino de Ciência da Computação 🤪**
