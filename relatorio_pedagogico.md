# Relatório Pedagógico do Plugin Gamificado

## 1. Identificação do Plugin
**Nome do jogo/plugin:** CompQuest

**Área da disciplina (Fundamentos, Análise de Algoritmos, Técnicas, Modelos Computacionais):** Computabilidade e Complexidade de Algoritmos 

**Grupo (nomes e RAs dos integrantes):**  
- Nohan Brendon Torresson Gomes (35120827)  
- Rafael Calixto de Oliveira (35293659)  
- Rafael Reis dos Anjos Corrêa (36142581)

---

## 2. Objetivo Pedagógico
O CompQuest é um quiz battle multilpayer que apresenta, intuitivamente, conceitos sobre computabilidade e complexidade de algoritmos. Através da gamificação, o aluno é apresentado a conceitos fundamentais de P, NP, NP-C e máquina de turing, enquanto participa de um ambiente competitivo saudável. O jogo, que ocorre entre dois jogadores, intende garantir ao aluno o aprendizado através da participação de partidas contínuas, apresentando sempre perguntas dentro do tema. É previsto que o jogador revisite perguntas entre partidas, estimulando o aprendizado contínuo.

---

## 3. Descrição do Jogo
O requisito primordial para funcionamento do jogo é a presença de, no mínimo, dois jogadores. Após os jogadores informarem seus apelidos, nos respectivos navegadores, devem iniciar e procurar uma sessão. Com isso, serão alocados em uma partida composta por 10 perguntas, sendo 4 fáceis (100 pts.), 4 médias (200 pts.) e 2 difíceis (400 pts.), nessa sequência. Cada pergunta é acompanhada do enunciado, uma dica/explicação e alternativas em uma tela intuitiva do navegador. Ao selecionar uma alternativa, um modal informa aos jogadores sobre o porquê de determinada alternativa ser a correta, e eles avançam para a próxima questão. Errar concede 20% dos pontos da questão ao oponente. Acertar em sequência garante mais pontos por questão. Vence aquele que tiver maior pontuação. A duração média é entre 4-6 minutos. 

---

## 4. Conteúdo Relacionado à Disciplina
O CompQuest reúne os principais conceitos da disciplina, apresentando cada tema de forma objetiva e aplicada ao contexto do jogo.

- **Máquina de Turing e Decidibilidade**  
  - Questões sobre o funcionamento básico da MT e exemplos de problemas decidíveis e indecidíveis.
  
- **Classes de Complexidade (P, NP, NP-Completo)**  
  - Perguntas que destacam diferenças entre as classes e usam problemas clássicos como referência.

- **Notação Assintótica (Big-O)**  
  - Itens que pedem identificação e comparação das ordens de complexidade.

O formato de quiz contribui diretamente para a compreensão desses conteúdos ao combinar repetição, variação de exemplos e feedback imediato, permitindo que o aluno perceba relações entre os temas e reconheça padrões de forma mais natural. A dinâmica rápida das partidas incentiva revisões constantes, enquanto o contexto do jogo torna conceitos abstratos mais acessíveis e menos formais, facilitando a assimilação mesmo de tópicos tradicionalmente considerados difíceis.

---

## 5. Critérios de Pontuação
A pontuação do jogador é calculada com base na quantidade de acertos por nível de dificuldade, sequência de acertos e erros do adversário. Cada questão tem um peso: fácil (100 pts.); média (200 pts.); e difícil (400 pts.). A cada questão acertada em sequência, o percentual de pontuação aumenta em 0,1. Ou seja, ao acertar 3 questões seguidas, a questão valerá 1.3x pontos – ex.: uma questão fácil de 100 pontos valerá 130 pontos. Caso erre ou use máquina de turing, perderá a sequência (volta para 1,0x). A pontuação final dos jogadores é entregue após a última pergunta (10ª). Não há tempo limite ou uma pontuação mínima para aprovação, vence o jogador com maior pontuação, ou empate. O jogo penaliza erros, para evitar chutes. Errar fornecerá 20% dos pontos da questão ao adversário, e o jogador perderá sua sequência de acertos (1,0x).  

---

## 6. Testes Realizados

### **Teste 1 — Acerto Total e Streak Máximo**
**Objetivo:** Garantir cálculo correto de pontuação com acertos consecutivos.  
**Cenário:** Jogador acerta as 10 questões seguidas.  
**Resultado Esperado:** Multiplicadores aplicados progressivamente, streak final = 10, pontuação = 3.220 pontos.  
**Status:** PASSOU  

### **Teste 2 — Erro e Penalidade**
**Objetivo:** Verificar reset de streak e bonificação do oponente após erro.  
**Cenário:** Jogador A erra uma questão difícil enquanto B participa.  
**Resultado Esperado:** Streak de A resetado (1.0x); B recebe 20% do ponto base da questão (80 pts).  
**Status:** PASSOU  

### **Teste 3 — Saída no Meio da Partida**
**Objetivo:** Validar tratamento quando um jogador sai no meio da partida.  
**Cenário:** Após 3 questões, Jogador A fecha o jogo/fecha conexão; Jogador B permanece.  
**Resultado Esperado:** Sistema envia notificação a B, e é redirecionado para o menu, pontuação não é registrada para partida incompleta, sessão é encerrada/removida.  
**Status:** PASSOU  

### **Teste 4 — Poderes Especiais**
**Objetivo:** Confirmar uso único e limitações dos poderes.  
**Cenário:** Jogadores tentam usar Alan Turing e Pente de Memória mais de uma vez.  
**Resultado Esperado:** Cada poder só pode ser usado uma vez por partida; botões desaparecem após jogador utilizar.  
**Status:** PASSOU  

### **Teste 5 — Empate e Persistência**
**Objetivo:** Validar empates e salvamento correto no banco.  
**Cenário:** Dois jogadores terminam com mesma pontuação final.  
**Resultado Esperado:** Empate registrado, ambas pontuações salvas no banco.  
**Status:** PASSOU  

---

## 7. Roteiro de Demonstração
A apresentação se baseará em dois cenários centrais.

No **primeiro cenário, caminho feliz**, dois jogadores participarão do quiz battle normalmente. Os jogadores utilizarão suas habilidades normalmente, e terão suas sequências funcionando normalmente, com acréscimos de pontuação conforme aumenta. Ao final, um jogador será apresentado como vencedor, com dados persistidos no banco de dados, e eles retornarão para o menu principal.

No **segundo cenário, caminho de erro**, os dois jogadores participarão do quiz battle normalmente, selecionando as alternativas, obtendo pontuações e utilizando suas habilidades. No entanto, durante a 5ª questão, um dos jogadores reiniciará a página para simular que houve uma desconexão. Isso deve interromper o fluxo convencional do jogo, levando o outro jogador a ser informado e voltar ao menu.
