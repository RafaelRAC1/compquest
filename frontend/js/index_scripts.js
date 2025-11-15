const startButton = document.getElementById("start-session");
const findButton = document.getElementById("find-session");
const inputName = document.getElementById("player-name");
const connectionStatus = document.getElementById("connection-status");

const lobbyForm = document.getElementById("lobby-form");
const gameArea = document.getElementById("game-area");
const questionText = document.getElementById("question-text");
const optionsDiv = document.getElementById("options");
const answerButtons = document.getElementById("answer-buttons");
const status = document.getElementById("status");
const scoreboardContainer = document.getElementById("scoreboard-container");
const menuHeader = document.querySelector(".menu-header");

const resultModal = document.getElementById("result-modal");
const modalTitle = document.getElementById("modal-title");
const modalMessage = document.getElementById("modal-message");
const modalScores = document.getElementById("modal-scores");
const modalStreaks = document.getElementById("modal-streaks");
const modalNextBtn = document.getElementById("modal-next-btn");

const AUTH_TOKEN = "my_secret_token";

let playerName = "";
let ws = null;
let currentQuestion = null;
let hasUsedTuring = false;
let hasUsedMemoryStick = false;

function updateStatus(message, isLoading = false) {
    connectionStatus.innerHTML = `<p class="${isLoading ? 'loading' : ''}">${message}</p>`;
}

function showModal(title, message, scores, streaks, isGameOver = false) {
    modalTitle.textContent = title;
    modalMessage.innerHTML = message;
    
    if (scores && Object.keys(scores).length > 0) {
        modalScores.innerHTML = '<h3><i class="fas fa-trophy"></i> Placar</h3>';
        Object.entries(scores).forEach(([player, score]) => {
            const scoreItem = document.createElement('div');
            scoreItem.className = 'modal-score-item';
            scoreItem.innerHTML = `
                <span class="player-name">${player}</span>
                <span class="player-score">${score} pontos</span>
            `;
            modalScores.appendChild(scoreItem);
        });
        modalScores.style.display = 'block';
    } else {
        modalScores.style.display = 'none';
    }
    
    if (streaks && Object.keys(streaks).length > 0) {
        modalStreaks.innerHTML = '<h3><i class="fas fa-fire"></i> Sequências</h3>';
        Object.entries(streaks).forEach(([player, streak]) => {
            const streakItem = document.createElement('div');
            streakItem.className = 'modal-streak-item';
            streakItem.innerHTML = `
                <span class="player-name">${player}</span>
                <span class="player-streak">${streak} ${streak === 1 ? 'acerto' : 'acertos'}</span>
            `;
            modalStreaks.appendChild(streakItem);
        });
        modalStreaks.style.display = 'block';
    } else {
        modalStreaks.style.display = 'none';
    }
    
    if (isGameOver) {
        modalNextBtn.textContent = 'Fechar';
    } else {
        modalNextBtn.textContent = 'Próxima';
    }
    
    resultModal.classList.add('show');
}

function hideModal() {
    resultModal.classList.remove('show');
}

function redirectToMenu() {
    if (ws) {
        ws.close();
        ws = null;
    }
    
    gameArea.style.display = "none";
    lobbyForm.style.display = "flex";
    if (scoreboardContainer) scoreboardContainer.style.display = "block";
    if (menuHeader) menuHeader.style.display = "block";
    updateStatus("");
    inputName.value = "";
    currentQuestion = null;
    hasUsedTuring = false;
    hasUsedMemoryStick = false;
    
    modalButtonHandler = () => {
        hideModal();
        if (modalNextBtn.textContent === 'Próxima' && ws) {
            ws.send(JSON.stringify({ event: "ready_next" }));
            status.textContent = "⏳ Aguardando outro jogador confirmar...";
            status.style.color = "var(--accent-color)";
        }
    };
}

let modalButtonHandler = () => {
    hideModal();
    
    if (modalNextBtn.textContent === 'Próxima' && ws) {
        ws.send(JSON.stringify({ event: "ready_next" }));
        status.textContent = "⏳ Aguardando outro jogador confirmar...";
        status.style.color = "var(--accent-color)";
    }
};

modalNextBtn.addEventListener('click', () => {
    modalButtonHandler();
});

