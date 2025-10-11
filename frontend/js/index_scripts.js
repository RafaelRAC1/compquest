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

let playerName = "";
let ws = null;
let currentQuestion = null;

function updateStatus(message, isLoading = false) {
    connectionStatus.innerHTML = `<p class="${isLoading ? 'loading' : ''}">${message}</p>`;
}
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
            headers: { "Content-Type": "application/json" },
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
            headers: { "Content-Type": "application/json" },
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

    const wsUrl = `ws://localhost:8000/compquest/ws/${sessionId}/${playerName}`;
    console.log("URL do WebSocket:", wsUrl);

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("WebSocket conectado com sucesso!");
        updateStatus("Conectado! Aguardando oponente...");
    };

    ws.onmessage = (event) => {
        console.log("Mensagem recebida:", event.data);
        const data = JSON.parse(event.data);

        if (data.event === "session_ready") {
            console.log("Sessão pronta:", data.session);
            updateStatus(`Jogo iniciado! Jogadores: ${data.session.players.join(", ")}`)

            lobbyForm.style.display = "none";
            gameArea.style.display = "flex";
        }

        if (data.event === "new_question") {
            console.log("Nova questão:", data.question);
            currentQuestion = data.question;
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

            status.textContent = "⚡ Seja o primeiro a responder!";
            status.style.color = "var(--success-color)";
        }

        if (data.event === "player_answered") {
            const buttons = answerButtons.querySelectorAll('.option-button');
            buttons.forEach(btn => btn.disabled = true);

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
            const resultMsg = data.correct ?
                `🎉 ${data.winner} escolheu "${data.answer_letter}) ${data.answer}" e acertou!\n\nResposta Correta: ${data.correct_answer}\n\nExplicação: ${data.explanation}` :
                `😔 ${data.winner} escolheu "${data.answer_letter}) ${data.answer}" e errou.\n\nResposta Correta: ${data.correct_answer}\n\nExplicação: ${data.explanation}`;

            let scoreText = "\n\nPlacar Atual:\n" + Object.entries(data.scores)
                .map(([p, s]) => `${p}: ${s} pontos`)
                .join("\n");

            const confirmed = confirm(resultMsg + scoreText + "\n\n🎯 Pressione OK para continuar para a próxima questão!");

            if (confirmed) {
                ws.send(JSON.stringify({ event: "ready_next" }));
                status.textContent = "⏳ Aguardando outro jogador confirmar...";
                status.style.color = "var(--accent-color)";
            }
        }

        if (data.event === "both_ready") {
            status.textContent = "✅ Ambos confirmaram! Próxima questão chegando...";
            status.style.color = "var(--success-color)";
        }

        if (data.event === "game_over") {
            let scores = data.final_scores;
            let maxScore = Math.max(...Object.values(scores));
            let winners = Object.keys(scores).filter(p => scores[p] === maxScore);
            let winner = winners.length > 1 ? "Empate!" : winners[0];

            let scoreText = Object.entries(scores)
                .map(([p, s]) => `${p}: ${s} pontos`)
                .join("\n");

            alert(`Fim de Jogo!\nPlacar Final:\n${scoreText}\n\nResultado: ${winner}`);

            gameArea.style.display = "none";
            lobbyForm.style.display = "flex";
            updateStatus("");
            inputName.value = "";
            ws = null;
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

startButton.addEventListener("click", startSession);
findButton.addEventListener("click", findSession);