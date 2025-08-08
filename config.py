# config.py
"""
Configurări și constante pentru aplicația de terapie vocală
"""
from dataclasses import dataclass
from enum import Enum

@dataclass
class AppConfig:
    """Configurări aplicație"""
    WINDOW_SIZE = "800x600"
    WINDOW_TITLE = "Aplicație Exerciții Pronunție"
    SPEECH_RATE = 150
    SIMILARITY_THRESHOLD = 0.7
    LISTEN_TIMEOUT = 5
    PHRASE_TIME_LIMIT = 3
    BLINK_COUNT = 3
    BLINK_DURATION = 0.2
    SUCCESS_DISPLAY_TIME = 1500

class Colors:
    """Constante pentru culori"""
    BACKGROUND = "#f0f0f0"
    WHITE = "#ffffff"
    SUCCESS_BG = "#90EE90"
    SUCCESS_FG = "#006400"
    ERROR_BG = "#ffcccb"
    BUTTON_PRIMARY = "#2196F3"
    BUTTON_SUCCESS = "#4CAF50"
    BUTTON_WARNING = "#FF9800"
    BUTTON_SECONDARY = "#9C27B0"
    BUTTON_DANGER = "#f44336"
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"

class FeedbackType(Enum):
    """Tipuri de feedback vizual"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    NEUTRAL = "neutral"
    LISTENING = "listening"

class UIText:
    """Texte folosite în interfață"""
    TITLE = "Exerciții de Pronunție"
    CATEGORY_LABEL = "Categorie:"
    SCORE_FORMAT = "Scor: {score}/{total}"
    LISTEN_BUTTON = "🔊 Ascultă cuvântul"
    MIC_BUTTON = "🎤 Vorbește"
    MIC_LISTENING = "🔴 Ascult..."
    SKIP_BUTTON = "⏭ Sari peste"
    RESTART_BUTTON = "🔄 Restart categorie"
    STATUS_DEFAULT = "Apasă pe microfon și pronunță cuvântul"
    STATUS_LISTENING = "Vorbește acum..."
    STATUS_CORRECT = "✅ Corect! Felicitări!"
    STATUS_INCORRECT = "❌ Ai spus: '{text}'. Încearcă din nou!"
    STATUS_NO_SOUND = "Nu am auzit nimic. Încearcă din nou."
    STATUS_NOT_UNDERSTOOD = "Nu am înțeles. Încearcă din nou."
    STATUS_SELECT_CATEGORY = "Alege o categorie pentru a începe"
    COMPLETION_MESSAGE = "Felicitări! Ai terminat categoria '{category}'!\n\nScor final: {score}/{total} ({percentage:.1f}%)"
    COMPLETION_TITLE = "Categoria completă"
    COMPLETION_QUESTION = "\n\nVrei să începi din nou această categorie?"