resultModal.addEventListener('click', (e) => {
    if (e.target === resultModal) {
        modalButtonHandler();
    }
});
async function startSession() {
    playerName = inputName.value.trim();
    if (!playerName) {
        updateStatus("Por favor, digite seu apelido!");
        return;
    }

    try {
        updateStatus("Criando sessão...", true);
        console.log("Enviando requisição para criar sessão...");

        const res = await fetch("http://localhost:8000/compquest/launch", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${AUTH_TOKEN}`
            },
            body: JSON.stringify({ name: playerName })
        });

        console.log("Status da resposta:", res.status);

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log("Dados recebidos:", data);

        updateStatus("Sessão criada! Aguardando outro jogador...");
        connectWS(data.session_id);
    } catch (error) {
        console.error("Erro ao criar sessão:", error);
        updateStatus("Erro ao criar sessão. Verifique se o servidor está rodando.");
    }
}

async function findSession() {
    playerName = inputName.value.trim();
    if (!playerName) {
        updateStatus("Por favor, digite seu apelido!");
        return;
    }

    try {
        updateStatus("Procurando sessão disponível...", true);
        console.log("Enviando requisição para entrar em sessão...");

        const res = await fetch("http://localhost:8000/compquest/join-random-session", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${AUTH_TOKEN}`
            },
            body: JSON.stringify({ name: playerName })
        });

        console.log("Status da resposta:", res.status);

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log("Dados recebidos:", data);

        updateStatus("Entrando na sessão...");
        connectWS(data.session_id);
    } catch (error) {
        console.error("Erro ao entrar em sessão:", error);
        if (error.message.includes("No available sessions")) {
            updateStatus("Nenhuma sessão disponível. Crie uma nova!");
        } else {
            updateStatus("Erro ao entrar em sessão. Verifique se o servidor está rodando.");
        }
    }
}

