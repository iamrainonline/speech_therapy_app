# game_controller.py
"""
Controller pentru logica jocului
"""
import threading
from typing import Optional, Callable
from models import GameState
from word_manager import WordCategoryManager
from audio_services import CombinedAudioService
from pronunciation_checker import PronunciationChecker
from config import AppConfig, UIText

class GameController:
    """Controller principal pentru logica jocului"""
    
    def __init__(self):
        self.state = GameState()
        self.word_manager = WordCategoryManager()
        self.audio_service = CombinedAudioService()
        self.pronunciation_checker = PronunciationChecker()
        
        # Callbacks pentru UI
        self.on_word_changed: Optional[Callable[[str], None]] = None
        self.on_score_changed: Optional[Callable[[int, int], None]] = None
        self.on_status_changed: Optional[Callable[[str], None]] = None
        self.on_feedback_correct: Optional[Callable[[], None]] = None
        self.on_feedback_incorrect: Optional[Callable[[], None]] = None
        self.on_listening_changed: Optional[Callable[[bool], None]] = None
        self.on_category_completed: Optional[Callable[[str, int, int, float], None]] = None
    
    def set_callbacks(self, **callbacks):
        """Setează callbacks pentru UI"""
        for name, callback in callbacks.items():
            if hasattr(self, name):
                setattr(self, name, callback)
    
    def start_new_category(self, category_name: str) -> bool:
        """Începe o categorie nouă"""
        category = self.word_manager.get_category(category_name)
        if not category:
            return False
        
        self.state.current_category = category_name
        self.state.remaining_words = category.get_random_words()
        self.state.reset_score()
        
        self._update_score()
        self._next_word()
        return True
    
    def restart_current_category(self) -> None:
        """Restart categoria curentă"""
        self.start_new_category(self.state.current_category)
    
    def skip_current_word(self) -> None:
        """Sare peste cuvântul curent"""
        self.state.add_attempt(correct=False)
        self._update_score()
        self._next_word()
    
    def speak_current_word(self) -> None:
        """Pronunță cuvântul curent"""
        if self.state.current_word:
            threading.Thread(
                target=self.audio_service.speak, 
                args=(self.state.current_word,), 
                daemon=True
            ).start()
    
    def start_listening(self) -> None:
        """Începe ascultarea pentru pronunție"""
        if self.state.is_listening:
            return
        
        self.state.is_listening = True
        self._update_listening_status()
        self._update_status(UIText.STATUS_LISTENING)
        
        # Rulează ascultarea într-un thread separat
        threading.Thread(target=self._listen_for_pronunciation, daemon=True).start()
    
    def get_available_categories(self) -> list:
        """Returnează lista categoriilor disponibile"""
        return self.word_manager.get_category_names()
    
    def get_audio_status(self) -> dict:
        """Returnează statusul serviciilor audio"""
        return self.audio_service.get_status()
    
    def _next_word(self) -> None:
        """Trece la următorul cuvânt"""
        if not self.state.remaining_words:
            self._handle_category_completion()
            return
        
        self.state.current_word = self.state.remaining_words.pop(0)
        self._update_word()
        self._update_status(UIText.STATUS_DEFAULT)
        
        # Pronunță automat cuvântul nou
        self.speak_current_word()
    
    def _listen_for_pronunciation(self) -> None:
        """Ascultă și procesează pronunția"""
        try:
            spoken_text = self.audio_service.listen()
            
            if spoken_text:
                is_correct, similarity = self.pronunciation_checker.check_pronunciation(
                    self.state.current_word, spoken_text
                )
                
                self.state.add_attempt(correct=is_correct)
                
                if is_correct:
                    self._handle_correct_pronunciation()
                else:
                    self._handle_incorrect_pronunciation(spoken_text)
                
                self._update_score()
            else:
                self._update_status("Nu am auzit nimic. Încearcă din nou.")
                
        except Exception as e:
            print(f"Eroare la ascultare: {e}")
            self._update_status("Eroare la ascultare. Încearcă din nou.")
        finally:
            self.state.is_listening = False
            self._update_listening_status()
    
    def _handle_correct_pronunciation(self) -> None:
        """Gestionează pronunția corectă"""
        self._update_status(UIText.STATUS_CORRECT)
        if self.on_feedback_correct:
            self.on_feedback_correct()
        
        # Programează trecerea la următorul cuvânt
        threading.Timer(
            AppConfig.SUCCESS_DISPLAY_TIME / 1000, 
            self._next_word
        ).start()
    
    def _handle_incorrect_pronunciation(self, spoken_text: str) -> None:
        """Gestionează pronunția incorectă"""
        feedback_msg = self.pronunciation_checker.get_feedback_message(
            self.state.current_word, spoken_text, False
        )
        self._update_status(feedback_msg)
        
        if self.on_feedback_incorrect:
            self.on_feedback_incorrect()
    
    def _handle_category_completion(self) -> None:
        """Gestionează finalizarea categoriei"""
        if self.on_category_completed:
            self.on_category_completed(
                self.state.current_category,
                self.state.score,
                self.state.total_attempts,
                self.state.get_score_percentage()
            )
    
    def _update_word(self) -> None:
        """Actualizează cuvântul în UI"""
        if self.on_word_changed:
            self.on_word_changed(self.state.current_word)
    
    def _update_score(self) -> None:
        """Actualizează scorul în UI"""
        if self.on_score_changed:
            self.on_score_changed(self.state.score, self.state.total_attempts)
    
    def _update_status(self, message: str) -> None:
        """Actualizează statusul în UI"""
        if self.on_status_changed:
            self.on_status_changed(message)
    
    def _update_listening_status(self) -> None:
        """Actualizează statusul de ascultare în UI"""
        if self.on_listening_changed:
            self.on_listening_changed(self.state.is_listening)