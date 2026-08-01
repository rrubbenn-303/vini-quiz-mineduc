// app.js - Maneja la interacción del DOM y el flujo de la UI

const engine = new QuizEngine();

// Referencias DOM
const screens = {
    start: document.getElementById('start-screen'),
    game: document.getElementById('game-screen'),
    end: document.getElementById('end-screen')
};

const moduleSelect = document.getElementById('module-select');
const startBtn = document.getElementById('start-btn');

// HUD
const livesDisplay = document.getElementById('lives-display');
const scoreDisplay = document.getElementById('score-display');
const streakDisplay = document.getElementById('streak-display');
const multiplierDisplay = document.getElementById('multiplier-display');
const currentModuleDisplay = document.getElementById('current-module-display');
const progressDisplay = document.getElementById('progress-display');

// Preguntas
const difficultyBadge = document.getElementById('difficulty-badge');
const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');

// Feedback
const feedbackModal = document.getElementById('feedback-modal');
const feedbackTitle = document.getElementById('feedback-title');
const feedbackText = document.getElementById('feedback-text');
const nextQuestionBtn = document.getElementById('next-question-btn');

// Fin
const endTitle = document.getElementById('end-title');
const finalScore = document.getElementById('final-score');
const finalStreak = document.getElementById('final-streak');
const endMessage = document.getElementById('end-message');
const restartBtn = document.getElementById('restart-btn');

let currentHighestStreak = 0;

// Inicialización
document.addEventListener('DOMContentLoaded', async () => {
    const loaded = await engine.loadQuestions();
    if (!loaded) {
        alert("Error al cargar la base de datos de preguntas.");
    }
});

// Habilitar botón de inicio cuando se selecciona un módulo
moduleSelect.addEventListener('change', () => {
    if (moduleSelect.value) {
        startBtn.disabled = false;
    }
});

// Iniciar Juego
startBtn.addEventListener('click', () => {
    // Inicializar audio context si estaba suspendido (política de navegadores)
    if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    const selectedModule = moduleSelect.value;
    const hasQuestions = engine.startSession(selectedModule);

    if (!hasQuestions) {
        alert("¡Ups! Todavía no hay preguntas para esta misión. Elige otra.");
        return;
    }

    SoundEffects.startMission();
    currentHighestStreak = 0;
    currentModuleDisplay.textContent = selectedModule;
    updateHUD();
    renderQuestion();

    showScreen('game');
});

// Renderizar pregunta actual
function renderQuestion() {
    const q = engine.getCurrentQuestion();
    if (!q) {
        endGame();
        return;
    }

    // Limpiar UI
    optionsContainer.innerHTML = '';

    // Configurar textos
    difficultyBadge.textContent = q.dificultad;
    questionText.textContent = q.pregunta;

    // Colores de dificultad
    if(q.dificultad === "Fácil") difficultyBadge.style.backgroundColor = "var(--neon-green)";
    if(q.dificultad === "Media") difficultyBadge.style.backgroundColor = "var(--neon-yellow)";
    if(q.dificultad === "Difícil") difficultyBadge.style.backgroundColor = "var(--neon-pink)";

    difficultyBadge.style.color = q.dificultad === "Media" ? "var(--space-dark)" : "white";

    // Crear botones
    q.shuffledOptions.forEach(opt => {
        const btn = document.createElement('button');
        btn.classList.add('option-btn');
        btn.textContent = opt;
        btn.onclick = () => handleAnswer(opt, btn);
        optionsContainer.appendChild(btn);
    });
}

// Manejar respuesta
function handleAnswer(selectedOption, btnElement) {
    // Deshabilitar todos los botones para evitar múltiples clics
    const allBtns = document.querySelectorAll('.option-btn');
    allBtns.forEach(b => b.disabled = true);

    const result = engine.checkAnswer(selectedOption);

    if (result.streak > currentHighestStreak) {
        currentHighestStreak = result.streak;
    }

    if (result.isCorrect) {
        btnElement.classList.add('correct');
        SoundEffects.correctAnswer();
        showFeedback(true, `¡Ganaste ${result.pointsEarned} puntos!\n${result.feedback}`);
    } else {
        btnElement.classList.add('wrong');
        SoundEffects.wrongAnswer();
        // Resaltar la correcta
        allBtns.forEach(b => {
            if(b.textContent === result.correctAnswer) b.classList.add('correct');
        });
        showFeedback(false, `La respuesta correcta era: ${result.correctAnswer}.\n${result.feedback}`);
    }

    updateHUD();
}

// Actualizar marcadores
function updateHUD() {
    livesDisplay.textContent = engine.lives;
    scoreDisplay.textContent = engine.score;
    streakDisplay.textContent = engine.streak;
    multiplierDisplay.textContent = engine.getMultiplier();

    const stats = engine.getStats();
    let currentQ = stats.questionsAnswered + 1;
    if (currentQ > stats.totalQuestions) currentQ = stats.totalQuestions;
    progressDisplay.textContent = `Pregunta ${currentQ} / ${stats.totalQuestions}`;
}

// Mostrar Feedback
function showFeedback(isCorrect, text) {
    setTimeout(() => {
        feedbackModal.classList.remove('hidden');
        feedbackTitle.textContent = isCorrect ? "¡EXCELENTE! 🚀" : "¡CUIDADO! 💥";
        feedbackTitle.className = isCorrect ? 'success' : 'error';
        feedbackText.textContent = text;

        // Si ya perdió, cambiar el botón
        if (engine.lives <= 0) {
            nextQuestionBtn.textContent = "Ver Resultados";
        } else {
            nextQuestionBtn.textContent = "Siguiente Pregunta ➡️";
        }
    }, 800); // Pequeño delay para ver la animación del botón
}

// Botón de Siguiente Pregunta / Fin
nextQuestionBtn.addEventListener('click', () => {
    feedbackModal.classList.add('hidden');

    if (engine.isGameOver()) {
        endGame();
    } else {
        engine.nextQuestion();
        renderQuestion();
    }
});

// Pantalla final
function endGame() {
    showScreen('end');
    const stats = engine.getStats();

    finalScore.textContent = stats.score;
    finalStreak.textContent = currentHighestStreak;

    if (stats.won) {
        SoundEffects.victory();
        endTitle.textContent = "¡MISIÓN COMPLETADA! 🏆";
        endTitle.style.color = "var(--neon-green)";
        endMessage.textContent = "¡Eres un explorador espacial increíble!";
    } else {
        SoundEffects.gameOver();
        endTitle.textContent = "¡NAVE DESTRUIDA! 💥";
        endTitle.style.color = "var(--neon-pink)";
        endMessage.textContent = "No te rindas, vuelve a intentarlo.";
    }
}

// Reiniciar
restartBtn.addEventListener('click', () => {
    // Resetear UI
    moduleSelect.value = "";
    startBtn.disabled = true;
    showScreen('start');
});

// Utilidad para cambiar pantallas
function showScreen(screenName) {
    Object.values(screens).forEach(s => {
        s.classList.remove('active');
        s.classList.add('hidden');
    });
    screens[screenName].classList.remove('hidden');
    screens[screenName].classList.add('active');
}