function connectWS(sessionId) {
    console.log(`Conectando WebSocket para sessão: ${sessionId}, jogador: ${playerName}`);
    updateStatus("Conectando...", true);

    const wsUrl = `ws://localhost:8000/compquest/ws/${sessionId}/${playerName}?token=${AUTH_TOKEN}`;
    console.log("URL do WebSocket:", wsUrl);

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("WebSocket conectado com sucesso!");
        updateStatus("Conectado! Aguardando oponente...");
    };

    ws.onmessage = (event) => {
        console.log("Mensagem recebida:", event.data);
        const data = JSON.parse(event.data);

        if (data.error && !data.event) {
            console.error("Erro de autenticação:", data.error);
            updateStatus(`Erro: ${data.error}`);
            ws.close();
            return;
        }

        if (data.event === "session_ready") {
            console.log("Sessão pronta:", data.session);
            updateStatus(`Jogo iniciado! Jogadores: ${data.session.players.join(", ")}`)

            lobbyForm.style.display = "none";
            gameArea.style.display = "flex";
            if (scoreboardContainer) scoreboardContainer.style.display = "none";
            if (menuHeader) menuHeader.style.display = "none";
            
            if (data.session.has_used_turing && data.session.has_used_turing[playerName]) {
                hasUsedTuring = true;
            } else {
                hasUsedTuring = false;
            }
            
            if (data.session.has_used_memory_stick && data.session.has_used_memory_stick[playerName]) {
                hasUsedMemoryStick = true;
            } else {
                hasUsedMemoryStick = false;
            }
        }

        if (data.event === "new_question") {
            console.log("Nova questão:", data.question);
            currentQuestion = data.question;
            
            lobbyForm.style.display = "none";
            gameArea.style.display = "flex";
            if (scoreboardContainer) scoreboardContainer.style.display = "none";
            if (menuHeader) menuHeader.style.display = "none";
            
            questionText.textContent = `Questão ${data.index || ''}: ${currentQuestion.question}`;

            optionsDiv.innerHTML = `<p><strong><i class="fas fa-lightbulb"></i> Dica do Oráculo:</strong> ${currentQuestion.oracle_hint || 'Pense bem antes de responder!'}</p>`;

            answerButtons.innerHTML = "";

            currentQuestion.options.forEach((option, index) => {
                const letter = String.fromCharCode(65 + index); 

                const button = document.createElement('button');
                button.className = 'option-button';
                button.innerHTML = `<strong>${letter})</strong> ${option}`;
                button.onclick = () => submitAnswer(letter);
                answerButtons.appendChild(button);
            });

            if (!hasUsedTuring) {
                const turingButton = document.createElement('button');
                turingButton.id = 'turing-button';
                turingButton.className = 'option-button turing-button';
                turingButton.innerHTML = '🧠 Usar Alan Turing';
                turingButton.onclick = () => useTuring();
                answerButtons.appendChild(turingButton);
            }
            
            if (!hasUsedMemoryStick) {
                const memoryStickButton = document.createElement('button');
                memoryStickButton.id = 'memory-stick-button';
                memoryStickButton.className = 'option-button memory-stick-button';
                memoryStickButton.innerHTML = '💾 Usar Pente de Troca';
                memoryStickButton.onclick = () => useMemoryStick();
                answerButtons.appendChild(memoryStickButton);
            }

            if (data.memory_stick_used) {
                status.textContent = "💾 Nova questão carregada! Seja o primeiro a responder!";
            } else {
                status.textContent = "⚡ Seja o primeiro a responder!";
            }
            status.style.color = "var(--success-color)";
        }

        if (data.event === "player_answered") {
            const buttons = answerButtons.querySelectorAll('.option-button');
            buttons.forEach(btn => btn.disabled = true);
            
            if (data.used_turing && data.player === playerName) {
                hasUsedTuring = true;
                const turingBtn = document.getElementById('turing-button');
                if (turingBtn) {
                    turingBtn.remove();
                }
            }

            if (data.player === playerName) {
                status.textContent = "✅ Você respondeu primeiro! Aguardando resultado...";
                status.style.color = "var(--primary-color)";
            } else {
                status.textContent = `❌ ${data.player} respondeu primeiro! Você perdeu esta rodada.`;
                status.style.color = "var(--error-color)";
            }
        }

        if (data.event === "round_result") {
            const isWinner = data.winner === playerName;
            const resultEmoji = data.correct ? "🎉" : "😔";
            const resultText = data.correct ? "acertou" : "errou";
            
            let message = `${resultEmoji} <strong>${data.winner}</strong> escolheu "<strong>${data.answer_letter}) ${data.answer}</strong>" e ${resultText}!<br><br>`;
            message += `<strong>Resposta Correta:</strong> ${data.correct_answer}<br><br>`;
            if (data.explanation) {
                message += `<strong>Explicação:</strong> ${data.explanation}`;
            }
            
            if (data.used_turing) {
                message += `<br><br><em>🧠 Alan Turing foi usado (sequência resetada)</em>`;
            }
            
            showModal("Resultado da Rodada", message, data.scores, data.streaks, false);
        }

        if (data.event === "both_ready") {
            status.textContent = "✅ Ambos confirmaram! Próxima questão chegando...";
            status.style.color = "var(--success-color)";
        }

        if (data.event === "player_disconnected") {
            let message = `<strong>⚠️ Oponente Desconectado</strong><br><br>`;
            message += `${data.disconnected_player || "O oponente"} saiu da partida.<br><br>`;
            message += `Você será redirecionado para o menu em alguns segundos...`;
            
            modalScores.style.display = 'none';
            modalStreaks.style.display = 'none';
            
            modalButtonHandler = () => {
                hideModal();
                redirectToMenu();
            };
            
            modalNextBtn.textContent = 'Voltar ao Menu';
            showModal("Partida Encerrada", message, null, null, false);
            
            setTimeout(() => {
                if (resultModal.classList.contains('show')) {
                    hideModal();
                    redirectToMenu();
                }
            }, 5000);
        }

        if (data.event === "game_over") {
            let scores = data.final_scores;
            let maxScore = Math.max(...Object.values(scores));
            let winners = Object.keys(scores).filter(p => scores[p] === maxScore);
            let winner = winners.length > 1 ? "Empate!" : winners[0];
            
            let message = `<strong>Fim de Jogo!</strong><br><br>`;
            message += `<strong>Resultado:</strong> ${winner}`;
            
            modalButtonHandler = () => {
                hideModal();
                redirectToMenu();
                loadScoreboard();
            };
            
            showModal("Fim de Jogo", message, scores, data.final_streaks, true);
        }
        
        if (data.event === "memory_stick_used") {
            status.textContent = data.message || "💾 Pente de Memória ativado! Carregando uma nova questão...";
            status.style.color = "var(--accent-color)";
            
            if (data.player === playerName) {
                hasUsedMemoryStick = true;
                const memoryStickBtn = document.getElementById('memory-stick-button');
                if (memoryStickBtn) {
                    memoryStickBtn.remove(); 
                }
            }
        }
        
        if (data.event === "memory_stick_failed") {
            status.textContent = data.message || "Não foi possível substituir a questão.";
            status.style.color = "var(--error-color)";
        }
        
        
        if (data.event === "round_result" && data.used_turing) {
            const turingMsg = data.winner === playerName ? 
                "🧠 Você usou Alan Turing e acertou!" : 
                `🧠 ${data.winner} usou Alan Turing e acertou!`;
            console.log(turingMsg);
        }
    };

    ws.onerror = (event) => {
        console.error("Erro no WebSocket:", event);
        updateStatus("Erro de conexão! Verifique se o servidor está rodando.");
    };

    ws.onclose = (event) => {
        console.log("WebSocket fechado:", event);
        updateStatus("Conexão perdida!");
    };
}

