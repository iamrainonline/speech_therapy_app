# models.py
"""
Modele de date pentru aplicația de terapie vocală
"""
from dataclasses import dataclass
from typing import List, Optional
import random

@dataclass
class WordCategory:
    """Model pentru o categorie de cuvinte"""
    name: str
    words: List[str]
    
    def get_random_words(self) -> List[str]:
        """Returnează lista de cuvinte amestecată"""
        shuffled = self.words.copy()
        random.shuffle(shuffled)
        return shuffled

@dataclass
class GameState:
    """Starea jocului"""
    current_category: str = "Animale"
    current_word: str = ""
    remaining_words: List[str] = None
    score: int = 0
    total_attempts: int = 0
    is_listening: bool = False
    
    def __post_init__(self):
        if self.remaining_words is None:
            self.remaining_words = []
    
    def reset_score(self):
        """Resetează scorul"""
        self.score = 0
        self.total_attempts = 0
    
    def add_attempt(self, correct: bool = False):
        """Adaugă o încercare"""
        self.total_attempts += 1
        if correct:
            self.score += 1
    
    def get_score_percentage(self) -> float:
        """Calculează procentajul de succes"""
        return (self.score / self.total_attempts * 100) if self.total_attempts > 0 else 0