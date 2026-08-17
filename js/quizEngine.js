// quizEngine.js - Maneja la lógica de las preguntas y reglas del juego

class QuizEngine {
    constructor() {
        this.allQuestions = [];
        this.sessionQuestions = [];
        this.currentQuestionIndex = 0;

        // Estado del jugador
        this.lives = 3;
        this.score = 0;
        this.streak = 0;

        // Configuración de puntos
        this.basePoints = {
            "Fácil": 10,
            "Media": 20,
            "Difícil": 30
        };
    }

    async loadQuestions() {
        try {
            // Añadir un parámetro timestamp para evitar el caché del navegador y cargar el JSON más reciente
            const timestamp = new Date().getTime();
            const randomBuster = Math.random().toString(36).substring(7);
            const response = await fetch(`data/preguntas.json?t=${timestamp}&r=${randomBuster}`, { cache: "no-store" });
            this.allQuestions = await response.json();
            return true;
        } catch (error) {
            console.error("Error cargando las preguntas:", error);
            return false;
        }
    }

    startSession(moduloEduhome) {
        // Filtrar preguntas por el módulo seleccionado
        let filtered = this.allQuestions.filter(q => q.modulo_eduhome === moduloEduhome);

        if (filtered.length === 0) {
            return false;
        }

        let shuffled = this._shuffleArray(filtered);
        this.sessionQuestions = [];

        // Garantizar exactamente 7 preguntas
        if (shuffled.length >= 7) {
            this.sessionQuestions = shuffled.slice(0, 7);
        } else {
            // Si hay menos de 7, rellenar duplicando preguntas aleatoriamente
            this.sessionQuestions = [...shuffled];
            while (this.sessionQuestions.length < 7) {
                const randomQuestion = shuffled[Math.floor(Math.random() * shuffled.length)];
                // Clonar el objeto de la pregunta para evitar referencias cruzadas raras
                this.sessionQuestions.push({...randomQuestion});
            }
        }

        // Reiniciar estado
        this.currentQuestionIndex = 0;
        this.lives = 3;
        this.score = 0;
        this.streak = 0;

        return true;
    }

    getCurrentQuestion() {
        if (this.currentQuestionIndex < this.sessionQuestions.length) {
            let q = this.sessionQuestions[this.currentQuestionIndex];
            // Mezclar opciones
            q.shuffledOptions = this._shuffleArray([...q.opciones]);
            return q;
        }
        return null; // No hay más preguntas
    }

    checkAnswer(selectedOption) {
        const question = this.sessionQuestions[this.currentQuestionIndex];
        const isCorrect = (selectedOption === question.respuesta_correcta);

        let pointsEarned = 0;

        if (isCorrect) {
            this.streak++;
            let multiplier = this.getMultiplier();
            let base = this.basePoints[question.dificultad] || 10;
            pointsEarned = base * multiplier;
            this.score += pointsEarned;
        } else {
            this.streak = 0;
            this.lives--;
        }

        return {
            isCorrect,
            correctAnswer: question.respuesta_correcta,
            feedback: question.retroalimentacion,
            pointsEarned,
            livesRemaining: this.lives,
            streak: this.streak,
            multiplier: this.getMultiplier()
        };
    }

    nextQuestion() {
        this.currentQuestionIndex++;
        return this.getCurrentQuestion();
    }

    getMultiplier() {
        if (this.streak >= 5) return 3;
        if (this.streak >= 3) return 2;
        return 1;
    }

    isGameOver() {
        return this.lives <= 0 || this.currentQuestionIndex >= this.sessionQuestions.length;
    }

    getStats() {
        return {
            score: this.score,
            questionsAnswered: this.currentQuestionIndex,
            totalQuestions: this.sessionQuestions.length,
            won: this.lives > 0 && this.currentQuestionIndex >= this.sessionQuestions.length
        };
    }

    // Utilidad: Fisher-Yates Shuffle
    _shuffleArray(array) {
        let newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
    }
}