function submitAnswer(selectedOption) {
    if (!currentQuestion) return;

    console.log("Enviando resposta:", selectedOption);
    ws.send(JSON.stringify({ event: "answer", answer: selectedOption }));

    const buttons = answerButtons.querySelectorAll('.option-button');
    buttons.forEach(btn => btn.disabled = true);

    status.textContent = "🚀 Enviando resposta...";
    status.style.color = "var(--accent-color)";
}

function useTuring() {
    if (!currentQuestion || hasUsedTuring) return;

    console.log("Usando Alan Turing");
    ws.send(JSON.stringify({ event: "use_turing" }));

    const buttons = answerButtons.querySelectorAll('.option-button');
    buttons.forEach(btn => btn.disabled = true);

    status.textContent = "🧠 Usando Alan Turing...";
    status.style.color = "var(--accent-color)";
}

function useMemoryStick() {
    if (!currentQuestion || hasUsedMemoryStick) return;

    console.log("Usando Pente de Memória");
    ws.send(JSON.stringify({ event: "use_memory_stick" }));

    const buttons = answerButtons.querySelectorAll('.option-button');
    buttons.forEach(btn => btn.disabled = true);

    status.textContent = "💾 Pente de Memória ativado! Carregando uma nova questão...";
    status.style.color = "var(--accent-color)";
}

document.addEventListener("keypress", (e) => {
    if (!currentQuestion) return;
    const key = e.key.toUpperCase();
    if (['A', 'B', 'C', 'D'].includes(key)) {
        const buttons = answerButtons.querySelectorAll('.option-button');
        const targetButton = Array.from(buttons).find(btn => btn.innerHTML.startsWith(`<strong>${key})`));
        if (targetButton && !targetButton.disabled) {
            submitAnswer(key);
        }
    }
});

async function loadScoreboard() {
    const scoreboard = document.getElementById("scoreboard");
    scoreboard.innerHTML = '<div class="scoreboard-loading">Carregando...</div>';
    
    try {
        const res = await fetch("http://localhost:8000/compquest/top-players?limit=3", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${AUTH_TOKEN}`
            }
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        const topPlayers = data.top_players || [];
        
        if (topPlayers.length === 0) {
            scoreboard.innerHTML = '<div class="scoreboard-empty">Nenhum jogador ainda</div>';
            return;
        }
        
        scoreboard.innerHTML = "";
        
        topPlayers.forEach((player, index) => {
            const rank = index + 1;
            const item = document.createElement("div");
            item.className = `scoreboard-item rank-${rank}`;
            
            const rankDiv = document.createElement("div");
            rankDiv.className = "scoreboard-rank";
            rankDiv.textContent = `#${rank}`;
            
            const playerDiv = document.createElement("div");
            playerDiv.className = "scoreboard-player";
            playerDiv.textContent = player.player_name;
            
            const scoreDiv = document.createElement("div");
            scoreDiv.className = "scoreboard-score";
            scoreDiv.textContent = `${player.max_score} pts`;
            
            item.appendChild(rankDiv);
            item.appendChild(playerDiv);
            item.appendChild(scoreDiv);
            scoreboard.appendChild(item);
        });
    } catch (error) {
        console.error("Erro ao carregar scoreboard:", error);
        scoreboard.innerHTML = '<div class="scoreboard-empty">Erro ao carregar</div>';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadScoreboard();
});

startButton.addEventListener("click", startSession);
findButton.addEventListener("click", findSession);