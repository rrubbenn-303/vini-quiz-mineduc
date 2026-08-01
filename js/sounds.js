// sounds.js - Web Audio API para generar efectos de sonido retro sin archivos externos

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

const SoundEffects = {
    playTone: function(frequency, type, duration, vol) {
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }

        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();

        oscillator.type = type;
        oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);

        // Envolvente de volumen (Fade out)
        gainNode.gain.setValueAtTime(vol, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);

        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        oscillator.start();
        oscillator.stop(audioCtx.currentTime + duration);
    },

    startMission: function() {
        // Arpegio ascendente
        setTimeout(() => this.playTone(300, 'square', 0.1, 0.1), 0);
        setTimeout(() => this.playTone(400, 'square', 0.1, 0.1), 100);
        setTimeout(() => this.playTone(500, 'square', 0.2, 0.1), 200);
        setTimeout(() => this.playTone(600, 'square', 0.3, 0.1), 300);
    },

    correctAnswer: function() {
        // Sonido de moneda/acierto
        this.playTone(800, 'sine', 0.1, 0.1);
        setTimeout(() => this.playTone(1200, 'sine', 0.3, 0.1), 100);
    },

    wrongAnswer: function() {
        // Sonido de error/golpe
        this.playTone(150, 'sawtooth', 0.2, 0.1);
        setTimeout(() => this.playTone(100, 'sawtooth', 0.4, 0.1), 150);
    },

    victory: function() {
        // Fanfarria corta
        const notes = [440, 440, 440, 587, 440, 587];
        const times = [0, 150, 300, 450, 750, 900];

        notes.forEach((freq, index) => {
            setTimeout(() => this.playTone(freq, 'square', 0.2, 0.1), times[index]);
        });
    },

    gameOver: function() {
        // Tonos descendentes tristes
        this.playTone(300, 'triangle', 0.4, 0.1);
        setTimeout(() => this.playTone(250, 'triangle', 0.4, 0.1), 300);
        setTimeout(() => this.playTone(200, 'triangle', 0.4, 0.1), 600);
        setTimeout(() => this.playTone(150, 'triangle', 0.8, 0.1), 900);
    }
};
