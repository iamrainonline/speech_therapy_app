# pronunciation_checker.py
"""
Serviciu pentru verificarea pronunției
"""
from difflib import SequenceMatcher
from typing import List, Tuple
from config import AppConfig

class PronunciationChecker:
    """Verifică corectitudinea pronunției"""
    
    def __init__(self, similarity_threshold: float = AppConfig.SIMILARITY_THRESHOLD):
        self.threshold = similarity_threshold
    
    def check_pronunciation(self, target_word: str, spoken_text: str) -> Tuple[bool, float]:
        """
        Verifică dacă pronunția este corectă
        
        Args:
            target_word: Cuvântul țintă
            spoken_text: Textul recunoscut
            
        Returns:
            Tuple cu (este_corect, scor_similaritate)
        """
        if not spoken_text or spoken_text in ["TIMEOUT", "UNKNOWN", "ERROR"]:
            return False, 0.0
        
        target_lower = target_word.lower().strip()
        spoken_lower = spoken_text.lower().strip()
        
        # Verifică match exact
        if target_lower == spoken_lower:
            return True, 1.0
        
        # Verifică variații comune
        variations = self._generate_variations(target_lower)
        
        for variation in variations:
            if variation in spoken_lower or spoken_lower in variation:
                return True, 0.9
        
        # Calculează similaritatea
        similarity = SequenceMatcher(None, target_lower, spoken_lower).ratio()
        
        # Verifică similaritatea cu variațiile
        max_similarity = similarity
        for variation in variations:
            var_similarity = SequenceMatcher(None, variation, spoken_lower).ratio()
            max_similarity = max(max_similarity, var_similarity)
        
        is_correct = max_similarity >= self.threshold
        return is_correct, max_similarity
    
    def _generate_variations(self, word: str) -> List[str]:
        """Generează variații comune ale cuvântului"""
        variations = [word]
        
        # Variații pentru terminații feminine
        if word.endswith('ă'):
            variations.append(word[:-1] + 'a')
        if word.endswith('a'):
            variations.append(word[:-1] + 'ă')
        
        # Variații pentru plurale
        if word.endswith('i'):
            variations.append(word[:-1])
        if word.endswith('e'):
            variations.append(word[:-1])
        
        # Variații pentru accente
        accent_variations = {
            'â': 'a', 'î': 'i', 'ă': 'a', 'ș': 's', 'ț': 't'
        }
        
        for orig, repl in accent_variations.items():
            if orig in word:
                variations.append(word.replace(orig, repl))
        
        # Elimină duplicatele
        return list(set(variations))
    
    def get_feedback_message(self, target_word: str, spoken_text: str, is_correct: bool) -> str:
        """Generează mesajul de feedback"""
        if spoken_text == "TIMEOUT":
            return "Nu am auzit nimic. Încearcă din nou."
        elif spoken_text == "UNKNOWN":
            return "Nu am înțeles. Încearcă din nou."
        elif spoken_text == "ERROR":
            return "Eroare la recunoaștere. Încearcă din nou."
        elif is_correct:
            return "✅ Corect! Felicitări!"
        else:
            return f"❌ Ai spus: '{spoken_text}'. Încearcă din nou!"